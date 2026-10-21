# Cycle 86: c window on the uncentered gate, with top-term share (member-1)

Seed 86101, 20000 sims per n, 20 batches of 1000 for Monte Carlo standard errors (batch sd / sqrt(20); power-loss SE is the paired batch SE). Level 5%, critical value from the normal sims at the same n and c. Harness: `uv run --with numpy --with scipy python -I cwin1.py` (script at the bottom, about 2 s).

**Gate definition, a third centering.** Same nonnegative terms as member-3: sample standardized by its own mean and sd (ddof=1), z sorted, F = Phi(z), w_i = (2i-1)/n * (-ln F_(i) - ln(1-F_(n+1-i))), sum = A^2 + n. The capped gate sums log(1+c w_i)/c. Here var/mean^2 is the **statistic-level** ratio var(S)/mean(S)^2 of the uncentered gate S = sum g(w_i), which has a positive mean near n+1, so it has neither member-2's negative-mean offset artifact nor member-3's per-term pooling. It is reported x1000 because the ratio is tiny. Alongside it is the **top-term share** mean(max_i g(w_i) / S), the dominance measure cycle 85 called "share". Power loss = uncapped power - capped power; negative means the cap gains power.

**Answer to rule 2: c = 20**, reading "power within 0.02" as "loses at most 0.02". The variance half is vacuous on this definition: var/mean^2 is below 0.001 at every (c, n, law), and the k=0 gate is already below 0.001, because the gate carries a deterministic offset of about n that dwarfs its spread. The top-term share tells the real dispersion story: k=0 sits at 0.063/0.031/0.015 at n=25/50/100 and every c in 20..40 cuts it to 0.047/0.023/0.012, flat in c to three decimals. Under the loses-at-most-0.02 reading every c passes at every n (the largest loss is +0.009 at c=40, n=25, three SE from zero), so the smallest is c=20. Read two-sided, none passes: c=20 gains 0.016/0.072/0.054 t(3) power at n=25/50/100, and even c=40 gains 0.036 and 0.025 at n=50 and 100.

**At c = 20, t(5) and contaminated normal, k = 0 baseline in the same table.** Both halves hold per law under the loses-at-most reading: var/mean^2 stays below 0.001, the top-term share drops from 0.060/0.030/0.015 to 0.047/0.023/0.012, and the cap gains power by 0.037/0.109/0.163 for t(5) and 0.060/0.159/0.173 for cn at n=25/50/100, with SEs of 0.002-0.003.

| law | n | c | var/mean^2 x1000 (SE) | top-term share (SE) | power (SE) | loss vs k=0 (SE) | both halves |
|---|---|---|---|---|---|---|---|
| t5 | 25 | 0 | 0.238 (0.007) | 0.060 (0.000) | 0.201 (0.003) | baseline | yes |
| t5 | 25 | 20 | 0.097 (0.001) | 0.047 (0.000) | 0.238 (0.003) | -0.037 (0.002) | yes |
| t5 | 50 | 0 | 0.114 (0.004) | 0.030 (0.000) | 0.303 (0.003) | baseline | yes |
| t5 | 50 | 20 | 0.062 (0.001) | 0.023 (0.000) | 0.412 (0.003) | -0.109 (0.003) | yes |
| t5 | 100 | 0 | 0.058 (0.003) | 0.015 (0.000) | 0.480 (0.004) | baseline | yes |
| t5 | 100 | 20 | 0.038 (0.000) | 0.012 (0.000) | 0.643 (0.003) | -0.163 (0.003) | yes |
| cn | 25 | 0 | 0.341 (0.006) | 0.060 (0.000) | 0.304 (0.003) | baseline | yes |
| cn | 25 | 20 | 0.142 (0.001) | 0.047 (0.000) | 0.364 (0.003) | -0.060 (0.003) | yes |
| cn | 50 | 0 | 0.163 (0.003) | 0.029 (0.000) | 0.454 (0.004) | baseline | yes |
| cn | 50 | 20 | 0.086 (0.001) | 0.023 (0.000) | 0.613 (0.003) | -0.159 (0.003) | yes |
| cn | 100 | 0 | 0.077 (0.001) | 0.014 (0.000) | 0.680 (0.003) | baseline | yes |
| cn | 100 | 20 | 0.046 (0.000) | 0.012 (0.000) | 0.853 (0.003) | -0.173 (0.002) | yes |

cn = 0.9 N(0,1) + 0.1 N(0,9).

**What this adds.** Three centerings (member-2 statistic-level centered, member-3 per-term, this one statistic-level uncentered) and three seeds now agree on the same numbers to within SE: the power effect of the cap is a gain on every heavy-tailed law, monotone in n and shrinking in c, and the t(5) and cn gains at c=20 match member-3's to 0.005. The variance half is not a discriminating criterion under any centering: it is met by k=0 in all three, and here it is met by three orders of magnitude. The top-term share is the one dispersion number that moves, and it is flat across c in 20..40, so the window pins nothing; what c trades is only the size of the power gain. Cycle 85's "c trades the halves" does not survive a change of seed, law, or centering. The open question is the one member-3 named: whether the gain reverses under shift or skew alternatives, where the capped tail terms are the ones carrying the signal.

## Full sweep (rule 1): one row per (c, n, law), normal and t(3), plus t(5) and cn

| law | n | c | var/mean^2 x1000 (SE) | top-term share (SE) | power (SE) | loss vs k=0 (SE) |
|---|---|---|---|---|---|---|
| normal | 25 | 0 | 0.052 (0.001) | 0.063 (0.000) | 0.050 (0.002) | +0.000 (0.000) |
| normal | 25 | 20 | 0.026 (0.000) | 0.048 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 25 | 25 | 0.024 (0.000) | 0.047 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 25 | 30 | 0.022 (0.000) | 0.047 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 25 | 35 | 0.021 (0.000) | 0.047 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 25 | 40 | 0.020 (0.000) | 0.047 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| t3 | 25 | 0 | 0.841 (0.021) | 0.059 (0.000) | 0.387 (0.003) | +0.000 (0.000) |
| t3 | 25 | 20 | 0.198 (0.003) | 0.047 (0.000) | 0.403 (0.003) | -0.016 (0.003) |
| t3 | 25 | 25 | 0.181 (0.003) | 0.046 (0.000) | 0.394 (0.003) | -0.007 (0.002) |
| t3 | 25 | 30 | 0.169 (0.002) | 0.046 (0.000) | 0.388 (0.003) | -0.000 (0.003) |
| t3 | 25 | 35 | 0.160 (0.002) | 0.046 (0.000) | 0.383 (0.003) | +0.005 (0.003) |
| t3 | 25 | 40 | 0.152 (0.002) | 0.046 (0.000) | 0.378 (0.003) | +0.009 (0.003) |
| t5 | 25 | 0 | 0.238 (0.007) | 0.060 (0.000) | 0.201 (0.003) | +0.000 (0.000) |
| t5 | 25 | 20 | 0.097 (0.001) | 0.047 (0.000) | 0.238 (0.003) | -0.037 (0.002) |
| t5 | 25 | 25 | 0.089 (0.001) | 0.047 (0.000) | 0.234 (0.003) | -0.033 (0.002) |
| t5 | 25 | 30 | 0.083 (0.001) | 0.046 (0.000) | 0.230 (0.003) | -0.029 (0.002) |
| t5 | 25 | 35 | 0.078 (0.001) | 0.046 (0.000) | 0.228 (0.003) | -0.027 (0.002) |
| t5 | 25 | 40 | 0.074 (0.001) | 0.046 (0.000) | 0.227 (0.003) | -0.025 (0.002) |
| cn | 25 | 0 | 0.341 (0.006) | 0.060 (0.000) | 0.304 (0.003) | +0.000 (0.000) |
| cn | 25 | 20 | 0.142 (0.001) | 0.047 (0.000) | 0.364 (0.003) | -0.060 (0.003) |
| cn | 25 | 25 | 0.130 (0.001) | 0.047 (0.000) | 0.358 (0.003) | -0.054 (0.003) |
| cn | 25 | 30 | 0.121 (0.001) | 0.046 (0.000) | 0.352 (0.003) | -0.048 (0.003) |
| cn | 25 | 35 | 0.114 (0.001) | 0.046 (0.000) | 0.347 (0.003) | -0.044 (0.003) |
| cn | 25 | 40 | 0.108 (0.001) | 0.046 (0.000) | 0.344 (0.003) | -0.041 (0.003) |
| normal | 50 | 0 | 0.014 (0.000) | 0.031 (0.000) | 0.050 (0.002) | +0.000 (0.000) |
| normal | 50 | 20 | 0.011 (0.000) | 0.024 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 50 | 25 | 0.010 (0.000) | 0.024 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 50 | 30 | 0.009 (0.000) | 0.023 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 50 | 35 | 0.008 (0.000) | 0.023 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 50 | 40 | 0.008 (0.000) | 0.023 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| t3 | 50 | 0 | 0.696 (0.019) | 0.029 (0.000) | 0.605 (0.003) | +0.000 (0.000) |
| t3 | 50 | 20 | 0.151 (0.002) | 0.023 (0.000) | 0.677 (0.003) | -0.072 (0.002) |
| t3 | 50 | 25 | 0.140 (0.002) | 0.023 (0.000) | 0.666 (0.003) | -0.061 (0.002) |
| t3 | 50 | 30 | 0.131 (0.002) | 0.023 (0.000) | 0.657 (0.003) | -0.051 (0.003) |
| t3 | 50 | 35 | 0.123 (0.002) | 0.023 (0.000) | 0.649 (0.003) | -0.043 (0.003) |
| t3 | 50 | 40 | 0.118 (0.001) | 0.023 (0.000) | 0.641 (0.003) | -0.036 (0.003) |
| t5 | 50 | 0 | 0.114 (0.004) | 0.030 (0.000) | 0.303 (0.003) | +0.000 (0.000) |
| t5 | 50 | 20 | 0.062 (0.001) | 0.023 (0.000) | 0.412 (0.003) | -0.109 (0.003) |
| t5 | 50 | 25 | 0.057 (0.001) | 0.023 (0.000) | 0.403 (0.003) | -0.100 (0.003) |
| t5 | 50 | 30 | 0.053 (0.001) | 0.023 (0.000) | 0.395 (0.003) | -0.092 (0.003) |
| t5 | 50 | 35 | 0.050 (0.001) | 0.023 (0.000) | 0.389 (0.003) | -0.086 (0.003) |
| t5 | 50 | 40 | 0.048 (0.001) | 0.023 (0.000) | 0.383 (0.003) | -0.080 (0.003) |
| cn | 50 | 0 | 0.163 (0.003) | 0.029 (0.000) | 0.454 (0.004) | +0.000 (0.000) |
| cn | 50 | 20 | 0.086 (0.001) | 0.023 (0.000) | 0.613 (0.003) | -0.159 (0.003) |
| cn | 50 | 25 | 0.079 (0.001) | 0.023 (0.000) | 0.606 (0.003) | -0.152 (0.003) |
| cn | 50 | 30 | 0.074 (0.001) | 0.023 (0.000) | 0.600 (0.003) | -0.146 (0.003) |
| cn | 50 | 35 | 0.069 (0.001) | 0.023 (0.000) | 0.595 (0.003) | -0.140 (0.003) |
| cn | 50 | 40 | 0.066 (0.001) | 0.023 (0.000) | 0.590 (0.003) | -0.136 (0.003) |
| normal | 100 | 0 | 0.004 (0.000) | 0.015 (0.000) | 0.050 (0.002) | +0.000 (0.000) |
| normal | 100 | 20 | 0.004 (0.000) | 0.012 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 100 | 25 | 0.004 (0.000) | 0.012 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 100 | 30 | 0.004 (0.000) | 0.012 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 100 | 35 | 0.003 (0.000) | 0.012 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| normal | 100 | 40 | 0.003 (0.000) | 0.012 (0.000) | 0.050 (0.002) | +0.000 (0.002) |
| t3 | 100 | 0 | 0.541 (0.020) | 0.014 (0.000) | 0.855 (0.002) | +0.000 (0.000) |
| t3 | 100 | 20 | 0.109 (0.002) | 0.012 (0.000) | 0.909 (0.002) | -0.054 (0.002) |
| t3 | 100 | 25 | 0.101 (0.002) | 0.011 (0.000) | 0.901 (0.002) | -0.046 (0.002) |
| t3 | 100 | 30 | 0.095 (0.002) | 0.011 (0.000) | 0.893 (0.002) | -0.038 (0.002) |
| t3 | 100 | 35 | 0.090 (0.001) | 0.011 (0.000) | 0.886 (0.002) | -0.032 (0.002) |
| t3 | 100 | 40 | 0.086 (0.001) | 0.011 (0.000) | 0.880 (0.002) | -0.025 (0.002) |
| t5 | 100 | 0 | 0.058 (0.003) | 0.015 (0.000) | 0.480 (0.004) | +0.000 (0.000) |
| t5 | 100 | 20 | 0.038 (0.000) | 0.012 (0.000) | 0.643 (0.003) | -0.163 (0.003) |
| t5 | 100 | 25 | 0.036 (0.000) | 0.012 (0.000) | 0.632 (0.003) | -0.152 (0.003) |
| t5 | 100 | 30 | 0.033 (0.000) | 0.012 (0.000) | 0.620 (0.003) | -0.140 (0.003) |
| t5 | 100 | 35 | 0.031 (0.000) | 0.011 (0.000) | 0.612 (0.003) | -0.131 (0.003) |
| t5 | 100 | 40 | 0.030 (0.000) | 0.011 (0.000) | 0.603 (0.003) | -0.123 (0.003) |
| cn | 100 | 0 | 0.077 (0.001) | 0.014 (0.000) | 0.680 (0.003) | +0.000 (0.000) |
| cn | 100 | 20 | 0.046 (0.000) | 0.012 (0.000) | 0.853 (0.003) | -0.173 (0.002) |
| cn | 100 | 25 | 0.042 (0.000) | 0.012 (0.000) | 0.850 (0.003) | -0.169 (0.002) |
| cn | 100 | 30 | 0.040 (0.000) | 0.011 (0.000) | 0.846 (0.003) | -0.166 (0.002) |
| cn | 100 | 35 | 0.037 (0.000) | 0.011 (0.000) | 0.844 (0.003) | -0.163 (0.002) |
| cn | 100 | 40 | 0.035 (0.000) | 0.011 (0.000) | 0.841 (0.003) | -0.160 (0.002) |

## Script (cwin1.py)

```python
import numpy as np
from scipy.stats import norm
SEED=86101; SIMS=20000; B=20; CS=[20,25,30,35,40]; NS=[25,50,100]
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
def g(w,c): return w if c==0 else np.log1p(c*w)/c
def gate(w,c): return g(w,c).sum(1)
def bse(v): b=[x.mean() for x in np.array_split(v,B)]; return np.mean(b), np.std(b,ddof=1)/np.sqrt(B)
W={}
for law in ['normal','t3','t5','cn']:
    for n in NS: W[law,n]=terms(draw(law,n))
rows=[]
for n in NS:
    S0={c:gate(W['normal',n],c) for c in [0]+CS}
    crit={c:np.quantile(S0[c],0.95) for c in S0}
    for law in ['normal','t3','t5','cn']:
        for c in [0]+CS:
            G=g(W[law,n],c); S=G.sum(1)
            # statistic-level var/mean^2 of the uncentered (nonnegative) gate, batch SE
            r=[(sb.var()/sb.mean()**2) for sb in np.array_split(S,B)]; d,dse=np.mean(r),np.std(r,ddof=1)/np.sqrt(B)
            sh,shse=bse(G.max(1)/S)   # top-term share of the gate
            rej=(S>crit[c]).astype(float); rej0=(gate(W[law,n],0)>crit[0]).astype(float)
            pb=np.array([x.mean() for x in np.array_split(rej,B)]); p0b=np.array([x.mean() for x in np.array_split(rej0,B)])
            loss=p0b.mean()-pb.mean(); lse=np.std(p0b-pb,ddof=1)/np.sqrt(B)
            rows.append((law,n,c,d,dse,sh,shse,rej.mean(),np.sqrt(rej.mean()*(1-rej.mean())/SIMS),loss,lse))
print("| law | n | c | var/mean^2 x1000 (SE) | top-term share (SE) | power (SE) | loss vs k=0 (SE) |"); print("|---|---|---|---|---|---|---|")
for r in rows: print(f"| {r[0]} | {r[1]} | {r[2]} | {1000*r[3]:.3f} ({1000*r[4]:.3f}) | {r[5]:.3f} ({r[6]:.3f}) | {r[7]:.3f} ({r[8]:.3f}) | {r[9]:+.3f} ({r[10]:.3f}) |")
```
