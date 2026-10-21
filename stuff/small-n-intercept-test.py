#!/usr/bin/env python3
"""Cycle 77, member-2: n=10 and n=15 under the stored-row, two-seed protocol,
and the affine-vs-pure-linear intercept test (rules 1 and 2).

Protocol (rule 1, inherited from cycle 76's n200-margin-exponent.py):
  * df=3 statistic: three standardized group means of n draws, squared and
    summed. Null is chi-square(3); the alternative shifts each mean by DELTA.
  * Stored rows: per seed, per n, per rep the draws are generated once and
    reused by both arms, so null and alternative are paired by row.
  * Critical value per n: that n's own stored null p95 (never shared across n).
  * Margin per n: median(alt stat) / that n's null p95. This is the ratio form
    the direction's analytic slope 3*delta^2/chi2_95 refers to. The difference
    form median(alt) - null p95 is printed too for the literal rule 1 wording;
    its analytic intercept is median(chi2_3) - chi2_95 < 0, so a > 0 can only
    be asked of the ratio form.
  * Two seeds; a point enters the fit only if the seeds agree within the
    bootstrap half-width.

Rule 2 (intercept test):
  * Fit margin = a + b*n (affine) and margin = b*n (pure linear) over the
    admitted n in {10, 15, 25, 50, 100, 200} by least squares.
  * AICc = N ln(RSS/N) + 2k + 2k(k+1)/(N-k-1), k = coefficients + 1 (sigma).
  * Bootstrap BOOT resamples of the stored-row pairs; record which model
    AICc prefers and the fitted a in each resample.
  * Affine wins only if it is preferred in >= 60% of resamples AND the 95%
    interval on a excludes zero. Otherwise undecided.
  * Analytic affine prediction: a = median(chi2_3)/chi2_95(3) = 2.366/7.815,
    b = 3*DELTA^2/chi2_95(3).

Pure python, no numpy. Run: python3 -I stuff/small-n-intercept-test.py
"""
import math
import random
import statistics

NS = [10, 15, 25, 50, 100, 200]
REPS = 2000
BOOT = 600
DELTA = 0.2
SEEDS = [1, 2]
ALPHA_Q = 0.95
CHI2_95_DF3 = 7.814728
CHI2_MED_DF3 = 2.365974
A_ANALYTIC = CHI2_MED_DF3 / CHI2_95_DF3
B_ANALYTIC = 3 * DELTA ** 2 / CHI2_95_DF3


def quantile(xs, q):
    s = sorted(xs)
    k = (len(s) - 1) * q
    lo = math.floor(k)
    hi = math.ceil(k)
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


def margins(null, alt):
    p95 = quantile(null, ALPHA_Q)
    med = statistics.median(alt)
    return med / p95, med - p95


def fit_affine(ns, ms):
    N = len(ns)
    xbar = sum(ns) / N
    ybar = sum(ms) / N
    sxx = sum((x - xbar) ** 2 for x in ns)
    sxy = sum((x - xbar) * (y - ybar) for x, y in zip(ns, ms))
    b = sxy / sxx
    a = ybar - b * xbar
    rss = sum((y - a - b * x) ** 2 for x, y in zip(ns, ms))
    return a, b, rss


def fit_linear(ns, ms):
    b = sum(x * y for x, y in zip(ns, ms)) / sum(x * x for x in ns)
    rss = sum((y - b * x) ** 2 for x, y in zip(ns, ms))
    return b, rss


def aicc(rss, N, k):
    rss = max(rss, 1e-12)
    return N * math.log(rss / N) + 2 * k + 2 * k * (k + 1) / (N - k - 1)


def main():
    rows = {seed: {n: stored_rows(seed, n) for n in NS} for seed in SEEDS}
    rng = random.Random(77)
    point = {seed: {n: margins(*rows[seed][n]) for n in NS} for seed in SEEDS}
    power = {
        seed: {
            n: sum(1 for s in rows[seed][n][1] if s > quantile(rows[seed][n][0], ALPHA_Q)) / REPS
            for n in NS
        }
        for seed in SEEDS
    }

    boot = {seed: {n: [] for n in NS} for seed in SEEDS}
    for seed in SEEDS:
        for _ in range(BOOT):
            for n in NS:
                null, alt = rows[seed][n]
                idx = [rng.randrange(REPS) for _ in range(REPS)]
                boot[seed][n].append(margins([null[i] for i in idx], [alt[i] for i in idx]))

    print(f"protocol: REPS={REPS} BOOT={BOOT} DELTA={DELTA} seeds={SEEDS} ns={NS}")
    print(f"analytic affine prediction: a={A_ANALYTIC:.4f} b={B_ANALYTIC:.5f}")
    print()
    print("per-n results (ratio margin [boot 95% CI], difference margin, power)")
    half = {seed: {} for seed in SEEDS}
    for n in NS:
        for seed in SEEDS:
            r = [m[0] for m in boot[seed][n]]
            lo, hi = quantile(r, 0.025), quantile(r, 0.975)
            half[seed][n] = (hi - lo) / 2
            print(
                f"  n={n:3d} seed={seed}: ratio={point[seed][n][0]:.3f} [{lo:.3f}, {hi:.3f}] "
                f"diff={point[seed][n][1]:+.3f} power={power[seed][n]:.3f}"
            )
    print()

    print("rule 1 seed agreement (|seed1 - seed2| <= max half-width), ratio form")
    admitted = []
    for n in NS:
        diff = abs(point[1][n][0] - point[2][n][0])
        hw = max(half[1][n], half[2][n])
        ok = diff <= hw
        print(f"  n={n:3d}: diff={diff:.3f} half_width={hw:.3f} -> {'enters fit' if ok else 'EXCLUDED'}")
        if ok:
            admitted.append(n)
    print()

    pooled = [(point[1][n][0] + point[2][n][0]) / 2 for n in admitted]
    a, b, rss_a = fit_affine(admitted, pooled)
    bl, rss_l = fit_linear(admitted, pooled)
    N = len(admitted)
    aicc_a, aicc_l = aicc(rss_a, N, 3), aicc(rss_l, N, 2)
    print(f"point fit over admitted n={admitted} (pooled seeds)")
    print(f"  affine: a={a:.4f} b={b:.5f} rss={rss_a:.5f} AICc={aicc_a:.2f}")
    print(f"  linear: b={bl:.5f} rss={rss_l:.5f} AICc={aicc_l:.2f}")
    print(f"  analytic: a={A_ANALYTIC:.4f} b={B_ANALYTIC:.5f}  (fitted a - analytic a = {a - A_ANALYTIC:+.4f})")
    print()

    wins = 0
    boot_a = []
    boot_b = []
    for i in range(BOOT):
        ms = [(boot[1][n][i][0] + boot[2][n][i][0]) / 2 for n in admitted]
        ba, bb, r_a = fit_affine(admitted, ms)
        _, r_l = fit_linear(admitted, ms)
        boot_a.append(ba)
        boot_b.append(bb)
        if aicc(r_a, N, 3) < aicc(r_l, N, 2):
            wins += 1
    frac = wins / BOOT
    a_lo, a_hi = quantile(boot_a, 0.025), quantile(boot_a, 0.975)
    b_lo, b_hi = quantile(boot_b, 0.025), quantile(boot_b, 0.975)
    crit1 = frac >= 0.60
    crit2 = a_lo > 0 or a_hi < 0
    print("rule 2 intercept test (bootstrap over stored-row pairs, both seeds pooled)")
    print(f"  criterion 1: affine preferred by AICc in {frac:.1%} of resamples (need >= 60%) -> {'met' if crit1 else 'not met'}")
    print(f"  criterion 2: 95% interval on a = [{a_lo:.4f}, {a_hi:.4f}] excludes zero -> {'met' if crit2 else 'not met'}")
    print(f"  95% interval on b = [{b_lo:.5f}, {b_hi:.5f}]; analytic b={B_ANALYTIC:.5f} {'inside' if b_lo <= B_ANALYTIC <= b_hi else 'OUTSIDE'}")
    print(f"  analytic a={A_ANALYTIC:.4f} {'inside' if a_lo <= A_ANALYTIC <= a_hi else 'OUTSIDE'} the bootstrap interval on a")
    verdict = "affine beats pure linear" if (crit1 and crit2) else "undecided (split verdict)" if (crit1 or crit2) else "affine does not beat pure linear"
    print(f"  verdict: {verdict}")


if __name__ == "__main__":
    main()

# --- recorded output, 2026-10-21, python3 -I stuff/small-n-intercept-test.py ---
# protocol: REPS=2000 BOOT=600 DELTA=0.2 seeds=[1, 2] ns=[10, 15, 25, 50, 100, 200]
# analytic affine prediction: a=0.3028 b=0.01536
#
# per-n results (ratio margin [boot 95% CI], difference margin, power)
#   n= 10 seed=1: ratio=0.455 [0.430, 0.478] diff=-4.163 power=0.142
#   n= 10 seed=2: ratio=0.443 [0.415, 0.469] diff=-4.175 power=0.143
#   n= 15 seed=1: ratio=0.508 [0.485, 0.545] diff=-3.802 power=0.191
#   n= 15 seed=2: ratio=0.502 [0.461, 0.539] diff=-4.004 power=0.169
#   n= 25 seed=1: ratio=0.666 [0.617, 0.710] diff=-2.542 power=0.296
#   n= 25 seed=2: ratio=0.653 [0.603, 0.687] diff=-2.718 power=0.265
#   n= 50 seed=1: ratio=1.042 [0.982, 1.110] diff=+0.330 power=0.522
#   n= 50 seed=2: ratio=1.071 [0.977, 1.120] diff=+0.528 power=0.534
#   n=100 seed=1: ratio=1.793 [1.702, 1.872] diff=+6.208 power=0.835
#   n=100 seed=2: ratio=1.770 [1.683, 1.873] diff=+6.065 power=0.835
#   n=200 seed=1: ratio=3.319 [3.172, 3.522] diff=+18.073 power=0.993
#   n=200 seed=2: ratio=3.491 [3.269, 3.729] diff=+18.809 power=0.995
#
# rule 1 seed agreement (|seed1 - seed2| <= max half-width), ratio form
#   n= 10: diff=0.011 half_width=0.027 -> enters fit
#   n= 15: diff=0.006 half_width=0.039 -> enters fit
#   n= 25: diff=0.013 half_width=0.046 -> enters fit
#   n= 50: diff=0.028 half_width=0.072 -> enters fit
#   n=100: diff=0.023 half_width=0.095 -> enters fit
#   n=200: diff=0.172 half_width=0.230 -> enters fit
#
# point fit over admitted n=[10, 15, 25, 50, 100, 200] (pooled seeds)
#   affine: a=0.2719 b=0.01556 rss=0.00311 AICc=-27.39
#   linear: b=0.01760 rss=0.22542 AICc=-11.69
#   analytic: a=0.3028 b=0.01536  (fitted a - analytic a = -0.0308)
#
# rule 2 intercept test (bootstrap over stored-row pairs, both seeds pooled)
#   criterion 1: affine preferred by AICc in 100.0% of resamples (need >= 60%) -> met
#   criterion 2: 95% interval on a = [0.2398, 0.2981] excludes zero -> met
#   95% interval on b = [0.01486, 0.01637]; analytic b=0.01536 inside
#   analytic a=0.3028 OUTSIDE the bootstrap interval on a
#   verdict: affine beats pure linear
#
# Reading: both rule 2 criteria met (affine in 100% of resamples; a in [0.240, 0.298]
# excludes zero), so affine beats pure linear. The fitted a=0.272 sits 0.031 below the
# analytic 0.303 and the analytic value falls just outside the bootstrap interval; the
# slope b matches the analytic 0.01536 inside its interval. n=10 and n=15 margins sit
# below 1 (power 0.14-0.19) and are what pins the intercept. Difference-form margins are
# negative below n=50, so "a > 0" is only meaningful for the ratio form.
