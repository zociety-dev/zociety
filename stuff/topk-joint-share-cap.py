#!/usr/bin/env python3
"""Cycle 84: joint share cap on the top k AD terms, the probe the winsorize
sweep (stuff/topk-winsorize-sweep.md) named as next.

Variant k (k = 0, 1, 2, 3, 5): compute the cycle 71/75 lower-tail-weighted
AD gate terms on the standardized sample; if the k largest terms jointly
exceed share C = 1/2 of the total, rescale them so their joint share is
exactly C. k = 0 is the uncapped baseline. Unlike winsorizing, the draws
are untouched, so standardization and the remaining terms do not move.

Per (k, n): var/mean^2 under t(3), post-cap share of the top k terms averaged
over the top 1% of t(3) sims, power = P(stat > normal-data p95 of the same
variant at the same n) on t(3), and the power difference against k = 0.
"""
import math, random, csv

SEED, SIMS, NS, KS, C = 84003, 20000, (25, 50, 100), (0, 1, 2, 3, 5), 0.5

def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def draw(rng, law, n):
    if law == "t3":
        return [rng.gauss(0, 1) / math.sqrt(rng.gammavariate(1.5, 2 / 3)) for _ in range(n)]
    return [rng.gauss(0, 1) for _ in range(n)]

def terms(xs):
    n = len(xs)
    m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    out = []
    for rank, x in enumerate(sorted(xs), start=1):
        f = min(max(phi((x - m) / sd), 1e-12), 1 - 1e-12)
        out.append(((rank - 0.5) / n - f) ** 2 / f)
    return sorted(out, reverse=True)

def stats(xs):
    t = terms(xs)
    n = len(xs)
    rec = {}
    for k in KS:
        top, rest = sum(t[:k]), sum(t[k:])
        if k and top > C * (top + rest):
            top = C / (1 - C) * rest
        s = top + rest
        rec[k] = (s * n ** -0.5, top / s if k else 0.0)
    return rec

def pct(v, p):
    v = sorted(v)
    return v[max(0, min(len(v) - 1, math.ceil(p * len(v)) - 1))]

out, crit = {}, {}
for law in ("normal", "t3"):
    for n in NS:
        rng = random.Random(SEED * 100 + n + (0 if law == "t3" else 1))
        recs = [stats(draw(rng, law, n)) for _ in range(SIMS)]
        for k in KS:
            st = [r[k][0] for r in recs]
            if law == "normal":
                crit[k, n] = pct(st, 0.95)
                continue
            mean = sum(st) / SIMS
            var = sum((s - mean) ** 2 for s in st) / (SIMS - 1)
            top = sorted(recs, key=lambda r: -r[k][0])[: max(1, SIMS // 100)]
            share = sum(r[k][1] for r in top) / len(top)
            power = sum(s > crit[k, n] for s in st) / SIMS
            out[k, n] = [var / mean ** 2, share, power]

with open("stuff/topk-joint-share-cap.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["n", "k", "var_over_mean2", "top1pct_topk_share", "power", "power_minus_k0", "normal_p95"])
    for n in NS:
        for k in KS:
            v, s, p = out[k, n]
            w.writerow([n, k, f"{v:.4g}", f"{s:.4g}", f"{p:.4g}", f"{p - out[0, n][2]:+.4f}", f"{crit[k, n]:.4g}"])
print(open("stuff/topk-joint-share-cap.csv").read())
