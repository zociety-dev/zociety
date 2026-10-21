#!/usr/bin/env python3
"""Cycle 83: does bounding one draw's AD contribution restore ncx2 moments?

Same cycle 75 gate statistic as stuff/tail-trim-check.py (cycle 82). Variants:
  uncapped : the gate statistic as defined
  winsor   : largest |draw| winsorized to the second-largest |draw| before
             standardizing (winsorize quantile 1 - 1/n)
  share50  : any one AD term capped at share 0.50 of the AD sum
  share25  : any one AD term capped at share 0.25 of the AD sum
Power = P(stat > normal-data p95 at that n), i.e. the cycle 75 gate calibrated
per n on normal data, evaluated on t(3). Rule 2: post-cap share of the largest
|draw| term in the top 1% of t(3) sims and the fraction of samples where the
cap bound was hit.
"""
import math, random, csv

SEED, SIMS, NS = 83002, 4000, (25, 50, 100)
SHARES = (0.50, 0.25)

def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def draw(rng, law, n):
    if law == "t3":
        return [rng.gauss(0, 1) / math.sqrt(rng.gammavariate(1.5, 2 / 3)) for _ in range(n)]
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

def winsorize(xs):
    a = sorted(range(len(xs)), key=lambda i: -abs(xs[i]))
    big, second = a[0], a[1]
    ys = list(xs)
    hit = abs(xs[big]) > abs(xs[second])
    ys[big] = math.copysign(abs(xs[second]), xs[big])
    return ys, hit

def capped(terms, c):
    s, mx = sum(terms), max(terms)
    if mx <= c * s:
        return s, mx / s, False
    rest = s - mx
    newmx = c * rest / (1 - c)      # so newmx == c * (rest + newmx)
    return rest + newmx, c, True

def stats(xs):
    n = len(xs)
    k = n ** -0.5
    t = terms_of(xs)
    s = sum(t)
    rec = {"uncapped": (s * k, max(t) / s, False)}
    ys, hit = winsorize(xs)
    tw = terms_of(ys)
    sw = sum(tw)
    rec["winsor"] = (sw * k, max(tw) / sw, hit)
    for c in SHARES:
        sc, sh, h = capped(t, c)
        rec["share%d" % int(c * 100)] = (sc * k, sh, h)
    return rec

def pct(v, p):
    v = sorted(v)
    return v[max(0, min(len(v) - 1, math.ceil(p * len(v)) - 1))]

VERS = ("uncapped", "winsor") + tuple("share%d" % int(c * 100) for c in SHARES)
rows, crit = [], {}
for law in ("normal", "t3"):
    for n in NS:
        rng = random.Random(SEED * 100 + n + (0 if law == "t3" else 1))
        recs = [stats(draw(rng, law, n)) for _ in range(SIMS)]
        for ver in VERS:
            st = [r[ver][0] for r in recs]
            top = sorted(recs, key=lambda r: -r[ver][0])[: SIMS // 100]
            share = sum(r[ver][1] for r in top) / len(top)
            hitfrac = sum(1 for r in recs if r[ver][2]) / SIMS
            mean = sum(st) / SIMS
            var = sum((x - mean) ** 2 for x in st) / (SIMS - 1)
            if law == "normal":
                crit[(ver, n)] = pct(st, .95)
            power = sum(1 for x in st if x > crit[(ver, n)]) / SIMS
            rows.append(dict(law=law, n=n, version=ver, seed=SEED, sims=SIMS,
                cap_rule=("none" if ver == "uncapped" else
                          "winsor q=%.3f" % (1 - 1 / n) if ver == "winsor" else
                          "share<=%.2f" % (int(ver[5:]) / 100)),
                mean=mean, var=var, var_over_mean2=var / mean ** 2,
                p90=pct(st, .9), p95=pct(st, .95), p99=pct(st, .99),
                crit_normal_p95=crit[(ver, n)], power=power,
                top1_largest_share=share, cap_hit_frac=hitfrac))
with open("stuff/cap-single-draw-check.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def g(x):
    return ("%.4g" % x) if abs(x) < 1e4 else ("%.3e" % x)
for law in ("t3", "normal"):
    print("\n### %s (rule 1)\n" % law)
    print("| n | variant | cap rule | mean | variance | var/mean^2 | p90 | p95 | p99 | power |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        if r["law"] == law:
            print("| %d | %s | %s | %s | %s | %s | %s | %s | %s | %.3f |" % (r["n"], r["version"], r["cap_rule"],
                g(r["mean"]), g(r["var"]), g(r["var_over_mean2"]), g(r["p90"]), g(r["p95"]), g(r["p99"]), r["power"]))
print("\n### Power difference, capped minus uncapped (rule 1)\n")
print("| n | " + " | ".join(VERS[1:]) + " |"); print("|---|" + "---|" * len(VERS[1:]))
for n in NS:
    base = [r for r in rows if r["law"] == "t3" and r["n"] == n and r["version"] == "uncapped"][0]["power"]
    print("| %d | " % n + " | ".join("%+.3f" % ([r for r in rows if r["law"] == "t3" and r["n"] == n and r["version"] == v][0]["power"] - base) for v in VERS[1:]) + " |")
print("\n### Rule 2: top-1% largest-draw share of the AD sum and cap-hit fraction, t(3)\n")
print("| n | variant | post-cap top1% share | uncapped cycle 82 share | cap hit fraction |"); print("|---|---|---|---|---|")
for r in rows:
    if r["law"] == "t3" and r["n"] in (25, 50):
        print("| %d | %s | %.3f | 1.00 | %.3f |" % (r["n"], r["version"], r["top1_largest_share"], r["cap_hit_frac"]))
