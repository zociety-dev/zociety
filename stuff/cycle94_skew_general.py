# Cycle 94: is SW's skew advantage general? SW vs plain AD vs plain S2 at exact 5% size,
# 20000 paired sims per n under chi2(2), chi2(10), lognormal(0,0.5), beta(2,5). Seed 94201.
import numpy as np, time
from scipy import stats
from scipy.special import log_ndtr
SEED = 94201; N_SIMS = 20000; NS = [25, 50, 100]
LAWS = ["chi2_2", "chi2_10", "lognormal_0_0.5", "beta_2_5"]
def draw(law, n, rng):
    if law == "normal":          return rng.standard_normal((N_SIMS, n))
    if law == "chi2_2":          return rng.chisquare(2, (N_SIMS, n))
    if law == "chi2_10":         return rng.chisquare(10, (N_SIMS, n))
    if law == "lognormal_0_0.5": return rng.lognormal(0.0, 0.5, (N_SIMS, n))
    if law == "beta_2_5":        return rng.beta(2, 5, (N_SIMS, n))
def score(x):
    n = x.shape[1]
    z = np.sort((x - x.mean(1, keepdims=True)) / x.std(1, ddof=1, keepdims=True), axis=1)
    w8 = (2 * np.arange(1, n + 1) - 1) / n
    t = -w8 * log_ndtr(z) - w8 * log_ndtr(-z[:, ::-1])   # plain AD terms t_i = l_i + u_i
    a2 = t.sum(1) - n                                    # plain AD, reject large
    s2 = np.log1p(2 * t).sum(1) / 2                      # plain S2 (c=2), reject large
    w = np.array([stats.shapiro(r)[0] for r in x])       # Shapiro-Wilk, reject small
    return w, a2, s2
def paired_se(rx, ry):
    d = rx.astype(float) - ry.astype(float)
    return d.std(ddof=1) / np.sqrt(len(d))
def verdict(gap, se):
    return "beats" if gap > 2 * se else ("loses" if gap < -2 * se else "tie")
rng = np.random.default_rng(SEED)
t0 = time.time()
cal, rows, fails = [], [], []
for n in NS:
    wn, an, sn = score(draw("normal", n, rng))
    cw, ca, cs = np.quantile(wn, 0.05), np.quantile(an, 0.95), np.quantile(sn, 0.95)
    cal.append((n, cw, (wn < cw).mean(), ca, (an > ca).mean(), cs, (sn > cs).mean()))
    for law in LAWS:
        w, a, s = score(draw(law, n, rng))
        rw, ra, rs = w < cw, a > ca, s > cs
        ga, gs = rw.mean() - ra.mean(), rw.mean() - rs.mean()
        sa, ss = paired_se(rw, ra), paired_se(rw, rs)
        va, vs = verdict(ga, sa), verdict(gs, ss)
        if va != "beats": fails.append(f"{law} n={n} SW-AD {ga:+.4f} = {ga/sa:+.1f} SE ({va})")
        if vs != "beats": fails.append(f"{law} n={n} SW-S2 {gs:+.4f} = {gs/ss:+.1f} SE ({vs})")
        rows.append((n, law, rw.mean(), ra.mean(), rs.mean(), ga, sa, va, gs, ss, vs))
print(f"WALL {time.time()-t0:.0f} s")
print("| n | W 5% crit | W null rate | A2 5% crit | A2 null rate | S2 5% crit | S2 null rate |")
print("|---|---|---|---|---|---|---|")
for c in cal:
    print("| %d | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f |" % c)
print()
print("| n | law | SW | AD | S2 | SW-AD (SE) | vs AD | SW-S2 (SE) | vs S2 |")
print("|---|---|---|---|---|---|---|---|---|")
for r in rows:
    print("| %d | %s | %.4f | %.4f | %.4f | %+.4f (%.4f) | %s | %+.4f (%.4f) | %s |" % r)
print()
print("SW_WINS_EVERY_CELL=" + ("True" if not fails else "False"))
for f in fails: print("NOT_WIN: " + f)
