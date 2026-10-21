#!/usr/bin/env python3
"""Scale-free tail check: does the cycle 75 statistic decay like ncx2(3, lambda)?

Companion to stuff/ncx2-shape-check.py (member-2), which rescales by the null
p95 and finds a huge variance. Rescaling by any constant leaves quantile
RATIOS unchanged, so this file compares p95/p90, p99/p95, p99/p90 of the raw
cycle 75 alternative draws (stuff/c75-df3-draws.csv, seeds 65068+65069
pooled, 4000 per n) against the same ratios for ncx2(3, lambda) with
cycle 80's lambda (4.018 at n=25, 7.154 at n=50), plus the exceedance
fraction above c * p95 for c in 1.5, 2, 3, and a Hill tail-index estimate
on the top 5 percent. ncx2 has an exponential tail (Hill index grows with
the sample); a t(3)-driven statistic has a power-law tail (Hill index stays
near a small constant). Also reports mean and variance of the raw draws
and of the ncx2 reference (rule 1).
Usage: python3 -I stuff/tail-ratio-check.py > stuff/tail-ratio-check.csv
"""
import csv, math, os, random, sys

NS = (25, 50)
LAMBDA = {25: 4.018, 50: 7.154}
NCX2_SIMS = 20000
NCX2_SEED = 65082
HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    out = {n: [] for n in NS}
    with open(os.path.join(HERE, name)) as f:
        for r in csv.DictReader(f):
            if int(r["n"]) in out:
                out[int(r["n"])].append(float(r["stat"]))
    return out


def pct(v, p):
    v = sorted(v)
    k = (len(v) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def mean_var(v):
    m = sum(v) / len(v)
    return m, sum((x - m) ** 2 for x in v) / (len(v) - 1)


def hill(v, frac=0.05):
    s = sorted(v, reverse=True)
    k = int(len(s) * frac)
    top, thr = s[:k], s[k]
    if thr <= 0:
        return float("nan")
    return k / sum(math.log(x / thr) for x in top)


def row(n, src, sims, seed, v):
    m, var = mean_var(v)
    p90, p95, p99 = pct(v, .9), pct(v, .95), pct(v, .99)
    exc = [sum(x > c * p95 for x in v) / len(v) for c in (1.5, 2, 3)]
    return [n, src, sims, seed, f"{m:.4g}", f"{var:.4g}", f"{p95/p90:.3f}",
            f"{p99/p95:.3f}", f"{p99/p90:.3f}", *[f"{e:.4f}" for e in exc],
            f"{hill(v):.2f}"]


alt = load("c75-df3-draws.csv")
rng = random.Random(NCX2_SEED)
w = csv.writer(sys.stdout)
w.writerow(["n", "source", "sims", "seed", "mean", "variance", "p95/p90", "p99/p95",
            "p99/p90", "frac>1.5p95", "frac>2p95", "frac>3p95", "hill_top5pct"])
for n in NS:
    w.writerow(row(n, "cycle75_t3_raw", len(alt[n]), "65068+65069", alt[n]))
    s = math.sqrt(LAMBDA[n])
    nc = [rng.gauss(s, 1) ** 2 + rng.gauss(0, 1) ** 2 + rng.gauss(0, 1) ** 2
          for _ in range(NCX2_SIMS)]
    w.writerow(row(n, f"ncx2_3_{LAMBDA[n]}", NCX2_SIMS, NCX2_SEED, nc))
