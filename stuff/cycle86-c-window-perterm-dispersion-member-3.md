# Cycle 86: c window with a per-term dispersion measure (member-3)

Seed 86031, 20000 sims per n, 20 batches of 1000 for Monte Carlo standard errors (batch sd / sqrt(20); power-loss SE is the paired batch SE). Level 5%, critical value from the normal sims at the same n and c. Harness: `uv run --with numpy --with scipy python -I cwin3.py` (script at the bottom, runs in about 2 s).

**Gate definition, chosen to avoid the offset artifact member-2 found.** Sample standardized by its own mean and sd (ddof=1), z sorted, F = Phi(z). Per-term contribution w_i = (2i-1)/n * (-ln F_(i) - ln(1-F_(n+1-i))), which is nonnegative and sums to A^2 + n. The capped gate sums log(1+c w_i)/c over every term (k=0 is the plain sum). var/mean^2 is the **per-term dispersion** var(g(w_i))/mean(g(w_i))^2 pooled over all terms and sims, i.e. the dominance measure cycle 85 was actually after, not the ratio of the statistic's variance to its squared (possibly negative) mean. Power loss = uncapped power - capped power; negative means the cap gains power.

**Answer to rule 2: c = 20, with a caveat on what "within 0.02" means.** Under this definition every c in 20..40 gives var/mean^2 between 0.03 and 0.05 at every n and law, far below 2/3. The uncapped k=0 gate already sits at 0.14-0.19, so the variance half is met before any cap is applied; the cap cuts dispersion by about 4x but was never needed for the 2/3 bar. Reading "power within 0.02" as "loses at most 0.02", every c passes at every n (all losses are at most +0.003, which is within one SE of zero) and the smallest is c = 20. Reading it two-sided, **none** passes: c = 20 gains 0.024 at n = 25 and 0.06 at n = 50 and 100 against t(3), and c = 40 still gains 0.02-0.03 at n = 50 and 100.

**At c = 20, t(5) and contaminated normal, k = 0 baseline in the same table.** Both halves hold per law: dispersion 0.04-0.05 against 0.15-0.17 uncapped, and power is never lost, it is gained, by 0.04/0.10/0.16 for t(5) and 0.06/0.15/0.17 for the contaminated normal at n = 25/50/100. The gain grows with n for every non-normal law, which is the same direction member-2 found with the centered definition, so the sign of the cap's power effect does not depend on the centering.

| law | n | c | var/mean^2 (SE) | power (SE) | loss vs k=0 (SE) | both halves |
|---|---|---|---|---|---|---|
| t5 | 25 | 0 | 0.166 (0.000) | 0.194 (0.003) | baseline | yes |
| t5 | 25 | 20 | 0.040 (0.000) | 0.230 (0.003) | -0.036 (0.002) | yes |
| t5 | 50 | 0 | 0.160 (0.000) | 0.308 (0.003) | baseline | yes |
| t5 | 50 | 20 | 0.043 (0.000) | 0.412 (0.003) | -0.104 (0.003) | yes |
| t5 | 100 | 0 | 0.157 (0.000) | 0.483 (0.004) | baseline | yes |
| t5 | 100 | 20 | 0.045 (0.000) | 0.643 (0.003) | -0.160 (0.002) | yes |
| cn | 25 | 0 | 0.160 (0.000) | 0.301 (0.003) | baseline | yes |
| cn | 25 | 20 | 0.038 (0.000) | 0.359 (0.003) | -0.058 (0.003) | yes |
| cn | 50 | 0 | 0.153 (0.000) | 0.460 (0.004) | baseline | yes |
| cn | 50 | 20 | 0.040 (0.000) | 0.606 (0.003) | -0.146 (0.003) | yes |
| cn | 100 | 0 | 0.148 (0.000) | 0.681 (0.003) | baseline | yes |
| cn | 100 | 20 | 0.041 (0.000) | 0.852 (0.003) | -0.170 (0.002) | yes |

cn = 0.9 N(0,1) + 0.1 N(0,9).

**What this means for the direction.** Two different centerings now agree that the log(1+ct)/c cap is a power device, not a dispersion device: it gains tail power against every heavy-tailed law tried and the gain grows with n. The 2/3 variance bar is met by k=0 under both definitions, so cycle 85's "c trades the halves" conclusion came from its specific statistic-level ratio, and the window c in 20..40 is flat on every measure here (dispersion 0.03-0.05, gains monotone in c). The next question is not c but whether the gain survives level-shift and skew alternatives, where the cap might cost power.

## Full sweep (rule 1): one row per (c, n, law), normal and t(3), plus t(5) and cn

| law | n | c | var/mean^2 (SE) | power (SE) | loss vs k=0 (SE) |
|---|---|---|---|---|---|
| normal | 25 | 0 | 0.189 (0.000) | 0.050 (0.002) | +0.000 (0.000) |
| normal | 25 | 20 | 0.042 (0.000) | 0.050 (0.002) | -0.000 (0.002) |
| normal | 25 | 25 | 0.038 (0.000) | 0.050 (0.002) | -0.000 (0.002) |
| normal | 25 | 30 | 0.035 (0.000) | 0.050 (0.002) | -0.000 (0.001) |
| normal | 25 | 35 | 0.033 (0.000) | 0.050 (0.002) | -0.000 (0.001) |
| normal | 25 | 40 | 0.031 (0.000) | 0.050 (0.002) | -0.000 (0.001) |
| t3 | 25 | 0 | 0.154 (0.000) | 0.380 (0.003) | +0.000 (0.000) |
| t3 | 25 | 20 | 0.038 (0.000) | 0.404 (0.003) | -0.024 (0.003) |
| t3 | 25 | 25 | 0.035 (0.000) | 0.395 (0.003) | -0.016 (0.003) |
| t3 | 25 | 30 | 0.033 (0.000) | 0.386 (0.003) | -0.007 (0.003) |
| t3 | 25 | 35 | 0.031 (0.000) | 0.381 (0.003) | -0.001 (0.003) |
| t3 | 25 | 40 | 0.029 (0.000) | 0.377 (0.003) | +0.003 (0.003) |
| t5 | 25 | 0 | 0.166 (0.000) | 0.194 (0.003) | +0.000 (0.000) |
| t5 | 25 | 20 | 0.040 (0.000) | 0.230 (0.003) | -0.036 (0.002) |
| t5 | 25 | 25 | 0.036 (0.000) | 0.225 (0.003) | -0.031 (0.002) |
| t5 | 25 | 30 | 0.034 (0.000) | 0.221 (0.003) | -0.027 (0.002) |
| t5 | 25 | 35 | 0.032 (0.000) | 0.217 (0.003) | -0.023 (0.002) |
| t5 | 25 | 40 | 0.030 (0.000) | 0.216 (0.003) | -0.022 (0.002) |
| cn | 25 | 0 | 0.160 (0.000) | 0.301 (0.003) | +0.000 (0.000) |
| cn | 25 | 20 | 0.038 (0.000) | 0.359 (0.003) | -0.058 (0.003) |
| cn | 25 | 25 | 0.034 (0.000) | 0.353 (0.003) | -0.052 (0.003) |
| cn | 25 | 30 | 0.032 (0.000) | 0.348 (0.003) | -0.046 (0.003) |
| cn | 25 | 35 | 0.030 (0.000) | 0.343 (0.003) | -0.041 (0.003) |
| cn | 25 | 40 | 0.029 (0.000) | 0.339 (0.003) | -0.038 (0.004) |
| normal | 50 | 0 | 0.188 (0.000) | 0.050 (0.002) | +0.000 (0.000) |
| normal | 50 | 20 | 0.046 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 50 | 25 | 0.042 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 50 | 30 | 0.039 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 50 | 35 | 0.036 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 50 | 40 | 0.035 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| t3 | 50 | 0 | 0.147 (0.000) | 0.616 (0.003) | +0.000 (0.000) |
| t3 | 50 | 20 | 0.040 (0.000) | 0.676 (0.003) | -0.059 (0.003) |
| t3 | 50 | 25 | 0.037 (0.000) | 0.664 (0.003) | -0.048 (0.003) |
| t3 | 50 | 30 | 0.035 (0.000) | 0.654 (0.003) | -0.037 (0.003) |
| t3 | 50 | 35 | 0.033 (0.000) | 0.644 (0.003) | -0.028 (0.003) |
| t3 | 50 | 40 | 0.032 (0.000) | 0.637 (0.003) | -0.020 (0.003) |
| t5 | 50 | 0 | 0.160 (0.000) | 0.308 (0.003) | +0.000 (0.000) |
| t5 | 50 | 20 | 0.043 (0.000) | 0.412 (0.003) | -0.104 (0.003) |
| t5 | 50 | 25 | 0.040 (0.000) | 0.402 (0.003) | -0.094 (0.003) |
| t5 | 50 | 30 | 0.037 (0.000) | 0.393 (0.003) | -0.085 (0.003) |
| t5 | 50 | 35 | 0.035 (0.000) | 0.385 (0.003) | -0.077 (0.002) |
| t5 | 50 | 40 | 0.033 (0.000) | 0.379 (0.003) | -0.071 (0.003) |
| cn | 50 | 0 | 0.153 (0.000) | 0.460 (0.004) | +0.000 (0.000) |
| cn | 50 | 20 | 0.040 (0.000) | 0.606 (0.003) | -0.146 (0.003) |
| cn | 50 | 25 | 0.037 (0.000) | 0.600 (0.003) | -0.140 (0.003) |
| cn | 50 | 30 | 0.035 (0.000) | 0.594 (0.003) | -0.133 (0.003) |
| cn | 50 | 35 | 0.033 (0.000) | 0.588 (0.003) | -0.127 (0.003) |
| cn | 50 | 40 | 0.031 (0.000) | 0.583 (0.003) | -0.123 (0.003) |
| normal | 100 | 0 | 0.187 (0.000) | 0.050 (0.002) | +0.000 (0.000) |
| normal | 100 | 20 | 0.048 (0.000) | 0.050 (0.002) | +0.000 (0.001) |
| normal | 100 | 25 | 0.044 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 100 | 30 | 0.041 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 100 | 35 | 0.039 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 100 | 40 | 0.037 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| t3 | 100 | 0 | 0.142 (0.000) | 0.851 (0.003) | +0.000 (0.000) |
| t3 | 100 | 20 | 0.041 (0.000) | 0.907 (0.002) | -0.056 (0.002) |
| t3 | 100 | 25 | 0.038 (0.000) | 0.900 (0.002) | -0.049 (0.002) |
| t3 | 100 | 30 | 0.036 (0.000) | 0.894 (0.002) | -0.043 (0.002) |
| t3 | 100 | 35 | 0.034 (0.000) | 0.888 (0.002) | -0.037 (0.002) |
| t3 | 100 | 40 | 0.033 (0.000) | 0.883 (0.002) | -0.032 (0.002) |
| t5 | 100 | 0 | 0.157 (0.000) | 0.483 (0.004) | +0.000 (0.000) |
| t5 | 100 | 20 | 0.045 (0.000) | 0.643 (0.003) | -0.160 (0.002) |
| t5 | 100 | 25 | 0.041 (0.000) | 0.631 (0.003) | -0.148 (0.002) |
| t5 | 100 | 30 | 0.039 (0.000) | 0.621 (0.003) | -0.138 (0.002) |
| t5 | 100 | 35 | 0.037 (0.000) | 0.613 (0.003) | -0.131 (0.002) |
| t5 | 100 | 40 | 0.035 (0.000) | 0.604 (0.003) | -0.121 (0.002) |
| cn | 100 | 0 | 0.148 (0.000) | 0.681 (0.003) | +0.000 (0.000) |
| cn | 100 | 20 | 0.041 (0.000) | 0.852 (0.003) | -0.170 (0.002) |
| cn | 100 | 25 | 0.038 (0.000) | 0.848 (0.003) | -0.166 (0.002) |
| cn | 100 | 30 | 0.036 (0.000) | 0.845 (0.003) | -0.164 (0.002) |
| cn | 100 | 35 | 0.034 (0.000) | 0.842 (0.003) | -0.161 (0.002) |
| cn | 100 | 40 | 0.033 (0.000) | 0.837 (0.003) | -0.156 (0.002) |

## Script (cwin3.py)

```python
import numpy as np
from scipy.stats import norm, t as tdist
SEED=86031; SIMS=20000; B=20; CS=[20,25,30,35,40]; NS=[25,50,100]
rng=np.random.default_rng(SEED)
def draw(law,n):
    if law=='normal': return rng.standard_normal((SIMS,n))
    if law=='t3': return rng.standard_t(3,(SIMS,n))
    if law=='t5': return rng.standard_t(5,(SIMS,n))
    m=rng.random((SIMS,n))<0.1; x=rng.standard_normal((SIMS,n)); x[m]*=3; return x
def terms(x):
    n=x.shape[1]; z=(x-x.mean(1,keepdims=True))/x.std(1,ddof=1,keepdims=True); z.sort(1)
    F=np.clip(norm.cdf(z),1e-300,1-1e-16); i=np.arange(1,n+1)
    return (2*i-1)/n*(-np.log(F)-np.log(1-F[:,::-1]))   # w_i >= 0, sum = A^2 + n
def gate(w,c): return (w if c==0 else np.log1p(c*w)/c).sum(1)
def disp(w,c):  # per-term dispersion var/mean^2, pooled over terms and sims, batch SE
    g=w if c==0 else np.log1p(c*w)/c
    r=[(gb.var()/gb.mean()**2) for gb in np.array_split(g,B)]
    return np.mean(r), np.std(r,ddof=1)/np.sqrt(B)
W={};
for law in ['normal','t3','t5','cn']:
    for n in NS: W[law,n]=terms(draw(law,n))
rows=[]
for n in NS:
    S0={c:gate(W['normal',n],c) for c in [0]+CS}
    crit={c:np.quantile(S0[c],0.95) for c in S0}
    for law in ['normal','t3','t5','cn']:
        for c in [0]+CS:
            d,dse=disp(W[law,n],c)
            S=gate(W[law,n],c); rej=(S>crit[c]).astype(float)
            rej0=(gate(W[law,n],0)>crit[0]).astype(float)
            pb=[r.mean() for r in np.array_split(rej,B)]; p0b=[r.mean() for r in np.array_split(rej0,B)]
            loss=np.mean(p0b)-np.mean(pb); lse=np.std(np.array(p0b)-np.array(pb),ddof=1)/np.sqrt(B)
            rows.append((law,n,c,d,dse,rej.mean(),np.sqrt(rej.mean()*(1-rej.mean())/SIMS),loss,lse))
print("| law | n | c | var/mean^2 (SE) | power (SE) | loss vs k=0 (SE) |"); print("|---|---|---|---|---|---|")
for r in rows: print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]:.3f} ({r[4]:.3f}) | {r[5]:.3f} ({r[6]:.3f}) | {r[7]:+.3f} ({r[8]:.3f}) |")
```
