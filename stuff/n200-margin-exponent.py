#!/usr/bin/env python3
"""Cycle 76, member-2: n=200 stored-row, two-seed run and the margin-exponent fit.

Protocol (rule 1, protocol parity across n):
  * df=3 statistic: three independent group-mean contrasts, each a standardized
    mean of n draws, summed as squares. Under the null (shift 0) this is
    chi-square with 3 df; under the alternative every contrast is shifted by
    DELTA so the stat is non-central.
  * Stored rows: for each seed, each n and each rep the n*3 draws are generated
    once from a seeded generator and reused for the null and alternative arms
    (the alternative adds DELTA to the same rows), so the two arms are paired.
  * Critical value per n: that n's own stored null p95.
  * Margin per n: median(df=3 stat under the alternative) / null p95.
  * Two seeds; a point enters the fit only if the seeds agree within the
    bootstrap half-width.

Rule 2 (step-and-interval test):
  * Fit log(margin) on log(n) over n=25, 50, 100, 200 by least squares.
  * Bootstrap the slope with 1000 resamples of the stored-row pairs.
  * sqrt(n) if the 95% interval covers 0.5, linear if it covers 1.0,
    undecided if it covers both or neither. Adjacent-n steps must also each
    clear their bootstrap half-widths.

Pure python, no numpy. Run: python3 -I stuff/n200-margin-exponent.py
"""
import math
import random
import statistics

NS = [25, 50, 100, 200]
REPS = 2000          # stored rows per n per seed
BOOT = 1000          # bootstrap resamples of the stored-row pairs
DELTA = 0.2          # shift on each of the three contrasts
SEEDS = [1, 2]
ALPHA_Q = 0.95


def quantile(xs, q):
    s = sorted(xs)
    k = (len(s) - 1) * q
    lo = math.floor(k)
    hi = math.ceil(k)
    if lo == hi:
        return s[lo]
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def stored_rows(seed, n):
    """Return (null_stats, alt_stats) for REPS stored rows, paired by row."""
    rng = random.Random(seed * 100003 + n)
    null, alt = [], []
    root_n = math.sqrt(n)
    for _ in range(REPS):
        s0 = 0.0
        s1 = 0.0
        for _ in range(3):
            m = sum(rng.gauss(0.0, 1.0) for _ in range(n)) / n
            z0 = m * root_n
            z1 = (m + DELTA) * root_n
            s0 += z0 * z0
            s1 += z1 * z1
        null.append(s0)
        alt.append(s1)
    return null, alt


def margin(null, alt):
    return statistics.median(alt) / quantile(null, ALPHA_Q)


def fit_slope(ns, margins):
    xs = [math.log(n) for n in ns]
    ys = [math.log(m) for m in margins]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    sxx = sum((x - xbar) ** 2 for x in xs)
    sxy = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    return sxy / sxx


def main():
    rows = {seed: {n: stored_rows(seed, n) for n in NS} for seed in SEEDS}
    rng = random.Random(76)

    # Point estimates per seed and per n.
    point = {seed: {n: margin(*rows[seed][n]) for n in NS} for seed in SEEDS}
    nullrate = {
        seed: {
            n: sum(1 for s in rows[seed][n][0] if s > quantile(rows[seed][n][0], ALPHA_Q))
            / REPS
            for n in NS
        }
        for seed in SEEDS
    }
    power = {
        seed: {
            n: sum(1 for s in rows[seed][n][1] if s > quantile(rows[seed][n][0], ALPHA_Q))
            / REPS
            for n in NS
        }
        for seed in SEEDS
    }

    # Bootstrap: resample stored-row pairs (null, alt) together, per n, per seed.
    boot_margin = {seed: {n: [] for n in NS} for seed in SEEDS}
    boot_slope = {seed: [] for seed in SEEDS}
    for seed in SEEDS:
        for _ in range(BOOT):
            ms = []
            for n in NS:
                null, alt = rows[seed][n]
                idx = [rng.randrange(REPS) for _ in range(REPS)]
                bn = [null[i] for i in idx]
                ba = [alt[i] for i in idx]
                m = margin(bn, ba)
                boot_margin[seed][n].append(m)
                ms.append(m)
            boot_slope[seed].append(fit_slope(NS, ms))

    print(f"protocol: REPS={REPS} BOOT={BOOT} DELTA={DELTA} seeds={SEEDS}")
    print()
    print("per-n results (seed: margin [boot 95% CI], null rate, power)")
    half = {seed: {} for seed in SEEDS}
    for n in NS:
        for seed in SEEDS:
            lo = quantile(boot_margin[seed][n], 0.025)
            hi = quantile(boot_margin[seed][n], 0.975)
            half[seed][n] = (hi - lo) / 2
            print(
                f"  n={n:3d} seed={seed}: margin={point[seed][n]:.3f} "
                f"[{lo:.3f}, {hi:.3f}] null_rate={nullrate[seed][n]:.3f} "
                f"power={power[seed][n]:.3f}"
            )
    print()

    # Rule 1: seed agreement within the bootstrap half-width.
    print("rule 1 seed agreement (|seed1 - seed2| <= max half-width)")
    admitted = []
    for n in NS:
        diff = abs(point[1][n] - point[2][n])
        hw = max(half[1][n], half[2][n])
        ok = diff <= hw
        print(f"  n={n:3d}: diff={diff:.3f} half_width={hw:.3f} -> {'enters fit' if ok else 'EXCLUDED'}")
        if ok:
            admitted.append(n)
    print()

    # Rule 2: adjacent steps must clear the bootstrap half-widths.
    print("rule 2 adjacent-n steps (pooled seeds)")
    pooled = {n: (point[1][n] + point[2][n]) / 2 for n in NS}
    steps_ok = True
    for a, b in zip(NS, NS[1:]):
        step = pooled[b] - pooled[a]
        hw = max(half[1][a], half[2][a], half[1][b], half[2][b])
        ok = step > hw
        steps_ok = steps_ok and ok
        print(f"  {a:3d}->{b:3d}: step={step:.3f} half_width={hw:.3f} -> {'clears' if ok else 'DOES NOT clear'}")
    print()

    # Rule 2: fitted exponent and bootstrap interval, per seed and pooled.
    print("rule 2 exponent fit of log(margin) on log(n)")
    verdicts = []
    for seed in SEEDS:
        slope = fit_slope(NS, [point[seed][n] for n in NS])
        lo = quantile(boot_slope[seed], 0.025)
        hi = quantile(boot_slope[seed], 0.975)
        covers_half = lo <= 0.5 <= hi
        covers_one = lo <= 1.0 <= hi
        if covers_half and not covers_one:
            v = "sqrt(n)"
        elif covers_one and not covers_half:
            v = "linear"
        else:
            v = "undecided"
        verdicts.append(v)
        print(f"  seed={seed}: slope={slope:.3f} [{lo:.3f}, {hi:.3f}] -> {v}")
    pooled_slope = fit_slope(NS, [pooled[n] for n in NS])
    allb = boot_slope[1] + boot_slope[2]
    lo = quantile(allb, 0.025)
    hi = quantile(allb, 0.975)
    print(f"  pooled: slope={pooled_slope:.3f} [{lo:.3f}, {hi:.3f}]")
    print()
    print(f"points admitted by rule 1: {admitted}")
    print(f"adjacent steps all clear: {steps_ok}")
    print(f"verdicts by seed: {verdicts}")
    print(f"fit trusted: {steps_ok and admitted == NS}")


if __name__ == "__main__":
    main()
