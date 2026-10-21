#!/usr/bin/env python3
"""Cycle 84, member-3: independent replication of the top-k winsorize sweep
(seed 84003, 4000 sims per n) plus a rank decomposition of where the residual
t(3) excess sits after the cap.

Same statistic as stuff/topk-winsorize-sweep.py (cycle 71/75 lower-tail
weighted AD gate, n^-1/2 * sum_i (F_n(i) - Phi(z_i))^2 / Phi(z_i), on the
standardized sample; variant k winsorizes the k largest |draw| to the (k+1)th
largest |draw|, sign kept; k = 0 is the uncapped baseline).

Added here: in the top 1% of t(3) sims by statistic value, the post-cap AD sum
is split by original |draw| rank into
  top k        (the capped draws; this is the rule 1 share column)
  rank k+1     (the draw that sets the cap level)
  ranks k+2..k+5
  the rest
so the direction's question, where does the residual excess live, is answered
by rank rather than inferred.
"""
import math, random, csv

SEED, SIMS, NS, KS = 84003, 4000, (25, 50, 100), (0, 1, 2, 3, 5)

def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def draw(rng, law, n):
    if law == "t3":
        return [rng.gauss(0, 1) / math.sqrt(rng.gammavariate(1.5, 2 / 3)) for _ in range(n)]
    return [rng.gauss(0, 1) for _ in range(n)]

def terms_by_index(xs):
    n = len(xs)
    m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    order = sorted(range(n), key=lambda i: xs[i])
    out = [0.0] * n
    for rank, i in enumerate(order, start=1):
        f = min(max(phi((xs[i] - m) / sd), 1e-12), 1 - 1e-12)
        out[i] = ((rank - 0.5) / n - f) ** 2 / f
    return out

def stats(xs):
    n = len(xs)
    a = sorted(range(n), key=lambda i: -abs(xs[i]))
    rec = {}
    for k in KS:
        ys = list(xs)
        if k:
            cap = abs(xs[a[k]])
            for i in a[:k]:
                ys[i] = math.copysign(cap, xs[i])
        t = terms_by_index(ys)
        s = sum(t)
        parts = (sum(t[i] for i in a[:k]) / s,
                 t[a[k]] / s,
                 sum(t[i] for i in a[k + 1:k + 5]) / s)
        rec[k] = (s * n ** -0.5, parts)
    return rec

def pct(v, p):
    v = sorted(v)
    return v[max(0, min(len(v) - 1, math.ceil(p * len(v)) - 1))]

rows, crit = [], {}
for law in ("normal", "t3"):
    for n in NS:
        rng = random.Random(SEED * 100 + n + (0 if law == "t3" else 1))
        recs = [stats(draw(rng, law, n)) for _ in range(SIMS)]
        for k in KS:
            st = [r[k][0] for r in recs]
            top = sorted(recs, key=lambda r: -r[k][0])[: SIMS // 100]
            sh = [sum(r[k][1][j] for r in top) / len(top) for j in range(3)]
            mean = sum(st) / SIMS
            var = sum((x - mean) ** 2 for x in st) / (SIMS - 1)
            if law == "normal":
                crit[(k, n)] = pct(st, .95)
            power = sum(1 for x in st if x > crit[(k, n)]) / SIMS
            rows.append(dict(law=law, n=n, k=k, seed=SEED, sims=SIMS,
                mean=mean, var=var, var_over_mean2=var / mean ** 2,
                p95=pct(st, .95), p99=pct(st, .99), crit_normal_p95=crit[(k, n)], power=power,
                share_topk=sh[0], share_rank_k1=sh[1], share_rank_k2_k5=sh[2],
                share_rest=1 - sum(sh)))
with open("stuff/topk-residual-by-rank.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def g(x):
    return ("%.4g" % x) if abs(x) < 1e4 else ("%.3e" % x)
def row(law, n, k):
    return [r for r in rows if r["law"] == law and r["n"] == n and r["k"] == k][0]

print("### Rule 1 and rule 2 table: t(3), seed %d, %d sims per n per law; k = 0 is the uncapped baseline\n" % (SEED, SIMS))
print("| n | k | mean | variance | var/mean^2 | p99 | top-1% AD share of top k | power n=25 | power n=50 | power n=100 | diff vs k=0 at n=25 / 50 / 100 |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for n in (25, 50):
    for k in KS:
        r = row("t3", n, k)
        p = [row("t3", m, k)["power"] for m in NS]
        d = [row("t3", m, k)["power"] - row("t3", m, 0)["power"] for m in NS]
        print("| %d | %d | %s | %s | %s | %s | %.3f | %.3f | %.3f | %.3f | %+.3f / %+.3f / %+.3f |" % (
            n, k, g(r["mean"]), g(r["var"]), g(r["var_over_mean2"]), g(r["p99"]), r["share_topk"], *p, *d))
print("\n### Where the residual lives: post-cap AD share by original |draw| rank, top 1% of t(3) sims\n")
print("| n | k | top k (capped) | rank k+1 (sets cap) | ranks k+2..k+5 | rest |")
print("|---|---|---|---|---|---|")
for n in (25, 50):
    for k in KS:
        r = row("t3", n, k)
        print("| %d | %d | %.3f | %.3f | %.3f | %.3f |" % (n, k, r["share_topk"], r["share_rank_k1"], r["share_rank_k2_k5"], r["share_rest"]))
print("\n### Normal data, same variants (calibration rows)\n")
print("| n | k | mean | variance | var/mean^2 | p95 (critical value) | top-1% share top k / rank k+1 |")
print("|---|---|---|---|---|---|---|")
for n in NS:
    for k in KS:
        r = row("normal", n, k)
        print("| %d | %d | %s | %s | %s | %s | %.3f / %.3f |" % (n, k, g(r["mean"]), g(r["var"]), g(r["var_over_mean2"]), g(r["p95"]), r["share_topk"], r["share_rank_k1"]))
print("\n### Verdict per n (rule 2): smallest k with var/mean^2 <= 2/3 and all power diffs within 0.02\n")
for n in (25, 50):
    ok = [k for k in KS[1:] if row("t3", n, k)["var_over_mean2"] <= 2 / 3
          and all(abs(row("t3", m, k)["power"] - row("t3", m, 0)["power"]) <= 0.02 for m in NS)]
    mom = [k for k in KS[1:] if row("t3", n, k)["var_over_mean2"] <= 2 / 3]
    print("- n=%d: %s (moment-only candidates: %s)" % (n, ("k=%d" % ok[0]) if ok else "none",
          ", ".join("k=%d" % k for k in mom) if mom else "none"))
