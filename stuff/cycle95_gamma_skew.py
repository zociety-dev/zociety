# Cycle 95: how does the SW margin over plain S2 scale with gamma skewness?
# Exact 5% size at n=50, 20000 paired draws per shape, shapes 1, 2, 5, 10, 20, 50.
# Seed 95201. Critical values from one 20000-draw N(0,1) run; null rate checked on a
# separate 20000-draw N(0,1) run (rule 2). sqrt(beta1) = 2/sqrt(shape) (rule 1).
import numpy as np, time
from scipy import stats
from scipy.special import log_ndtr
SEED = 95201; N_SIMS = 20000; N = 50
SHAPES = [1, 2, 5, 10, 20, 50]
def score(x):
    n = x.shape[1]
    z = np.sort((x - x.mean(1, keepdims=True)) / x.std(1, ddof=1, keepdims=True), axis=1)
    w8 = (2 * np.arange(1, n + 1) - 1) / n
    t = -w8 * log_ndtr(z) - w8 * log_ndtr(-z[:, ::-1])   # plain AD terms t_i = l_i + u_i
    s2 = np.log1p(2 * t).sum(1) / 2                      # plain S2 (c=2), reject large
    w = np.array([stats.shapiro(r)[0] for r in x])       # Shapiro-Wilk, reject small
    return w, s2
def paired_se(rx, ry):
    d = rx.astype(float) - ry.astype(float)
    return d.std(ddof=1) / np.sqrt(len(d))
rng = np.random.default_rng(SEED)
t0 = time.time()
# calibration run: exact-size 5% critical values
wn, sn = score(rng.standard_normal((N_SIMS, N)))
cw, cs = np.quantile(wn, 0.05), np.quantile(sn, 0.95)
# separate null check run at the stated critical values
wn2, sn2 = score(rng.standard_normal((N_SIMS, N)))
null_w, null_s = (wn2 < cw).mean(), (sn2 > cs).mean()
rows = []
for k in SHAPES:
    w, s = score(rng.gamma(k, 1.0, (N_SIMS, N)))
    rw, rs = w < cw, s > cs
    gap, se = rw.mean() - rs.mean(), paired_se(rw, rs)
    rows.append((k, 2 / np.sqrt(k), rw.mean(), rs.mean(), gap, se, gap / se, gap > 2 * se))
print(f"WALL {time.time()-t0:.0f} s  SEED {SEED}  N_SIMS {N_SIMS}  n {N}")
print(f"CRIT W_5pct={cw:.5f} (calibration rate {(wn < cw).mean():.4f})  S2_5pct={cs:.5f} (calibration rate {(sn > cs).mean():.4f})")
print(f"NULL_CHECK separate 20000 N(0,1): SW rate {null_w:.4f}  S2 rate {null_s:.4f}")
print()
print("| shape | sqrt(beta1) | SW power | S2 power | SW-S2 | paired SE | gap/SE | beats >2SE |")
print("|---|---|---|---|---|---|---|---|")
for r in rows:
    print("| %d | %.4f | %.4f | %.4f | %+.4f | %.4f | %+.1f | %s |" % r)
print()
# ordering check: shapes listed by decreasing sqrt(beta1); margin monotone means it never rises
gaps = [r[4] for r in rows]
inv = sum(1 for i in range(len(gaps) - 1) if gaps[i + 1] > gaps[i])
print(f"ADJACENT_INVERSIONS {inv} (0 means margin monotone decreasing in sqrt(beta1))")
wins = [r for r in rows if r[7]]
if wins:
    k, sb, _, _, gap, se, _, _ = wins[-1]
    print(f"LARGEST_SHAPE_WIN shape={k} sqrt(beta1)={sb:.4f} margin={gap:+.4f} SE={se:.4f}")
else:
    print("LARGEST_SHAPE_WIN none")
