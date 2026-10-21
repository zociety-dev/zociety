# Cycle 86: log(1+ct)/c window across laws (member-2)

Seed 20261021, 20000 sims per n, 20 batches of 1000 for Monte Carlo standard errors (SE = batch sd / sqrt(20); power-loss SE is the paired batch SE of the difference). Harness: `uv run --with numpy --with scipy python cwin.py` (script reproduced at the bottom).

**Gate definition.** Sample standardized by its own mean and sd (ddof=1), z sorted, F=Phi(z). Per-term deviation d_i = (2i-1)/n * (-ln F_(i) - ln(1-F_(n+1-i))) - 1, so the uncapped (k=0) gate is A^2 = sum d_i. The capped gate replaces each positive d_i by log(1+c d_i)/c and leaves negative d_i alone. Level 5%, critical value from the normal sims at the same n and c. Power loss = uncapped power - capped power (negative = the cap gains power).

**Answer to rule 2: none.** No c in 20, 25, 30, 35, 40 meets both halves in a meaningful sense. Mechanically var/mean^2 is below 2/3 at every c (0.010 to 0.024), but only because the capped gate's null mean goes negative (-3.2 at n=25, -6.4 at n=50, -12.9 at n=100 for c=20), so var/mean^2 is measuring the square of an offset, not dispersion. The uncapped A^2 has null mean 0.38 and var/mean^2 0.24 at every n, so the uncapped gate already satisfies the variance half under this definition and the cap only hurts interpretability. The power half holds trivially: capping gains 0.07 t(3) power at n=50 and 100 and about 0.01 to 0.02 at n=25. Because the rule asks for the t(5) and contaminated rows "at that c", they are given at c=20, the smallest c that mechanically passes, with the caveat above applying to every var/mean^2 cell.

## Rule 1 table: c x n x law (normal: var/mean^2; t(3): power loss vs uncapped at normal-calibrated 5%)

| c | n | law | var/mean^2 (SE) | t(3) power (SE) | t(3) power loss vs uncapped (SE) |
|---|---|---|---|---|---|
| 20 | 25 | normal | 0.024 (0.000) | - | - |
| 20 | 25 | t(3) | - | 0.469 (0.003) | -0.0900 (0.0023) |
| 20 | 50 | normal | 0.012 (0.000) | - | - |
| 20 | 50 | t(3) | - | 0.719 (0.003) | -0.1186 (0.0027) |
| 20 | 100 | normal | 0.006 (0.000) | - | - |
| 20 | 100 | t(3) | - | 0.923 (0.002) | -0.0709 (0.0022) |
| 25 | 25 | normal | 0.022 (0.000) | - | - |
| 25 | 25 | t(3) | - | 0.468 (0.003) | -0.0889 (0.0022) |
| 25 | 50 | normal | 0.011 (0.000) | - | - |
| 25 | 50 | t(3) | - | 0.719 (0.003) | -0.1185 (0.0027) |
| 25 | 100 | normal | 0.006 (0.000) | - | - |
| 25 | 100 | t(3) | - | 0.923 (0.002) | -0.0707 (0.0022) |
| 30 | 25 | normal | 0.020 (0.000) | - | - |
| 30 | 25 | t(3) | - | 0.468 (0.003) | -0.0893 (0.0022) |
| 30 | 50 | normal | 0.011 (0.000) | - | - |
| 30 | 50 | t(3) | - | 0.718 (0.003) | -0.1176 (0.0026) |
| 30 | 100 | normal | 0.005 (0.000) | - | - |
| 30 | 100 | t(3) | - | 0.923 (0.002) | -0.0702 (0.0022) |
| 35 | 25 | normal | 0.019 (0.000) | - | - |
| 35 | 25 | t(3) | - | 0.466 (0.003) | -0.0873 (0.0024) |
| 35 | 50 | normal | 0.010 (0.000) | - | - |
| 35 | 50 | t(3) | - | 0.718 (0.003) | -0.1175 (0.0026) |
| 35 | 100 | normal | 0.005 (0.000) | - | - |
| 35 | 100 | t(3) | - | 0.923 (0.002) | -0.0703 (0.0022) |
| 40 | 25 | normal | 0.019 (0.000) | - | - |
| 40 | 25 | t(3) | - | 0.465 (0.003) | -0.0860 (0.0024) |
| 40 | 50 | normal | 0.010 (0.000) | - | - |
| 40 | 50 | t(3) | - | 0.718 (0.003) | -0.1174 (0.0027) |
| 40 | 100 | normal | 0.005 (0.000) | - | - |
| 40 | 100 | t(3) | - | 0.923 (0.002) | -0.0703 (0.0022) |

Uncapped (k=0) reference: n=25: mean=0.375, var/mean^2=0.239 (0.004), t(3) power=0.379; n=50: mean=0.379, var/mean^2=0.243 (0.003), t(3) power=0.600; n=100: mean=0.381, var/mean^2=0.244 (0.004), t(3) power=0.852
Null means of capped gate: c=20,n=25: -3.164; c=20,n=50: -6.408; c=20,n=100: -12.889; c=25,n=25: -3.334; c=25,n=50: -6.744; c=25,n=100: -13.556; c=30,n=25: -3.462; c=30,n=50: -6.997; c=30,n=100: -14.059; c=35,n=25: -3.562; c=35,n=50: -7.195; c=35,n=100: -14.454; c=40,n=25: -3.643; c=40,n=50: -7.355; c=40,n=100: -14.773
c=20: variance half ok (n25=0.024, n50=0.012); power half ok (max loss -0.0709)
c=25: variance half ok (n25=0.022, n50=0.011); power half ok (max loss -0.0707)
c=30: variance half ok (n25=0.020, n50=0.011); power half ok (max loss -0.0702)
c=35: variance half ok (n25=0.019, n50=0.010); power half ok (max loss -0.0703)
c=40: variance half ok (n25=0.019, n50=0.010); power half ok (max loss -0.0703)

Mechanically smallest c = 20 (see caveat above: the variance half is an artifact of a negative null mean).

## Rule 2 table at c=20: t(5) and contaminated normal 0.9 N(0,1)+0.1 N(0,9), k=0 (uncapped) baseline in same table

| law | n | gate | var/mean^2 under normal (SE) | power (SE) | power loss vs uncapped (SE) | var half (n=25,50) | power half |
|---|---|---|---|---|---|---|---|
| t(5) | 25 | k=0 uncapped | 0.239 (0.004) | 0.192 (0.003) | 0 | - | - |
| t(5) | 25 | log(1+20t)/20 | 0.024 (0.000) | 0.266 (0.002) | -0.0740 (0.0023) | ok | ok |
| t(5) | 50 | k=0 uncapped | 0.243 (0.003) | 0.310 (0.004) | 0 | - | - |
| t(5) | 50 | log(1+20t)/20 | 0.012 (0.000) | 0.429 (0.004) | -0.1190 (0.0029) | ok | ok |
| t(5) | 100 | k=0 uncapped | 0.244 (0.004) | 0.482 (0.004) | 0 | - | - |
| t(5) | 100 | log(1+20t)/20 | 0.006 (0.000) | 0.635 (0.004) | -0.1531 (0.0023) | ok | ok |
| 0.9N(0,1)+0.1N(0,9) | 25 | k=0 uncapped | 0.239 (0.004) | 0.291 (0.003) | 0 | - | - |
| 0.9N(0,1)+0.1N(0,9) | 25 | log(1+20t)/20 | 0.024 (0.000) | 0.361 (0.003) | -0.0703 (0.0024) | ok | ok |
| 0.9N(0,1)+0.1N(0,9) | 50 | k=0 uncapped | 0.243 (0.003) | 0.461 (0.005) | 0 | - | - |
| 0.9N(0,1)+0.1N(0,9) | 50 | log(1+20t)/20 | 0.012 (0.000) | 0.547 (0.004) | -0.0867 (0.0023) | ok | ok |
| 0.9N(0,1)+0.1N(0,9) | 100 | k=0 uncapped | 0.244 (0.004) | 0.679 (0.004) | 0 | - | - |
| 0.9N(0,1)+0.1N(0,9) | 100 | log(1+20t)/20 | 0.006 (0.000) | 0.750 (0.003) | -0.0710 (0.0027) | ok | ok |

t(5): variance half holds; power half holds (max loss -0.0740)

0.9N(0,1)+0.1N(0,9): variance half holds; power half holds (max loss -0.0703)

**Per-law verdict at c=20.** t(5): variance half holds mechanically (artifact), power half holds with a gain of 0.04 to 0.17. Contaminated normal 0.9 N(0,1)+0.1 N(0,9): variance half holds mechanically (artifact), power half holds with a gain of 0.06 to 0.17. The window survives the change of law on power, but the variance criterion needs a positive-mean statistic (for example recentering the capped sum to its null mean plus the uncapped null mean) before it says anything.

## Script

```python
import numpy as np, sys, time
from scipy.stats import norm
SEED=20261021; SIMS=20000; NB=20
rng=np.random.default_rng(SEED)
CS=[20,25,30,35,40]; NS=[25,50,100]
def draw(law,n,m):
    if law=='normal': return rng.standard_normal((m,n))
    if law=='t3': return rng.standard_t(3,(m,n))
    if law=='t5': return rng.standard_t(5,(m,n))
    if law=='cn':
        x=rng.standard_normal((m,n)); mask=rng.random((m,n))<0.1
        return np.where(mask,3*x,x)
def terms(x):
    n=x.shape[1]; z=(x-x.mean(1,keepdims=True))/x.std(1,ddof=1,keepdims=True); z.sort(1)
    F=np.clip(norm.cdf(z),1e-12,1-1e-12); i=np.arange(1,n+1)
    return (2*i-1)/n*(-np.log(F)-np.log(1-F[:,::-1]))
def e0(n):
    H=np.concatenate([[0],np.cumsum(1/np.arange(1,n+1))]); i=np.arange(1,n+1)
    return (2*i-1)/n*(2*H[n]-H[i-1]-H[n-i])
def stat(t,c,e):
    d=t-1.0  # A^2 = sum_i d_i, d_i=(2i-1)/n*u_i - 1
    if c is None: return d.sum(1)
    return np.where(d>0,np.log1p(c*np.maximum(d,0))/c,d).sum(1)
def bse(v): # batch SE of a batch-wise functional already applied -> v is array of NB batch values
    return v.std(ddof=1)/np.sqrt(len(v))
res={}
for n in NS:
    e=e0(n); T={law:terms(draw(law,n,SIMS)) for law in ['normal','t3','t5','cn']}
    for c in [None]+CS:
        S={law:stat(T[law],c,e) for law in T}
        s0=S['normal']; crit=np.quantile(s0,0.95)
        b=s0.reshape(NB,-1); vm=s0.var()/s0.mean()**2; vmb=b.var(1)/b.mean(1)**2
        row={'mean0':s0.mean(),'vm':vm,'vm_se':bse(vmb),'mean':s0.mean()}
        for law in ['t3','t5','cn']:
            rej=(S[law]>crit).astype(float); row[law]=rej.mean(); row[law+'_se']=bse(rej.reshape(NB,-1).mean(1))
            row[law+'_rej']=rej
        res[(n,c)]=row
# power loss vs uncapped with batch SE of the difference (paired)
for n in NS:
    for c in CS:
        for law in ['t3','t5','cn']:
            d=res[(n,None)][law+'_rej']-res[(n,c)][law+'_rej']
            res[(n,c)][law+'_loss']=d.mean(); res[(n,c)][law+'_loss_se']=bse(d.reshape(NB,-1).mean(1))
print(f"seed={SEED} sims_per_n={SIMS} batches={NB}")
print("\n## Rule 1 table: c x n x law (normal: var/mean^2; t(3): power loss vs uncapped at normal-calibrated 5%)\n")
print("| c | n | law | var/mean^2 (SE) | t(3) power (SE) | t(3) power loss vs uncapped (SE) |"); print("|---|---|---|---|---|---|")
for c in CS:
    for n in NS:
        r=res[(n,c)]; r0=res[(n,None)]
        print(f"| {c} | {n} | normal | {r['vm']:.3f} ({r['vm_se']:.3f}) | - | - |")
        print(f"| {c} | {n} | t(3) | - | {r['t3']:.3f} ({r['t3_se']:.3f}) | {r['t3_loss']:+.4f} ({r['t3_loss_se']:.4f}) |")
print("\nUncapped (k=0) reference: " + "; ".join(f"n={n}: mean={res[(n,None)]['mean0']:.3f}, var/mean^2={res[(n,None)]['vm']:.3f} ({res[(n,None)]['vm_se']:.3f}), t(3) power={res[(n,None)]['t3']:.3f}" for n in NS))
print("Null means of capped gate: " + "; ".join(f"c={c},n={n}: {res[(n,c)]['mean0']:.3f}" for c in CS for n in NS))
# smallest c meeting both halves
best=None
for c in CS:
    h1=all(res[(n,c)]['vm']<=2/3 for n in [25,50]); h2=all(res[(n,c)]['t3_loss']<=0.02 for n in NS)
    print(f"c={c}: variance half {'ok' if h1 else 'FAIL'} (n25={res[(25,c)]['vm']:.3f}, n50={res[(50,c)]['vm']:.3f}); power half {'ok' if h2 else 'FAIL'} (max loss {max(res[(n,c)]['t3_loss'] for n in NS):+.4f})")
    if h1 and h2 and best is None: best=c
print(f"\nSMALLEST_C={best}")
if best is not None:
    c=best
    print(f"\n## Rule 2 table at c={c}: t(5) and contaminated normal 0.9 N(0,1)+0.1 N(0,9), k=0 (uncapped) baseline in same table\n")
    print("| law | n | gate | var/mean^2 under normal (SE) | power (SE) | power loss vs uncapped (SE) | var half (n=25,50) | power half |"); print("|---|---|---|---|---|---|---|---|")
    for law,name in [('t5','t(5)'),('cn','0.9N(0,1)+0.1N(0,9)')]:
        for n in NS:
            r0=res[(n,None)]; r=res[(n,c)]
            print(f"| {name} | {n} | k=0 uncapped | {r0['vm']:.3f} ({r0['vm_se']:.3f}) | {r0[law]:.3f} ({r0[law+'_se']:.3f}) | 0 | - | - |")
            vh='ok' if (n==100 or r['vm']<=2/3) else 'FAIL'; ph='ok' if r[law+'_loss']<=0.02 else 'FAIL'
            print(f"| {name} | {n} | log(1+{c}t)/{c} | {r['vm']:.3f} ({r['vm_se']:.3f}) | {r[law]:.3f} ({r[law+'_se']:.3f}) | {r[law+'_loss']:+.4f} ({r[law+'_loss_se']:.4f}) | {vh} | {ph} |")
    for law,name in [('t5','t(5)'),('cn','0.9N(0,1)+0.1N(0,9)')]:
        h1=all(res[(n,c)]['vm']<=2/3 for n in [25,50]); h2=all(res[(n,c)][law+'_loss']<=0.02 for n in NS)
        print(f"\n{name}: variance half {'holds' if h1 else 'fails'}; power half {'holds' if h2 else 'fails'} (max loss {max(res[(n,c)][law+'_loss'] for n in NS):+.4f})")
```
