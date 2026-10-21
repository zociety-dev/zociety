#!/usr/bin/env python3
"""Measure, on held-out lognormal pools, the false-alarm rate of rule 2's
calibrated Anderson-Darling cutoff versus the textbook asymptotic one.

Rule 2 sets the cutoff at the 95th percentile of A^2 across >=10,000
simulated lognormal pools of the same size. A cutoff estimated from a
simulation is itself noisy, so this script calibrates on one batch and
counts rejections on a second, independent batch. If the calibration is
sound the held-out false-alarm rate sits near 5%.

Usage: ad-false-alarm-check.py [n=50] [sims=10000] [seed=66]
Pure standard library; runs in a few seconds at the defaults.
"""
import math
import random
import sys

TEXTBOOK_5PCT = 0.752  # Stephens, case 3, applied to A*=A^2(1+0.75/n+2.25/n^2)


def ad_stat(logs):
    n = len(logs)
    mu = sum(logs) / n
    sd = math.sqrt(sum((x - mu) ** 2 for x in logs) / (n - 1))
    z = sorted((x - mu) / sd for x in logs)
    cdf = [min(max(0.5 * (1 + math.erf(v / math.sqrt(2))), 1e-12), 1 - 1e-12) for v in z]
    s = sum((2 * i + 1) * (math.log(cdf[i]) + math.log(1 - cdf[n - 1 - i])) for i in range(n))
    return -n - s / n


def batch(rng, n, sims):
    # Lognormal with sigma 0.5: the log is normal, and AD on the logs is
    # location/scale invariant, so drawing the logs directly is exact.
    return [ad_stat([rng.gauss(0.0, 0.5) for _ in range(n)]) for _ in range(sims)]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    sims = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
    rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 66)

    calib = sorted(batch(rng, n, sims))
    cutoff = calib[int(math.ceil(0.95 * sims)) - 1]
    held = batch(rng, n, sims)

    adj = 1 + 0.75 / n + 2.25 / n ** 2
    fa_cal = sum(a > cutoff for a in held) / sims
    fa_txt = sum(a * adj > TEXTBOOK_5PCT for a in held) / sims
    se = math.sqrt(0.05 * 0.95 / sims)

    print(f"n={n} sims={sims} per batch")
    print(f"calibrated 5% cutoff (raw A^2): {cutoff:.4f}")
    print(f"held-out false-alarm, calibrated cutoff: {fa_cal:.4f}")
    print(f"held-out false-alarm, textbook A*>{TEXTBOOK_5PCT}: {fa_txt:.4f}")
    print(f"binomial s.e. at 5%: {se:.4f}  (|rate-0.05| under ~2 s.e. is consistent)")


if __name__ == "__main__":
    main()
