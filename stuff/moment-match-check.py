#!/usr/bin/env python3
"""Can ANY ncx2(3, lambda), at ANY scale, match the cycle 75 moments?

Member-2 rescaled the draws by the null p95 and member-3 used scale-free
ratios. This check asks the direction's question the other way round: take
the empirical mean and variance of the raw cycle 75 alternative draws and
solve for the ncx2(3, lambda) and scale factor c that reproduce them.

For c * ncx2(3, lambda):  mean = c(3+lambda),  var = c^2 * 2(3+2 lambda).
So var/mean^2 = 2(3+2 lambda)/(3+lambda)^2, a scale-free number that is 2/3
at lambda=0 and decreases monotonically to 0. If the empirical var/mean^2
exceeds 2/3 there is no lambda >= 0 and no c that match both moments.
If it is below 2/3, the implied lambda is reported and compared with cycle
80's fitted lambda (4.018 at n=25, 7.154 at n=50), and the moment-matched
ncx2's p90/p95/p99 are compared with the empirical ones (rule 2).

Inputs: c75-df3-draws.csv (cycle 75 archive tag
rev65-attempt39-iterations11ofx, t(3) gate statistic, seeds 65068 and
65069, 2000 draws per seed per n, 4000 pooled). Moments are reported
pooled and per seed, plus a bootstrap interval for the variance (BOOT
resamples, seed BOOT_SEED), so moment stability can be audited.
Usage: python3 -I stuff/moment-match-check.py > stuff/moment-match-check.csv
"""
import csv, math, os, random, sys

NS = (25, 50)
LAMBDA80 = {25: 4.018, 50: 7.154}
BOOT, BOOT_SEED = 400, 65083
NCX2_SIMS, NCX2_SEED = 20000, 65084
HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    out = {n: {} for n in NS}
    with open(os.path.join(HERE, name)) as f:
        for r in csv.DictReader(f):
            n = int(r["n"])
            if n in out:
                out[n].setdefault(r["seed"], []).append(float(r["stat"]))
    return out


def pct(vals, p):
    v = sorted(vals)
    k = (len(v) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def mean_var(v):
    m = sum(v) / len(v)
    return m, sum((x - m) ** 2 for x in v) / (len(v) - 1)


def ratio(lam):
    return 2 * (3 + 2 * lam) / (3 + lam) ** 2


def solve_lambda(r):
    """Return lambda >= 0 with ratio(lambda) == r, or None if r >= 2/3."""
    if r >= ratio(0):
        return None
    lo, hi = 0.0, 1.0
    while ratio(hi) > r:
        hi *= 2
    for _ in range(200):
        mid = (lo + hi) / 2
        if ratio(mid) > r:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


alt = load("c75-df3-draws.csv")
boot = random.Random(BOOT_SEED)
rng = random.Random(NCX2_SEED)
w = csv.writer(sys.stdout)
w.writerow(["n", "source", "sims", "seed", "mean", "variance", "var_over_mean2",
            "ncx2_max_ratio", "implied_lambda", "implied_scale", "lambda_cycle80",
            "p90", "p95", "p99"])
for n in NS:
    seeds = sorted(alt[n])
    pooled = [x for s in seeds for x in alt[n][s]]
    groups = [(s, alt[n][s]) for s in seeds] + [("+".join(seeds), pooled)]
    for label, v in groups:
        m, var = mean_var(v)
        r = var / m ** 2
        lam = solve_lambda(r)
        c = m / (3 + lam) if lam is not None else None
        w.writerow([n, "cycle75_t3_raw", len(v), label, f"{m:.6f}", f"{var:.6e}",
                    f"{r:.3f}", f"{ratio(0):.3f}",
                    "none" if lam is None else f"{lam:.3f}",
                    "none" if c is None else f"{c:.5f}", LAMBDA80[n],
                    f"{pct(v,0.9):.6f}", f"{pct(v,0.95):.6f}", f"{pct(v,0.99):.6f}"])
    # bootstrap the pooled variance and the pooled var/mean^2
    bv, br = [], []
    for _ in range(BOOT):
        s = [boot.choice(pooled) for _ in pooled]
        bm, bvar = mean_var(s)
        bv.append(bvar)
        br.append(bvar / bm ** 2)
    w.writerow([n, "bootstrap_pooled_2.5pct", BOOT, BOOT_SEED, "", f"{pct(bv,0.025):.6e}",
                f"{pct(br,0.025):.3f}", f"{ratio(0):.3f}", "", "", LAMBDA80[n], "", "", ""])
    w.writerow([n, "bootstrap_pooled_97.5pct", BOOT, BOOT_SEED, "", f"{pct(bv,0.975):.6e}",
                f"{pct(br,0.975):.3f}", f"{ratio(0):.3f}", "", "", LAMBDA80[n], "", "", ""])
    # moment-matched ncx2 (if one exists) and cycle 80's ncx2, both on the raw scale
    m, var = mean_var(pooled)
    lam = solve_lambda(var / m ** 2)
    fits = [("ncx2_cycle80_scaled_to_mean", LAMBDA80[n], m / (3 + LAMBDA80[n]))]
    if lam is not None:
        fits.insert(0, ("ncx2_moment_matched", lam, m / (3 + lam)))
    for label, l, c in fits:
        s = math.sqrt(l)
        nc = [c * (rng.gauss(s, 1) ** 2 + rng.gauss(0, 1) ** 2 + rng.gauss(0, 1) ** 2)
              for _ in range(NCX2_SIMS)]
        mn, vn = mean_var(nc)
        w.writerow([n, label, NCX2_SIMS, NCX2_SEED, f"{mn:.6f}", f"{vn:.6e}",
                    f"{vn/mn**2:.3f}", f"{ratio(0):.3f}", f"{l:.3f}", f"{c:.5f}", LAMBDA80[n],
                    f"{pct(nc,0.9):.6f}", f"{pct(nc,0.95):.6f}", f"{pct(nc,0.99):.6f}"])
