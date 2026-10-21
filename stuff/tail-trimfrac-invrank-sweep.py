#!/usr/bin/env python3
"""Cycle 85, follow-up to tail-trim-rankweight-sweep: sweep the trim fraction
between 0.1 and 0.2, and invert the rank weight so it damps the extreme terms
instead of the bulk.

Variants of the cycle 71/75 lower-tail-weighted AD gate
    n^-1/2 * sum_i w_i * (F_n(i) - Phi(z_i))^2 / Phi(z_i)
on the standardized sample, with w_i a function of the |draw| rank r_i
(r = 1 is the largest |draw|):
  k0     : w = 1 everywhere (uncapped baseline)
  trim   : w = 0 for r <= m = ceil(0.1 n), else 1 (trimmed sum)
  rw1    : w = r^-1 (rank-weighted sum)
  rw2    : w = r^-2
  trim15 : trim with m = ceil(0.15 n);  trim20 : m = ceil(0.2 n)
  inv1   : w = 1 - r^-1 (inverted rank weight: rank 1 gets 0, bulk ~1)
  inv2   : w = 1 - r^-2
  ramp   : w = min(1, (r - 1) / m), m = ceil(0.2 n) (linear ramp over the top)
Same pure-python statistic and t(3) draw as cycles 82-84.

Reported per (variant, n):
  var/mean^2 of the statistic under t(3)
  post-variant AD share of the top 3 draws by |draw| averaged over the top 1%
  of t(3) sims by statistic value (weighted terms over weighted sum)
  power = P(stat > normal-data p95 of the same variant at the same n) on t(3),
  i.e. the gate calibrated per n on normal data, and the difference vs k0.
"""
import math, random, csv

SEED, SIMS, NS = 85002, 4000, (25, 50, 100)
VARIANTS = ("k0", "trim", "rw1", "rw2", "trim15", "trim20", "inv1", "inv2", "ramp")
FRAC = dict(trim=0.1, trim15=0.15, trim20=0.2, ramp=0.2)

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

def weights(n, variant, absrank):
    # absrank[i] = rank of |x_i| among |x|, 1 = largest
    if variant == "k0":
        return [1.0] * n
    if variant.startswith("trim"):
        m = math.ceil(FRAC[variant] * n)
        return [0.0 if absrank[i] <= m else 1.0 for i in range(n)]
    if variant == "ramp":
        m = math.ceil(FRAC[variant] * n)
        return [min(1.0, (absrank[i] - 1) / m) for i in range(n)]
    p = 1 if variant.endswith("1") else 2
    if variant.startswith("inv"):
        return [1.0 - absrank[i] ** -p for i in range(n)]
    return [absrank[i] ** -p for i in range(n)]

def stats(xs):
    n = len(xs)
    t = terms_by_index(xs)
    a = sorted(range(n), key=lambda i: -abs(xs[i]))
    absrank = [0] * n
    for r, i in enumerate(a, start=1):
        absrank[i] = r
    top3 = a[:3]
    rec = {}
    for v in VARIANTS:
        w = weights(n, v, absrank)
        s = sum(w[i] * t[i] for i in range(n))
        share = sum(w[i] * t[i] for i in top3) / s if s > 0 else 0.0
        rec[v] = (s * n ** -0.5, share)
    return rec

def pct(v, p):
    v = sorted(v)
    return v[max(0, min(len(v) - 1, math.ceil(p * len(v)) - 1))]

rows, crit = [], {}
for law in ("normal", "t3"):
    for n in NS:
        rng = random.Random(SEED * 100 + n + (0 if law == "t3" else 1))
        recs = [stats(draw(rng, law, n)) for _ in range(SIMS)]
        for v in VARIANTS:
            st = [r[v][0] for r in recs]
            top = sorted(recs, key=lambda r: -r[v][0])[: SIMS // 100]
            share = sum(r[v][1] for r in top) / len(top)
            mean = sum(st) / SIMS
            var = sum((x - mean) ** 2 for x in st) / (SIMS - 1)
            if law == "normal":
                crit[(v, n)] = pct(st, .95)
            power = sum(1 for x in st if x > crit[(v, n)]) / SIMS
            rows.append(dict(law=law, n=n, variant=v, seed=SEED, sims=SIMS,
                trim_m=(math.ceil(FRAC[v] * n) if v in FRAC else 0),
                mean=mean, var=var, var_over_mean2=var / mean ** 2,
                p90=pct(st, .9), p95=pct(st, .95), p99=pct(st, .99),
                crit_normal_p95=crit[(v, n)], power=power, top1_top3_share=share))
with open("stuff/tail-trimfrac-invrank-sweep.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def g(x):
    return ("%.4g" % x) if abs(x) < 1e4 else ("%.3e" % x)
def row(law, n, v):
    return [r for r in rows if r["law"] == law and r["n"] == n and r["variant"] == v][0]
LABEL = dict(k0="k=0 uncapped", trim="trimmed sum (drop top m=ceil(0.1n))", rw1="rank-weighted r^-1", rw2="rank-weighted r^-2",
    trim15="trimmed sum m=ceil(0.15n)", trim20="trimmed sum m=ceil(0.2n)", inv1="inverted 1-r^-1", inv2="inverted 1-r^-2", ramp="ramp min(1,(r-1)/ceil(0.2n))")

print("### Rule 1 table: t(3), k=0 is the uncapped baseline\n")
print("| n | variant | m dropped | mean | variance | var/mean^2 | p99 | top-1% AD share of top 3 draws | power n=25 | power n=50 | power n=100 | loss n=25 | loss n=50 | loss n=100 |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for n in (25, 50):
    for v in VARIANTS:
        r = row("t3", n, v)
        pw = [row("t3", m, v)["power"] for m in NS]
        ls = [row("t3", m, v)["power"] - row("t3", m, "k0")["power"] for m in NS]
        print("| %d | %s | %d | %s | %s | %s | %s | %.3f | %.3f | %.3f | %.3f | %+.3f | %+.3f | %+.3f |" % (
            n, LABEL[v], r["trim_m"], g(r["mean"]), g(r["var"]), g(r["var_over_mean2"]), g(r["p99"]),
            r["top1_top3_share"], pw[0], pw[1], pw[2], ls[0], ls[1], ls[2]))
print("\n### Normal data, same variants (calibration rows; power is 0.05 by construction)\n")
print("| n | variant | mean | variance | var/mean^2 | p95 (critical value) |")
print("|---|---|---|---|---|---|")
for n in NS:
    for v in VARIANTS:
        r = row("normal", n, v)
        print("| %d | %s | %s | %s | %s | %s |" % (n, LABEL[v], g(r["mean"]), g(r["var"]), g(r["var_over_mean2"]), g(r["p95"])))
print("\n### Rule 2 verdict and frontier\n")
best, bestloss = None, None
for v in VARIANTS[1:]:
    vm = {n: row("t3", n, v)["var_over_mean2"] for n in (25, 50)}
    ls = {n: row("t3", n, v)["power"] - row("t3", n, "k0")["power"] for n in NS}
    mom = all(vm[n] <= 2 / 3 for n in (25, 50))
    pw = all(abs(ls[n]) <= 0.02 for n in NS)
    print("- %s: var/mean^2 n=25 %s, n=50 %s (bound %s); power loss n=25 %+.3f, n=50 %+.3f, n=100 %+.3f (within 0.02: %s); meets both: %s"
          % (LABEL[v], g(vm[25]), g(vm[50]), "met" if mom else "missed", ls[25], ls[50], ls[100], "yes" if pw else "no", "YES" if (mom and pw) else "no"))
    if mom:
        worst = max(-ls[n] for n in NS)
        if bestloss is None or worst < bestloss:
            best, bestloss = v, worst
print("- smallest power loss among variants reaching var/mean^2 <= 2/3 at both n: %s" % (("%s (worst loss %.3f)" % (LABEL[best], bestloss)) if best else "none"))
