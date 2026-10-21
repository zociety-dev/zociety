#!/usr/bin/env python3
"""Cycle 78, member-2: is the 0.03 intercept gap a small-n threshold artefact?

Follows the cycle-77 stored-row protocol (small-n-intercept-test.py) and
implements rules 1 and 2 of this cycle:

  1. Print each per-n null p95 beside chi2_95(3) = 7.815.
  2. Refit margin = a + b*n with the asymptotic threshold 7.815 substituted
     for the empirical null p95 at n=10 and n=15 only (all other n keep their
     own stored null p95, as rule 1 of cycle 77 requires).
  3. Report the intercept gap a - 0.303 as a signed difference with its
     bootstrap interval, for the original fit and for the refit, and say in
     one line whether the refit closes, narrows, or leaves the gap.
  4. Add a third seed at n=10 and n=15 only if the gap is unchanged, i.e. the
     refit's gap interval still excludes zero and its centre moved by less
     than the original bootstrap half-width.

Margin is the ratio form median(alt stat) / threshold. Two seeds per n; the
per-n margin is the mean of the two seeds' margins (seeds agreed within the
bootstrap half-width in cycle 77, so no admission gate is re-run here).

Pure python, no numpy. Run: python3 -I stuff/threshold-refit.py
"""
import math
import random
import statistics

NS = [10, 15, 25, 50, 100, 200]
SMALL = {10, 15}
REPS = 2000
BOOT = 600
DELTA = 0.2
SEEDS = [1, 2]
THIRD_SEED = 3
CHI2_95_DF3 = 7.814728
CHI2_MED_DF3 = 2.365974
A_ANALYTIC = CHI2_MED_DF3 / CHI2_95_DF3
B_ANALYTIC = 3 * DELTA ** 2 / CHI2_95_DF3


def quantile(xs, q):
    s = sorted(xs)
    k = (len(s) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    if lo == hi:
        return s[lo]
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def stored_rows(seed, n):
    rng = random.Random(seed * 100003 + n)
    null, alt = [], []
    root_n = math.sqrt(n)
    for _ in range(REPS):
        s0 = s1 = 0.0
        for _ in range(3):
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
    a = my - b * mx
    return a, b


def margin_from(null, alt, asymptotic):
    thr = CHI2_95_DF3 if asymptotic else quantile(null, 0.95)
    return statistics.median(alt) / thr


def bootstrap_a(rows, seeds, asymptotic_small, rng):
    """Resample stored rows per seed per n, recompute margins, refit; return
    the list of bootstrap intercepts."""
    out = []
    for _ in range(BOOT):
        ys = []
        for n in NS:
            ms = []
            for s in seeds:
                null, alt = rows[(s, n)]
                idx = [rng.randrange(REPS) for _ in range(REPS)]
                bn = [null[i] for i in idx]
                ba = [alt[i] for i in idx]
                ms.append(margin_from(bn, ba, asymptotic_small and n in SMALL))
            ys.append(sum(ms) / len(ms))
        a, _ = fit_affine(NS, ys)
        out.append(a)
    return out


def point_fit(rows, seeds, asymptotic_small):
    ys = []
    for n in NS:
        ms = [margin_from(*rows[(s, n)], asymptotic_small and n in SMALL)
              for s in seeds]
        ys.append(sum(ms) / len(ms))
    return fit_affine(NS, ys)


def report(label, rows, seeds, asymptotic_small, rng):
    a, b = point_fit(rows, seeds, asymptotic_small)
    boots = bootstrap_a(rows, seeds, asymptotic_small, rng)
    lo, hi = quantile(boots, 0.025), quantile(boots, 0.975)
    gap = a - A_ANALYTIC
    print(f"{label}: a = {a:.3f} [{lo:.3f}, {hi:.3f}]  b = {b:.4f}  "
          f"(analytic a = {A_ANALYTIC:.3f}, b = {B_ANALYTIC:.4f})")
    print(f"  gap a - 0.303 = {gap:+.3f} "
          f"[{lo - A_ANALYTIC:+.3f}, {hi - A_ANALYTIC:+.3f}]  "
          f"analytic inside interval: {lo <= A_ANALYTIC <= hi}")
    return a, lo, hi, gap


def main():
    rows = {(s, n): stored_rows(s, n) for s in SEEDS for n in NS}

    print("Rule 1: per-n null p95 beside chi2_95(3) = 7.815")
    print(f"{'n':>4} {'seed':>4} {'null p95':>9} {'diff':>7} {'ratio':>6}")
    for n in NS:
        for s in SEEDS:
            p95 = quantile(rows[(s, n)][0], 0.95)
            print(f"{n:>4} {s:>4} {p95:>9.3f} {p95 - CHI2_95_DF3:>+7.3f} "
                  f"{p95 / CHI2_95_DF3:>6.3f}")
    print()

    rng = random.Random(2026)
    a0, lo0, hi0, gap0 = report("original (empirical p95 at every n)",
                                rows, SEEDS, False, rng)
    a1, lo1, hi1, gap1 = report("refit (7.815 at n=10, 15 only)",
                                rows, SEEDS, True, rng)

    half = (hi0 - lo0) / 2
    excludes = not (lo1 <= A_ANALYTIC <= hi1)
    moved = abs(gap1 - gap0)
    if not excludes:
        verdict = "closes"
    elif moved >= half:
        verdict = "narrows"
    else:
        verdict = "leaves"
    print()
    print(f"Verdict: the asymptotic-threshold refit {verdict} the gap "
          f"({gap0:+.3f} -> {gap1:+.3f}, moved {moved:.3f} vs half-width "
          f"{half:.3f}).")

    if verdict == "leaves":
        print()
        print(f"Gap unchanged: adding seed {THIRD_SEED} at n=10 and n=15 "
              f"(rule 2 condition).")
        for n in sorted(SMALL):
            rows[(THIRD_SEED, n)] = stored_rows(THIRD_SEED, n)
            p95 = quantile(rows[(THIRD_SEED, n)][0], 0.95)
            print(f"{n:>4} {THIRD_SEED:>4} {p95:>9.3f} "
                  f"{p95 - CHI2_95_DF3:>+7.3f} {p95 / CHI2_95_DF3:>6.3f}")
        # Third seed only exists at the small n; other n keep two seeds.
        for n in NS:
            if n not in SMALL:
                rows[(THIRD_SEED, n)] = rows[(SEEDS[0], n)]
        seeds3 = SEEDS + [THIRD_SEED]
        # Avoid double-counting seed 1 at large n: average over distinct rows.
        def point_fit3(asym):
            ys = []
            for n in NS:
                ss = seeds3 if n in SMALL else SEEDS
                ms = [margin_from(*rows[(s, n)], asym and n in SMALL)
                      for s in ss]
                ys.append(sum(ms) / len(ms))
            return fit_affine(NS, ys)
        a3, b3 = point_fit3(False)
        a3r, _ = point_fit3(True)
        print(f"three-seed point fit: a = {a3:.3f} (gap {a3 - A_ANALYTIC:+.3f}), "
              f"refit a = {a3r:.3f} (gap {a3r - A_ANALYTIC:+.3f}), b = {b3:.4f}")
        print("Model unchanged this cycle; bootstrap of the three-seed fit "
              "is the next turn's job if the gap persists.")


if __name__ == "__main__":
    main()
