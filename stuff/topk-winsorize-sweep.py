#!/usr/bin/env python3
"""Cycle 84: after the largest |draw| is capped, where does the residual t(3)
excess in the cycle 75 gate statistic live?

Variant k (k = 0, 1, 2, 3, 5): the k largest |draw| in each sample are
winsorized to the (k+1)th largest |draw| (sign kept) before standardizing,
then the cycle 71/75 lower-tail-weighted AD gate
    n^-1/2 * sum_i (F_n(i) - Phi(z_i))^2 / Phi(z_i)
is computed on the standardized sample. k = 0 is the uncapped baseline.
Same pure-python statistic as cycles 82 and 83.

Reported per (k, n):
  var/mean^2 of the statistic under t(3)
  post-cap AD share of the top k draws (by original |draw|) averaged over the
  top 1% of t(3) sims by statistic value
  power = P(stat > normal-data p95 of the same variant at the same n) on t(3),
  i.e. the gate calibrated per n on normal data (cycle 83 convention), and the
  difference against k = 0.
"""
import math, random, csv

SEED, SIMS, NS, KS = 84002, 4000, (25, 50, 100), (0, 1, 2, 3, 5)

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

def winsorize_k(xs, k):
    if k == 0:
        return list(xs), []
    a = sorted(range(len(xs)), key=lambda i: -abs(xs[i]))
    cap = abs(xs[a[k]])
    ys = list(xs)
    for i in a[:k]:
        ys[i] = math.copysign(cap, xs[i])
    return ys, a[:k]

def stats(xs):
    n = len(xs)
    rec = {}
    for k in KS:
        ys, top = winsorize_k(xs, k)
        t = terms_by_index(ys)
        s = sum(t)
        rec[k] = (s * n ** -0.5, sum(t[i] for i in top) / s if top else 0.0)
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
            share = sum(r[k][1] for r in top) / len(top)
            mean = sum(st) / SIMS
            var = sum((x - mean) ** 2 for x in st) / (SIMS - 1)
            if law == "normal":
                crit[(k, n)] = pct(st, .95)
            power = sum(1 for x in st if x > crit[(k, n)]) / SIMS
            rows.append(dict(law=law, n=n, k=k, seed=SEED, sims=SIMS,
                winsor_q=(1 - k / n), mean=mean, var=var, var_over_mean2=var / mean ** 2,
                p90=pct(st, .9), p95=pct(st, .95), p99=pct(st, .99),
                crit_normal_p95=crit[(k, n)], power=power, top1_topk_share=share))
with open("stuff/topk-winsorize-sweep.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def g(x):
    return ("%.4g" % x) if abs(x) < 1e4 else ("%.3e" % x)
def row(law, n, k):
    return [r for r in rows if r["law"] == law and r["n"] == n and r["k"] == k][0]

print("### Rule 1 and rule 2 table: t(3), k = 0 is the uncapped baseline\n")
print("| n | k | winsor q | mean | variance | var/mean^2 | p99 | top-1% AD share of top k | power (normal-calibrated) | power minus k=0 | n=100 power minus k=0 |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for n in (25, 50):
    for k in KS:
        r = row("t3", n, k); b = row("t3", n, 0)
        r100 = row("t3", 100, k); b100 = row("t3", 100, 0)
        print("| %d | %d | %.3f | %s | %s | %s | %s | %.3f | %.3f | %+.3f | %+.3f |" % (n, k, r["winsor_q"],
            g(r["mean"]), g(r["var"]), g(r["var_over_mean2"]), g(r["p99"]), r["top1_topk_share"],
            r["power"], r["power"] - b["power"], r100["power"] - b100["power"]))
print("\n### Power at every n (t(3), gate calibrated on normal-data p95 per n)\n")
print("| k | n=25 | n=50 | n=100 | max |diff vs k=0| |")
print("|---|---|---|---|---|")
for k in KS:
    d = [row("t3", n, k)["power"] - row("t3", n, 0)["power"] for n in NS]
    print("| %d | %.3f | %.3f | %.3f | %.3f |" % ((k,) + tuple(row("t3", n, k)["power"] for n in NS) + (max(abs(x) for x in d),)))
print("\n### Normal data, same variants (calibration rows; power is 0.05 by construction)\n")
print("| n | k | mean | variance | var/mean^2 | p95 (critical value) |")
print("|---|---|---|---|---|---|")
for n in NS:
    for k in KS:
        r = row("normal", n, k)
        print("| %d | %d | %s | %s | %s | %s |" % (n, k, g(r["mean"]), g(r["var"]), g(r["var_over_mean2"]), g(r["p95"])))
print("\n### Verdict per n (rule 2): smallest k with var/mean^2 <= 2/3 and all power diffs within 0.02\n")
for n in (25, 50):
    ok = [k for k in KS[1:] if row("t3", n, k)["var_over_mean2"] <= 2 / 3
          and all(abs(row("t3", m, k)["power"] - row("t3", m, 0)["power"]) <= 0.02 for m in NS)]
    mom = [k for k in KS[1:] if row("t3", n, k)["var_over_mean2"] <= 2 / 3]
    print("- n=%d: %s (moment-only candidates: %s)" % (n, ("k=%d" % ok[0]) if ok else "none",
          ", ".join("k=%d" % k for k in mom) if mom else "none"))
