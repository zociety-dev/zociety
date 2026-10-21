#!/usr/bin/env python3
"""Power of the rule-2 heavier-tail check at n=50.

Rule 1 log-transforms the pooled outages and runs Anderson-Darling for
normality with estimated mean and spread. Rule 2 sets the cutoff at the
95th percentile of that statistic over >=10,000 simulated lognormal pools.
The two earlier stuff files measured the false-alarm rate (~5%). This one
asks the other half of the direction: how often does the check catch a
pool that really is heavier-tailed than lognormal?

Alternatives (on the log scale, so log-normal = normal null):
  - log-t with 5 and 3 degrees of freedom (moderately / clearly heavier)
  - log-Pareto-like mixture: 90% lognormal, 10% from a 3x wider lognormal

Usage: python3 ad-power-heavier-tail.py [n] [sims] [seed]
"""
import math
import random
import sys


def ad_stat(xs):
    n = len(xs)
    m = sum(xs) / n
    s = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    z = sorted((x - m) / s for x in xs)
    cdf = [min(max(0.5 * math.erfc(-v / math.sqrt(2)), 1e-12), 1 - 1e-12) for v in z]
    a2 = -n - sum((2 * i + 1) * (math.log(cdf[i]) + math.log(1 - cdf[n - 1 - i]))
                  for i in range(n)) / n
    return a2


def student_t(rng, df):
    return rng.gauss(0, 1) / math.sqrt(rng.gammavariate(df / 2, 2) / df)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    sims = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
    rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 66)

    null = sorted(ad_stat([rng.gauss(0, 0.5) for _ in range(n)]) for _ in range(sims))
    cut = null[int(0.95 * sims)]
    print(f"n={n} sims={sims} rule-2 cutoff (95th pct) = {cut:.4f}")

    alts = {
        "lognormal (null)": lambda: rng.gauss(0, 0.5),
        "log-t df=5": lambda: 0.5 * student_t(rng, 5),
        "log-t df=3": lambda: 0.5 * student_t(rng, 3),
        "10% 3x-wide mix": lambda: rng.gauss(0, 1.5 if rng.random() < 0.1 else 0.5),
    }
    print("| pool | rejection rate |")
    print("|---|---|")
    for name, draw in alts.items():
        hits = sum(ad_stat([draw() for _ in range(n)]) > cut for _ in range(sims // 2))
        print(f"| {name} | {hits / (sims // 2):.1%} |")


if __name__ == "__main__":
    main()
