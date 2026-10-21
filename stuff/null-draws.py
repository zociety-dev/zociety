#!/usr/bin/env python3
"""Per-draw null gate statistics for n=25, 50, 100, two seeds each (rule 1 record).

Rule 1: every simulation run stores per-draw null statistics for each n it
tests, two seeds each, one row per draw. This script produces exactly that and
nothing else, so later margin or flag-rate claims can resample real draws.

Model is the cycle 68 gate, reproduced verbatim so draws are comparable:
  * null pool = n i.i.d. N(0,1) values
  * statistic = lower-tail-weighted Anderson-Darling on standardized data
    (same lower_tail_ad as stuff/margin-sweep-n50.py)
  * reference critical = cycle 68's n=50 value 0.06059550007392117, applied
    unchanged at every n so the false-flag rate can be compared across n.
    A per-n 95th percentile is also stored so a per-n critical can be read off.

Output (stdout, CSV): n,seed,draw,stat   one row per draw.
Summary per (n, seed) goes to stderr: draws, p95 of stat, false-flag rate
against the fixed cycle 68 critical, with a 95% Wilson interval.
Pure python, fixed seeds, no third-party deps.
Usage: python3 -I stuff/null-draws.py > stuff/null-draws.csv
"""
import math, random, sys

NS = (25, 50, 100)
SEEDS = (65068, 65069)
REPS = 2000
CRIT_C68 = 0.06059550007392117


def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def lower_tail_ad(xs):
    m = sum(xs) / len(xs)
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))
    z = sorted((x - m) / sd for x in xs)
    n = len(z)
    s = 0.0
    for i, v in enumerate(z, start=1):
        f = min(max(phi(v), 1e-12), 1 - 1e-12)
        fn = (i - 0.5) / n
        s += (fn - f) ** 2 / f
    return s / n * n ** 0.5


def pct(vals, p):
    v = sorted(vals)
    k = max(0, min(len(v) - 1, math.ceil(p * len(v)) - 1))
    return v[k]


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def main():
    sys.stdout.write("n,seed,draw,stat\n")
    sys.stderr.write("n,seed,draws,p95_stat,flags_at_c68_crit,false_flag_rate,wilson_lo,wilson_hi\n")
    for n in NS:
        for seed in SEEDS:
            rng = random.Random(seed)
            stats = []
            for d in range(REPS):
                s = lower_tail_ad([rng.gauss(0, 1) for _ in range(n)])
                stats.append(s)
                sys.stdout.write(f"{n},{seed},{d},{s:.6f}\n")
            flags = sum(s >= CRIT_C68 for s in stats)
            lo, hi = wilson(flags, REPS)
            sys.stderr.write(f"{n},{seed},{REPS},{pct(stats, 0.95):.6f},{flags},"
                             f"{flags / REPS:.4f},{lo:.4f},{hi:.4f}\n")


if __name__ == "__main__":
    main()
