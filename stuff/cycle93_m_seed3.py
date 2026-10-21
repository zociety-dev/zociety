# Cycle 93, stuff 2 (member-3): replicate M vs AD, SW, S2 under a new seed; check exact-5% calibration
# out of sample and the paired SE formula. 20000 sims per n.
import numpy as np, time
from scipy import stats
from scipy.special import log_ndtr
SEED = 93403; N_SIMS = 20000; NS = [25, 50, 100]
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
    l = -w8 * log_ndtr(z)                 # l_i = -((2i-1)/n) ln Phi(z_(i))
    u = -w8 * log_ndtr(-z[:, ::-1])       # u_i = -((2i-1)/n) ln(1 - Phi(z_(n+1-i)))
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
def discordant_se(rx, ry):
    # closed form for the SE of a difference of paired proportions: sqrt((p10 + p01 - (p10 - p01)^2) / N)
    p10 = (rx & ~ry).mean(); p01 = (~rx & ry).mean()
    return np.sqrt((p10 + p01 - (p10 - p01) ** 2) / len(rx))
def unpaired_se(rx, ry):
    p, q, N = rx.mean(), ry.mean(), len(rx)
    return np.sqrt(p * (1 - p) / N + q * (1 - q) / N)
def verdict(gap, se):
    return "beats" if gap > 2 * se else ("loses" if gap < -2 * se else "tie")
rng = np.random.default_rng(SEED)
t0 = time.time()
cal, oos, rows, sechk = [], [], [], []
chi_ok, side_ok = True, True
for n in NS:
    mn, an, wn, sn = score(draw("normal", n, rng))
    cm, ca, cw, cs = np.quantile(mn, 0.95), np.quantile(an, 0.95), np.quantile(wn, 0.05), np.quantile(sn, 0.95)
    cal.append((n, cm, (mn > cm).mean(), ca, (an > ca).mean(), cw, (wn < cw).mean(), cs, (sn > cs).mean()))
    # out-of-sample size: a second, independent 20000 null draws scored at the critical values above
    m2, a2, w2, s2 = score(draw("normal", n, rng))
    oos.append((n, (m2 > cm).mean(), (a2 > ca).mean(), (w2 < cw).mean(), (s2 > cs).mean()))
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
        sechk.append((n, law, sa, discordant_se(rm, ra), unpaired_se(rm, ra), ss, discordant_se(rm, rs), unpaired_se(rm, rs)))
print(f"WALL {time.time()-t0:.0f} s")
print("| n | M 5% crit | M null rate | A2 5% crit | A2 null rate | W 5% crit | W null rate | S2 5% crit | S2 null rate |")
print("|---|---|---|---|---|---|---|---|---|")
for c in cal:
    print("| %d | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f |" % c)
print()
print("| n | M oos size | A2 oos size | W oos size | S2 oos size |")
print("|---|---|---|---|---|")
for o in oos:
    print("| %d | %.4f | %.4f | %.4f | %.4f |" % o)
print()
print("| n | law | M | A2 | W | S2 | M-A2 (SE) | vs AD | M-W (SE) | vs SW | M-S2 (SE) | within 2 SE of S2? |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    print("| %d | %s | %.4f | %.4f | %.4f | %.4f | %+.4f (%.4f) | %s | %+.4f (%.4f) | %s | %+.4f (%.4f) | %s |" % r)
print()
print("| n | law | M-A2 paired SE (indicator sd) | closed form | unpaired SE | M-S2 paired SE | closed form | unpaired SE |")
print("|---|---|---|---|---|---|---|---|")
for s in sechk:
    print("| %d | %s | %.5f | %.5f | %.5f | %.5f | %.5f | %.5f |" % s)
print()
print(f"CHI_OK={chi_ok} SIDE_OK={side_ok}")
