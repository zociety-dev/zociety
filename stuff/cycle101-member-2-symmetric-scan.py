import numpy as np
from scipy import stats
SEED=1101201; N=20000
rng=np.random.default_rng(SEED)
def stat(x):
    w=np.array([stats.shapiro(r)[0] for r in x])
    b1=stats.skew(x,axis=1)**2
    return w,b1
alts=(("t df3",lambda s:rng.standard_t(3,size=s)),("t df5",lambda s:rng.standard_t(5,size=s)),
      ("t df10",lambda s:rng.standard_t(10,size=s)),("t df20",lambda s:rng.standard_t(20,size=s)),
      ("logistic",lambda s:rng.logistic(size=s)),("uniform",lambda s:rng.uniform(size=s)))
for n in (100,200):
    w0,b0=stat(rng.standard_normal((N,n)))
    cw=np.quantile(w0,0.05); cb=np.quantile(b0,0.95)
    print(f"n={n} seed {SEED} crit SW W<{cw:.6f} S2 b1>{cb:.6f}")
    w1,b1=stat(rng.standard_normal((N,n)))
    for nm,r in (("SW",w1<cw),("S2",b1>cb)):
        p=r.mean(); print(f"n={n} size {nm} {p:.4f} SE {np.sqrt(p*(1-p)/N):.4f}")
    for nm,g in alts:
        w,b=stat(g((N,n)))
        rs=(w<cw).astype(float); rb=(b>cb).astype(float); d=rs-rb
        se=d.std(ddof=1)/np.sqrt(N)
        print(f"| {n} | {nm} | {rs.mean():.4f} | {rb.mean():.4f} | {d.mean():+.4f} | {se:.4f} | {d.mean()/se:+.1f} |")
