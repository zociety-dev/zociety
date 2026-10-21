#!/usr/bin/env python3
"""Cycle 83, member-1: the follow-up cap-power-replication.md asked for.

Instead of capping one term, two variants bound the tail at its source:
  top3_50: the three largest AD terms together are capped at 0.50 of the sum
           (scaled down proportionally when they exceed it).
  wfloor3: the 1/Phi(z) weight is bounded by flooring f at Phi(-3) (and
           ceiling at Phi(3)), i.e. weight at most 1/Phi(-3) ~ 741.
Power = rejection rate under t(3) at the normal-calibrated 0.95 critical value;
the power difference (capped minus uncapped) is the tolerance check (0.02).
Rule 2: under t(3), share of the largest |draw| term in the top 1% of sims
(by the statistic) and the fraction of samples where the bound was hit.
"""
import math, random, csv

SEED, SIMS, NS = 83101, 2000, (25, 50, 100)
FLOOR = 0.5 * (1.0 + math.erf(-3 / math.sqrt(2.0)))

def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def draw(rng, law, n):
    if law == "t3":
        return [rng.gauss(0, 1) / math.sqrt(rng.gammavariate(1.5, 2 / 3)) for _ in range(n)]
    return [rng.gauss(0, 1) for _ in range(n)]

def terms_of(xs, lo):
    n = len(xs)
    m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    z = sorted((x - m) / sd for x in xs)
    out, hit = [], False
    for i, v in enumerate(z, start=1):
        f = phi(v)
        if f < lo or f > 1 - lo:
            hit = True
        f = min(max(f, lo), 1 - lo)
        out.append(((i - 0.5) / n - f) ** 2 / f)
    return out, hit

def top3(t, c=0.50):
    s = sum(t)
    st = sorted(t, reverse=True)
    k = sum(st[:3])
    if k <= c * s:
        return s, st[0] / s, False
    rest = s - k
    scale = c * rest / ((1 - c) * k)
    return rest + k * scale, st[0] * scale / (rest + k * scale), True

def stats(xs):
    k = len(xs) ** -0.5
    t, _ = terms_of(xs, 1e-12)
    s = sum(t)
    a, ash, ah = top3(t)
    w, wh = terms_of(xs, FLOOR)
    ws = sum(w)
    return {"uncapped": (s * k, max(t) / s, False), "top3_50": (a * k, ash, ah),
            "wfloor3": (ws * k, max(w) / ws, wh)}

def pct(v, p):
    v = sorted(v)
    return v[max(0, min(len(v) - 1, math.ceil(p * len(v)) - 1))]

VERS = ("uncapped", "top3_50", "wfloor3")
rows, crit, rej = [], {}, {}
for law in ("normal", "t3"):
    for n in NS:
        rng = random.Random(SEED * 1000 + n + (1 if law == "normal" else 0))
        recs = [stats(draw(rng, law, n)) for _ in range(SIMS)]
        for ver in VERS:
            vals = [r[ver][0] for r in recs]
            mean = sum(vals) / SIMS
            var = sum((v - mean) ** 2 for v in vals) / (SIMS - 1)
            if law == "normal":
                crit[(n, ver)] = pct(vals, 0.95)
            rate = sum(v > crit[(n, ver)] for v in vals) / SIMS
            rej[(law, n, ver)] = rate
            order = sorted(range(SIMS), key=lambda i: vals[i], reverse=True)[: max(1, SIMS // 100)]
            top_share = sum(recs[i][ver][1] for i in order) / len(order)
            hitf = sum(r[ver][2] for r in recs) / SIMS
            rows.append({"law": law, "n": n, "version": ver, "seed": SEED, "sims": SIMS,
                         "mean": round(mean, 4), "var": round(var, 4),
                         "var_over_mean2": round(var / mean ** 2, 3),
                         "p90": round(pct(vals, 0.90), 4), "p95": round(pct(vals, 0.95), 4),
                         "p99": round(pct(vals, 0.99), 4), "reject_rate": round(rate, 4),
                         "power_diff_vs_uncapped": round(rate - rej[(law, n, "uncapped")], 4),
                         "top1pct_max_share": round(top_share, 3), "hit_frac": round(hitf, 3)})

with open("stuff/cap-weight-floor.csv", "w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rows[0]))
    wr.writeheader()
    wr.writerows(rows)
for r in rows:
    print("%-6s %3d %-8s mean %.3f var/m2 %8.3f p90 %.3f p95 %.3f p99 %.3f rej %.3f d %+.3f top1%% %.2f hit %.3f" % (
        r["law"], r["n"], r["version"], r["mean"], r["var_over_mean2"], r["p90"], r["p95"], r["p99"],
        r["reject_rate"], r["power_diff_vs_uncapped"], r["top1pct_max_share"], r["hit_frac"]))
