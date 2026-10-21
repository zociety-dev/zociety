#!/usr/bin/env python3
"""Calibrate the pooled floor's heavier-tail check (rules 1 and 2).

Rule 1: log-transform the outages and run an Anderson-Darling normality
test with mean and spread estimated from the data; lognormal is the null.
Rule 2: a pool fails at 5% when its A^2 exceeds the 95th percentile of A^2
across at least 10,000 simulated lognormal pools of the same size.

Usage: ad-lognormal-calibration.py [n] [sims] < outages.txt
Without stdin data it prints only the simulated critical value.
"""
import math
import random
import sys


def ad_stat(xs):
    """A^2 for normality of xs with mean and sd estimated from xs."""
    n = len(xs)
    mu = sum(xs) / n
    sd = math.sqrt(sum((x - mu) ** 2 for x in xs) / (n - 1))
    zs = sorted((x - mu) / sd for x in xs)
    cdf = [min(max(0.5 * (1 + math.erf(z / math.sqrt(2))), 1e-12), 1 - 1e-12)
           for z in zs]
    s = sum((2 * i + 1) * (math.log(cdf[i]) + math.log(1 - cdf[n - 1 - i]))
            for i in range(n))
    return -n - s / n


def critical_value(n, sims, alpha=0.05, seed=65):
    # A^2 is location/scale invariant once mu and sd are estimated, so any
    # lognormal (here sigma 0.5) gives the same null distribution on the log scale.
    rng = random.Random(seed)
    stats = sorted(ad_stat([rng.gauss(0.0, 0.5) for _ in range(n)])
                   for _ in range(sims))
    return stats[int(math.ceil((1 - alpha) * sims)) - 1]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    sims = max(int(sys.argv[2]) if len(sys.argv) > 2 else 10000, 10000)
    data = [] if sys.stdin.isatty() else [float(t) for t in sys.stdin.read().split()]
    if data:
        n = len(data)
    crit = critical_value(n, sims)
    print(f"n={n} sims={sims} A2_crit(5%)={crit:.4f}")
    if data:
        a2 = ad_stat([math.log(x) for x in data])
        verdict = "heavier tail cannot be ruled out" if a2 > crit else "lognormal holds"
        print(f"A2={a2:.4f} -> {verdict}")


if __name__ == "__main__":
    main()
