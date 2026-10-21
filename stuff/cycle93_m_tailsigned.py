# Cycle 93: tail-signed S2 max (M) vs AD, SW, plain S2 at exact 5% size. 20000 sims per n.
import numpy as np, sys, time
from scipy import stats
from scipy.special import log_ndtr
SEED = 93201; N_SIMS = 20000; NS = [25, 50, 100]
LAWS = ["chi2_5", "t3", "t5", "laplace", "cont10", "cont5"]
def draw(law, n, rng):
    if law == "normal":  return rng.standard_normal((N_SIMS, n))
    if law == "chi2_5":  return rng.chisquare(5, (N_SIMS, n))
    if law == "t3":      return rng.standard_t(3, (N_SIMS, n))
    if law == "t5":      return rng.standard_t(5, (N_SIMS, n))
    if law == "laplace": return rng.laplace(size=(N_SIMS, n))
    if law == "cont10":
        m = rng.random((N_SIMS, n)) < 0.10
        return np.where(m, 3.0, 1.0) * rng.standard_normal((N_SIMS, n))
    if law == "cont5":
        m = rng.random((N_SIMS, n)) < 0.05
        return np.where(m, 5.0, 1.0) * rng.standard_normal((N_SIMS, n))
def score(x):
    n = x.shape[1]
    z = np.sort((x - x.mean(1, keepdims=True)) / x.std(1, ddof=1, keepdims=True), axis=1)
    w8 = (2 * np.arange(1, n + 1) - 1) / n
    l = -w8 * log_ndtr(z)                 # lower-tail term l_i, uses z_(i)
    u = -w8 * log_ndtr(-z[:, ::-1])       # upper-tail term u_i, uses z_(n+1-i)
    t = l + u
    s2 = np.log1p(2 * t).sum(1) / 2
    a2 = t.sum(1) - n
    s2p = np.log1p(2 * u).sum(1) / 2
    s2m = np.log1p(2 * l).sum(1) / 2
    m = np.maximum(s2p, s2m)
    w = np.array([stats.shapiro(r)[0] for r in x])
    return m, a2, w, s2
def paired_se(rx, ry):
    d = rx.astype(float) - ry.astype(float)
    return d.std(ddof=1) / np.sqrt(len(d))
def verdict(gap, se):
    return "beats" if gap > 2 * se else ("loses" if gap < -2 * se else "tie")
rng = np.random.default_rng(SEED)
t0 = time.time()
cal, rows = [], []
chi_ok, side_ok = True, True
for n in NS:
    mn, an, wn, sn = score(draw("normal", n, rng))
    cm, ca, cw, cs = np.quantile(mn, 0.95), np.quantile(an, 0.95), np.quantile(wn, 0.05), np.quantile(sn, 0.95)
    cal.append((n, cm, (mn > cm).mean(), ca, (an > ca).mean(), cw, (wn < cw).mean(), cs, (sn > cs).mean()))
    for law in LAWS:
        m, a, w, s = score(draw(law, n, rng))
        rm, ra, rw, rs = m > cm, a > ca, w < cw, s > cs
        ga, gw, gs = rm.mean() - ra.mean(), rm.mean() - rw.mean(), rm.mean() - rs.mean()
        sa, sw, ss = paired_se(rm, ra), paired_se(rm, rw), paired_se(rm, rs)
        va, vw, vs = verdict(ga, sa), verdict(gw, sw), verdict(gs, ss)
        keep = "yes" if vs == "tie" else ("no (above)" if gs > 0 else "no (below)")
        if law == "chi2_5" and (va == "loses" or vw == "loses"): chi_ok = False
        if law != "chi2_5" and vs != "tie": side_ok = False
        rows.append((n, law, rm.mean(), ra.mean(), rw.mean(), rs.mean(), ga, sa, va, gw, sw, vw, gs, ss, keep))
print(f"WALL {time.time()-t0:.0f} s")
print("| n | M 5% crit | M null rate | A2 5% crit | A2 null rate | W 5% crit | W null rate | S2 5% crit | S2 null rate |")
print("|---|---|---|---|---|---|---|---|---|")
for c in cal:
    print("| %d | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f |" % c)
print()
print("| n | law | M | A2 | W | S2 | M-A2 (SE) | vs AD | M-W (SE) | vs SW | M-S2 (SE) | within 2 SE of S2? |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    print("| %d | %s | %.4f | %.4f | %.4f | %.4f | %+.4f (%.4f) | %s | %+.4f (%.4f) | %s | %+.4f (%.4f) | %s |" % r)
print()
print(f"CHI_OK={chi_ok} SIDE_OK={side_ok}")
