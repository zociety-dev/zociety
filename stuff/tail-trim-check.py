#!/usr/bin/env python3
"""Cycle 82: does removing the single largest AD term restore ncx2 moments?

Same cycle 75 gate statistic as stuff/tail-source-check.py, new seed. For each
sample it computes three versions of the statistic:
  full    : the gate statistic as defined
  drop1   : the same sum with its single largest term removed
  floorF  : every denominator F = Phi(z) floored at 1/(2n) (caps the 1/F weight)
and reports seed, sims, mean, variance, var/mean^2, p90/p95/p99 per law and n
(rule 1), plus the top-1% mean share of the largest term (rule 2). If the tail
is one draw's 1/F weight, drop1 and floorF should both bring var/mean^2 under
the ncx2 ceiling of 2/3 for t(3).
"""
import math, random, csv

SEED, SIMS, NS = 82003, 4000, (25, 50)

def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def draw(rng, law, n):
    if law == "t3":
        return [rng.gauss(0, 1) / math.sqrt(rng.gammavariate(1.5, 2 / 3)) for _ in range(n)]
    return [rng.gauss(0, 1) for _ in range(n)]

def gate(xs):
    n = len(xs)
    m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    z = sorted((x - m) / sd for x in xs)
    terms, floored = [], []
    for i, v in enumerate(z, start=1):
        f = min(max(phi(v), 1e-12), 1 - 1e-12)
        e = ((i - 0.5) / n - f) ** 2
        terms.append(e / f)
        floored.append(e / max(f, 1 / (2 * n)))
    s, k = sum(terms), n ** -0.5
    return s * k, (s - max(terms)) * k, sum(floored) * k, max(terms) / s

def pct(v, p):
    v = sorted(v)
    return v[max(0, min(len(v) - 1, math.ceil(p * len(v)) - 1))]

rows = []
for law in ("t3", "normal"):
    for n in NS:
        rng = random.Random(SEED * 100 + n + (0 if law == "t3" else 1))
        recs = [gate(draw(rng, law, n)) for _ in range(SIMS)]
        top = sorted(recs, key=lambda r: -r[0])[: SIMS // 100]
        share = sum(r[3] for r in top) / len(top)
        for j, ver in enumerate(("full", "drop1", "floorF")):
            st = [r[j] for r in recs]
            mean = sum(st) / SIMS
            var = sum((x - mean) ** 2 for x in st) / (SIMS - 1)
            rows.append(dict(law=law, n=n, version=ver, seed=SEED, sims=SIMS,
                mean=round(mean, 4), var=round(var, 4), var_over_mean2=round(var / mean ** 2, 3),
                p90=round(pct(st, .9), 4), p95=round(pct(st, .95), 4), p99=round(pct(st, .99), 4),
                top1_largest_term_share=round(share, 3)))
with open("stuff/tail-trim-check.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
for r in rows:
    print(r)
