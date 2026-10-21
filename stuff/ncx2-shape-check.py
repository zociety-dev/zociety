#!/usr/bin/env python3
"""Is the cycle 75 alternative statistic ncx2(3, lambda), or a heavier tail?

Inputs (copied verbatim from the cycle 75 archive tag
rev65-attempt39-iterations11ofx): c75-df3-draws.csv (t(3) alternative gate
statistic, seeds 65068 and 65069 pooled, 4000 draws per n) and
c75-null-draws.csv (null gate statistic, same seeds, 4000 per n).

The raw gate statistic lives on a ~0.06 scale, while the ncx2(3, lambda)
model of cycles 78-80 lives on the chi-square scale where the null p95 is
chi2_95(3) = 7.815. So the alternative draws are rescaled by
7.815 / (per-n null p95) before comparison; this is the only mapping under
which "power = P(ncx2 > 7.815)" means anything for these draws.

Fitted ncx2(3, lambda) uses cycle 80's per-n lambda: 4.018 (n=25), 7.154
(n=50). Its mean is 3 + lambda and variance 2(3 + 2 lambda) analytically;
its p90/p95/p99 come from NCX2_SIMS pure-python draws (sum of three squared
normals, one shifted by sqrt(lambda)), seed NCX2_SEED.
Usage: python3 -I stuff/ncx2-shape-check.py > stuff/ncx2-shape-check.csv
"""
import csv, math, os, random, sys

NS = (25, 50)
LAMBDA = {25: 4.018, 50: 7.154}
CHI2_95_3 = 7.815
NCX2_SIMS = 20000
NCX2_SEED = 65081
HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    out = {n: [] for n in NS}
    with open(os.path.join(HERE, name)) as f:
        for r in csv.DictReader(f):
            if int(r["n"]) in out:
                out[int(r["n"])].append(float(r["stat"]))
    return out


def pct(vals, p):
    v = sorted(vals)
    k = (len(v) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def mean_var(v):
    m = sum(v) / len(v)
    return m, sum((x - m) ** 2 for x in v) / (len(v) - 1)


null, alt = load("c75-null-draws.csv"), load("c75-df3-draws.csv")
rng = random.Random(NCX2_SEED)
w = csv.writer(sys.stdout)
w.writerow(["n", "source", "sims", "seed", "lambda", "scale", "mean", "variance",
            "p90", "p95", "p99", "power_at_7.815"])
for n in NS:
    crit = pct(null[n], 0.95)
    scale = CHI2_95_3 / crit
    a = [x * scale for x in alt[n]]
    m, v = mean_var(a)
    lam = LAMBDA[n]
    s = math.sqrt(lam)
    nc = [(rng.gauss(s, 1) ** 2 + rng.gauss(0, 1) ** 2 + rng.gauss(0, 1) ** 2)
          for _ in range(NCX2_SIMS)]
    mn, vn = mean_var(nc)
    w.writerow([n, "cycle75_t3_rescaled", len(a), "65068+65069", lam, f"{scale:.4f}",
                f"{m:.3f}", f"{v:.3f}", f"{pct(a,0.9):.3f}", f"{pct(a,0.95):.3f}",
                f"{pct(a,0.99):.3f}", f"{sum(x > CHI2_95_3 for x in a)/len(a):.4f}"])
    w.writerow([n, "ncx2_analytic", "", "", lam, "", f"{3+lam:.3f}", f"{2*(3+2*lam):.3f}",
                "", "", "", ""])
    w.writerow([n, "ncx2_simulated", NCX2_SIMS, NCX2_SEED, lam, "", f"{mn:.3f}", f"{vn:.3f}",
                f"{pct(nc,0.9):.3f}", f"{pct(nc,0.95):.3f}", f"{pct(nc,0.99):.3f}",
                f"{sum(x > CHI2_95_3 for x in nc)/len(nc):.4f}"])
