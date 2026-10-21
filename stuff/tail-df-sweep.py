#!/usr/bin/env python3
"""Cycle 82, third check: at which tail weight does the cycle 75 gate statistic
stop being ncx2-like?

Same statistic as tail-source-check.py (lower-tail-weighted AD gate, pure
python), but the data law is swept over t(3), t(5), t(10), t(30) and N(0,1)
at n=25 and 50 with a fresh seed.  For every law the script reports mean,
variance, var/mean^2, p90/p95/p99 (rule 1) and, over the top 1% of
statistics, the share of the variance term and of the AD sum owed to the
single largest |draw| / largest term (rule 2).  Writes tail-df-sweep.csv.
"""
import math, random, csv

SEED, SIMS, NS = 82111, 4000, (25, 50)
LAWS = ("t3", "t5", "t10", "t30", "normal")

def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def draw(rng, law, n):
    if law == "normal":
        return [rng.gauss(0, 1) for _ in range(n)]
    df = int(law[1:])
    return [rng.gauss(0, 1) / math.sqrt(rng.gammavariate(df / 2, 2 / df)) for _ in range(n)]

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
for li, law in enumerate(LAWS):
    for n in NS:
        rng = random.Random(SEED * 100 + n * 10 + li)
        recs = [gate(draw(rng, law, n)) for _ in range(SIMS)]
        stat = [r[0] for r in recs]
        mean = sum(stat) / SIMS
        var = sum((s - mean) ** 2 for s in stat) / (SIMS - 1)
        top = sorted(recs, key=lambda r: -r[0])[: SIMS // 100]
        rows.append(dict(law=law, n=n, seed=SEED, sims=SIMS, mean=mean, var=var,
            var_over_mean2=var / mean ** 2, p90=pct(stat, .9), p95=pct(stat, .95), p99=pct(stat, .99), max=max(stat), var_drop_max=(lambda v: sum((x-sum(v)/len(v))**2 for x in v)/(len(v)-1))(sorted(stat)[:-1]),
            top1_share_var=sum(r[1] for r in top) / len(top), top1_share_ad=sum(r[2] for r in top) / len(top),
            all_share_var=sum(r[1] for r in recs) / SIMS, all_share_ad=sum(r[2] for r in recs) / SIMS))
with open("stuff/tail-df-sweep.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
for r in rows:
    print(" ".join(f"{k}={v:.4g}" if isinstance(v, float) else f"{k}={v}" for k, v in r.items()))
