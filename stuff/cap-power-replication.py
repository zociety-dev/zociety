#!/usr/bin/env python3
"""Cycle 83, member-3: independent-seed replication of the power half.

Same cycle 75 gate statistic and same cap variants as stuff/cap-single-draw-check.py
(member-2), but a fresh seed, and the power difference (capped minus uncapped)
is reported with its paired standard error so the 0.02 tolerance is judged
against Monte Carlo noise, not just the point estimate. Two alternatives are
run against the normal-calibrated gate: t(3) (as in member-2's item) and a
right-skewed law, standardized exp(N(0,1)), to check the cap does not cost
power against an alternative that is not a heavy symmetric tail.
Rule 2: post-cap top-1% largest-draw share and cap-hit fraction under t(3).
"""
import math, random, csv

SEED, SIMS, NS = 83003, 3000, (25, 50, 100)
SHARES = (0.50, 0.25)

def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def draw(rng, law, n):
    if law == "t3":
        return [rng.gauss(0, 1) / math.sqrt(rng.gammavariate(1.5, 2 / 3)) for _ in range(n)]
    if law == "lognormal":
        return [math.exp(rng.gauss(0, 1)) for _ in range(n)]
    return [rng.gauss(0, 1) for _ in range(n)]

def terms_of(xs):
    n = len(xs)
    m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    z = sorted((x - m) / sd for x in xs)
    out = []
    for i, v in enumerate(z, start=1):
        f = min(max(phi(v), 1e-12), 1 - 1e-12)
        out.append(((i - 0.5) / n - f) ** 2 / f)
    return out

def capped(terms, c):
    s, mx = sum(terms), max(terms)
    if mx <= c * s:
        return s, mx / s, False
    rest = s - mx
    newmx = c * rest / (1 - c)
    return rest + newmx, c, True

def stats(xs):
    n = len(xs)
    k = n ** -0.5
    t = terms_of(xs)
    s = sum(t)
    rec = {"uncapped": (s * k, max(t) / s, False)}
    for c in SHARES:
        sc, sh, h = capped(t, c)
        rec["share%d" % int(c * 100)] = (sc * k, sh, h)
    return rec

def pct(v, p):
    v = sorted(v)
    return v[max(0, min(len(v) - 1, math.ceil(p * len(v)) - 1))]

VERS = ("uncapped",) + tuple("share%d" % int(c * 100) for c in SHARES)
rows, crit, rej = [], {}, {}
for law in ("normal", "t3", "lognormal"):
    for n in NS:
        rng = random.Random(SEED * 100 + n + {"normal": 1, "t3": 0, "lognormal": 2}[law])
        recs = [stats(draw(rng, law, n)) for _ in range(SIMS)]
        for ver in VERS:
            vals = [r[ver][0] for r in recs]
            mean = sum(vals) / SIMS
            var = sum((v - mean) ** 2 for v in vals) / (SIMS - 1)
            if law == "normal":
                crit[(n, ver)] = pct(vals, 0.95)
            c = crit[(n, ver)]
            flags = [v > c for v in vals]
            rej[(law, n, ver)] = flags
            power = sum(flags) / SIMS
            top = sorted(range(SIMS), key=lambda i: -vals[i])[: max(1, SIMS // 100)]
            share = sum(recs[i][ver][1] for i in top) / len(top)
            hit = sum(1 for r in recs if r[ver][2]) / SIMS
            rows.append(dict(law=law, n=n, version=ver, seed=SEED, sims=SIMS,
                cap_rule="none" if ver == "uncapped" else "share<=%.2f" % (int(ver[5:]) / 100),
                mean=mean, var=var, var_over_mean2=var / mean ** 2,
                p90=pct(vals, .9), p95=pct(vals, .95), p99=pct(vals, .99),
                crit_normal_p95=c, power=power, top1_largest_share=share, cap_hit_frac=hit))

with open("stuff/cap-power-replication.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

def fmt(r):
    return "%-9s %3d %-8s %-12s %8.4f %10.3e %9.3f %7.3f %7.3f %8.3f %6.3f %5.2f %5.3f" % (
        r["law"], r["n"], r["version"], r["cap_rule"], r["mean"], r["var"], r["var_over_mean2"],
        r["p90"], r["p95"], r["p99"], r["power"], r["top1_largest_share"], r["cap_hit_frac"])
print("seed=%d sims_per_n=%d" % (SEED, SIMS))
print("law         n version  cap_rule         mean        var  var/mu^2     p90     p95      p99  power top1% hitfrac")
for r in rows:
    print(fmt(r))
print()
print("power difference (capped - uncapped) with paired SE; tolerance 0.02")
print("law         n version   diff     se   |diff|<=0.02  |diff|<=2se")
for law in ("t3", "lognormal"):
    for n in NS:
        base = rej[(law, n, "uncapped")]
        for ver in VERS[1:]:
            cap = rej[(law, n, ver)]
            d = [(1 if a else 0) - (1 if b else 0) for a, b in zip(cap, base)]
            diff = sum(d) / SIMS
            se = math.sqrt(sum((x - diff) ** 2 for x in d) / (SIMS - 1) / SIMS)
            print("%-9s %3d %-8s %+6.3f %6.3f  %-5s  %-5s" % (law, n, ver, diff, se, abs(diff) <= 0.02, abs(diff) <= 2 * se))
