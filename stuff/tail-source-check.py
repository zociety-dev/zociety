#!/usr/bin/env python3
"""Cycle 82: where does the cycle 75 gate statistic's heavy upper tail come from?

Regenerates the cycle 75 lower-tail-weighted AD gate statistic (same code as
the cycle 71 sweep scripts, pure python) under t(3) and under N(0,1) data at
n=25 and 50, SIMS draws per n per law, one seed. For every sample it also
records
  share_var : (max |x-m|)^2 / sum (x-m)^2  (share of the variance term owed
              to the single largest |draw|)
  share_ad  : largest single AD term / AD sum (the term is (Fn-F)^2/F; its
              denominator F = Phi(z) is smallest for the most negative draw)
and reports both shares averaged over the top 1% of statistics and over all
samples (rule 2), beside mean, variance, var/mean^2, p90/p95/p99 (rule 1).
"""
import math, random, csv

SEED, SIMS, NS = 65082, 4000, (25, 50)

def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def draw(rng, law, n):
    if law == "t3":
        return [rng.gauss(0, 1) / math.sqrt(rng.gammavariate(1.5, 2 / 3)) for _ in range(n)]
    return [rng.gauss(0, 1) for _ in range(n)]

def gate(xs):
    m = sum(xs) / len(xs)
    sq = [(x - m) ** 2 for x in xs]
    ss = sum(sq)
    sd = math.sqrt(ss / (len(xs) - 1))
    z = sorted((x - m) / sd for x in xs)
    n = len(z)
    terms = []
    for i, v in enumerate(z, start=1):
        f = min(max(phi(v), 1e-12), 1 - 1e-12)
        terms.append(((i - 0.5) / n - f) ** 2 / f)
    s = sum(terms)
    return s / n * n ** 0.5, max(sq) / ss, max(terms) / s

def pct(vals, p):
    v = sorted(vals)
    return v[max(0, min(len(v) - 1, math.ceil(p * len(v)) - 1))]

rows = []
for law in ("t3", "normal"):
    for n in NS:
        rng = random.Random(SEED * 100 + n + (0 if law == "t3" else 1))
        recs = [gate(draw(rng, law, n)) for _ in range(SIMS)]
        stat = [r[0] for r in recs]
        mean = sum(stat) / SIMS
        var = sum((s - mean) ** 2 for s in stat) / (SIMS - 1)
        top = sorted(recs, key=lambda r: -r[0])[: SIMS // 100]
        rows.append(dict(law=law, n=n, seed=SEED, sims=SIMS, mean=mean, var=var,
            var_over_mean2=var / mean ** 2, p90=pct(stat, .9), p95=pct(stat, .95), p99=pct(stat, .99),
            top1_share_var=sum(r[1] for r in top) / len(top), top1_share_ad=sum(r[2] for r in top) / len(top),
            all_share_var=sum(r[1] for r in recs) / SIMS, all_share_ad=sum(r[2] for r in recs) / SIMS))
with open("stuff/tail-source-check.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
for r in rows:
    print(" ".join(f"{k}={v:.4g}" if isinstance(v, float) else f"{k}={v}" for k, v in r.items()))
