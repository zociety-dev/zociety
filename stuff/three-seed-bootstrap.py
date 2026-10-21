#!/usr/bin/env python3
"""Cycle 78, member-3: bootstrap the three-seed fit, and explain the gap.

threshold-refit.py (member-2) found that the asymptotic-threshold refit
leaves the gap, triggered the third seed at n=10 and n=15, and reported the
three-seed point fit a = 0.275 (gap -0.028) without a bootstrap. This file
does two things.

  1. Bootstraps the three-seed fit (seeds 1, 2, 3 at n=10, 15; seeds 1, 2
     elsewhere) and reports the signed gap a - 0.303 with its interval, in
     the rule-2 format.

  2. Tests a candidate explanation that does not involve the small-n
     threshold at all. The alt statistic is an exact noncentral chi-square
     with k = 3 and lambda = 3 * delta^2 * n. The analytic intercept 0.303
     assumes median(alt) = median(chi2_3) + lambda = 2.366 + lambda, i.e.
     that the mean-minus-median skew term stays at its central value 0.634.
     It does not: for a noncentral chi-square the Pearson approximation of
     mean - median is (2/3) * (k + 3 lambda) / (k + 2 lambda), which rises
     from 2/3 at lambda = 0 toward 1 as lambda grows. So median(alt) sits
     BELOW 2.366 + lambda by an amount that grows from 0 to about 0.37 and
     saturates. A straight line fitted through a saturating negative offset
     has a negative intercept, which is exactly a downward shift of a.

     The script prints, per n, the observed median(alt) beside the naive
     prediction and the skew-corrected prediction, then fits the affine
     model to the skew-corrected analytic curve over the same n grid and
     reports the corrected analytic intercept and the gap to the empirical a.

Pure python, no numpy. Run: python3 -I stuff/three-seed-bootstrap.py
"""
import math
import random
import statistics

NS = [10, 15, 25, 50, 100, 200]
SMALL = {10, 15}
REPS = 2000
BOOT = 300
DELTA = 0.2
SEEDS = [1, 2]
THIRD_SEED = 3
K = 3
CHI2_95_DF3 = 7.814728
CHI2_MED_DF3 = 2.365974
A_ANALYTIC = CHI2_MED_DF3 / CHI2_95_DF3
B_ANALYTIC = K * DELTA ** 2 / CHI2_95_DF3


def quantile(xs, q):
    s = sorted(xs)
    k = (len(s) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    if lo == hi:
        return s[lo]
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def stored_rows(seed, n):
    """Identical generator to threshold-refit.py so the rows are the same."""
    rng = random.Random(seed * 100003 + n)
    null, alt = [], []
    root_n = math.sqrt(n)
    for _ in range(REPS):
        s0 = s1 = 0.0
        for _ in range(K):
            m = sum(rng.gauss(0.0, 1.0) for _ in range(n)) / n
            z0 = m * root_n
            z1 = (m + DELTA) * root_n
            s0 += z0 * z0
            s1 += z1 * z1
        null.append(s0)
        alt.append(s1)
    return null, alt


def fit_affine(ns, ys):
    N = len(ns)
    mx = sum(ns) / N
    my = sum(ys) / N
    sxx = sum((x - mx) ** 2 for x in ns)
    sxy = sum((x - mx) * (y - my) for x, y in zip(ns, ys))
    b = sxy / sxx
    return my - b * mx, b


def margin_from(null, alt):
    return statistics.median(alt) / quantile(null, 0.95)


def seeds_at(n):
    return SEEDS + [THIRD_SEED] if n in SMALL else SEEDS


def point_fit(rows):
    ys = []
    for n in NS:
        ms = [margin_from(*rows[(s, n)]) for s in seeds_at(n)]
        ys.append(sum(ms) / len(ms))
    return fit_affine(NS, ys)


def bootstrap_a(rows, rng):
    out = []
    for _ in range(BOOT):
        ys = []
        for n in NS:
            ms = []
            for s in seeds_at(n):
                null, alt = rows[(s, n)]
                idx = [rng.randrange(REPS) for _ in range(REPS)]
                ms.append(margin_from([null[i] for i in idx],
                                      [alt[i] for i in idx]))
            ys.append(sum(ms) / len(ms))
        out.append(fit_affine(NS, ys)[0])
    return out


def skew_term(lam):
    """Pearson mean-minus-median approximation for noncentral chi2(k, lam)."""
    return (2.0 / 3.0) * (K + 3 * lam) / (K + 2 * lam)


def main():
    rows = {(s, n): stored_rows(s, n) for n in NS for s in seeds_at(n)}

    print("Part 1: three-seed fit (seeds 1,2,3 at n=10,15; seeds 1,2 elsewhere)")
    a, b = point_fit(rows)
    boots = bootstrap_a(rows, random.Random(2078))
    lo, hi = quantile(boots, 0.025), quantile(boots, 0.975)
    print(f"a = {a:.3f} [{lo:.3f}, {hi:.3f}]  b = {b:.4f}  "
          f"(analytic a = {A_ANALYTIC:.3f}, b = {B_ANALYTIC:.4f}, "
          f"BOOT = {BOOT})")
    print(f"gap a - 0.303 = {a - A_ANALYTIC:+.3f} "
          f"[{lo - A_ANALYTIC:+.3f}, {hi - A_ANALYTIC:+.3f}]  "
          f"analytic inside interval: {lo <= A_ANALYTIC <= hi}")
    print()

    print("Part 2: observed median(alt) vs naive and skew-corrected prediction")
    print(f"{'n':>4} {'lambda':>7} {'med(alt)':>9} {'naive':>8} "
          f"{'corr':>8} {'obs-naive':>10} {'obs-corr':>9}")
    corr_curve = []
    for n in NS:
        lam = K * DELTA ** 2 * n
        med = statistics.mean(statistics.median(rows[(s, n)][1])
                              for s in seeds_at(n))
        naive = CHI2_MED_DF3 + lam
        corr = K + lam - skew_term(lam)
        corr_curve.append(corr / CHI2_95_DF3)
        print(f"{n:>4} {lam:>7.2f} {med:>9.3f} {naive:>8.3f} {corr:>8.3f} "
              f"{med - naive:>+10.3f} {med - corr:>+9.3f}")
    a_corr, b_corr = fit_affine(NS, corr_curve)
    print()
    print(f"affine fit to the skew-corrected analytic curve over the same n: "
          f"a = {a_corr:.3f}, b = {b_corr:.4f}")
    print(f"empirical a - corrected analytic a = {a - a_corr:+.3f}  "
          f"(interval [{lo - a_corr:+.3f}, {hi - a_corr:+.3f}], "
          f"corrected a inside: {lo <= a_corr <= hi})")
    print(f"empirical a - naive analytic a     = {a - A_ANALYTIC:+.3f}")
    print()
    if lo <= a_corr <= hi:
        print("Verdict: the gap is a noncentral-chi-square skew effect, not a "
              "small-n threshold artefact; the skew-corrected intercept sits "
              "inside the bootstrap interval.")
    else:
        print("Verdict: the skew correction does not fully account for the "
              "gap; something else remains.")


if __name__ == "__main__":
    main()
