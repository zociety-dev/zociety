# Cycle 108 (member-1): held-out size check for member-3's pooled 1,600,000-draw cutoffs.
# Statistic code below is copied unchanged from stuff/cycle108-member-3-recalibration.py (lines 5-33).
# Four NEW null streams (1,600,000 draws) that played no part in any cutoff measure the size of the pooled cutoffs.
# run: uv run --no-project --with numpy python3 stuff/cycle108-member-1-pooled-heldout-size.py
import math, numpy as np
from statistics import NormalDist
N=400; R=20000; W=0.75; DELTA=0.63; NULL_SEED=108999
SEEDS=(108011,108023,108037,108041,108053,108067,108079,108083,108097,108103)
nd=NormalDist(); n=N
m=[nd.inv_cdf((i-0.375)/(N+0.25)) for i in range(1,N+1)]
mm=sum(x*x for x in m); c=[x/math.sqrt(mm) for x in m]; u=1/math.sqrt(N)
an=c[-1]+0.221157*u-0.147981*u**2-2.071190*u**3+4.434685*u**4-2.706056*u**5
an1=c[-2]+0.042981*u-0.293762*u**2-1.752461*u**3+5.682633*u**4-3.582633*u**5
phi=(mm-2*m[-1]**2-2*m[-2]**2)/(1-2*an**2-2*an1**2)
a=[x/math.sqrt(phi) for x in m]; a[-1]=an; a[-2]=an1; a[0]=-an; a[1]=-an1
ln=math.log(N); MU=0.0038915*ln**3-0.083751*ln**2-0.31082*ln-1.5861
SG=math.exp(0.0030302*ln**2-0.082676*ln-0.4803)
beta2=3*(n*n+27*n-70)*(n+1)*(n+3)/((n-2)*(n+5)*(n+7)*(n+9))
W2=-1+math.sqrt(2*(beta2-1)); dl=1/math.sqrt(math.log(math.sqrt(W2))); al=math.sqrt(2/(W2-1))
E=3*(n-1)/(n+1); V=24*n*(n-2)*(n-3)/((n+1)**2*(n+3)*(n+5))
sb=6*(n*n-5*n+2)/((n+7)*(n+9))*math.sqrt(6*(n+3)*(n+5)/(n*(n-2)*(n-3)))
A=6+8/sb*(2/sb+math.sqrt(1+4/sb**2)); yk=math.sqrt((n+1)*(n+3)/(6*(n-2)))
ndtr=np.vectorize(lambda z: 0.5*math.erfc(-z/math.sqrt(2))); av=np.array(a)
def vt(x):
    xs=np.sort(x,axis=1); d=xs-xs.mean(1,keepdims=True)
    m2=(d**2).mean(1); m3=(d**3).mean(1); m4=(d**4).mean(1)
    Wst=(xs@av)**2/(m2*n)
    psw=np.maximum(ndtr(-(np.log(1-Wst)-MU)/SG),1e-300)
    Y=m3/m2**1.5*yk/al; Z1=dl*np.arcsinh(Y)
    xk=(m4/m2**2-E)/math.sqrt(V); t=(1-2/A)/(1+xk*math.sqrt(2/(A-4)))
    Z2=((1-2/(9*A))-np.cbrt(t))/math.sqrt(2/(9*A))
    s=(Z1*Z1+Z2*Z2)/2
    return s, -2*(W*(-s)+(1-W)*np.log(psw))
OLD_NULLS=(108201,108211,108223,108227)   # member-3's four streams: rebuilt here to reproduce the pooled cutoffs
NEW_NULLS=(108301,108307,108311,108317)   # fresh, used nowhere before
def nullset(seeds):
    S=[];F=[]
    for ns in seeds:
        g=np.random.default_rng(ns)
        for _ in range(20): s,f=vt(g.standard_normal((20000,n))); S.append(s); F.append(f)
    return np.concatenate(S),np.concatenate(F)
q=lambda v: np.sort(v)[int(0.95*len(v))]
oS,oF=nullset(OLD_NULLS); cS,cF=q(oS),q(oF)
print('pooled cutoffs rebuilt: cS %.6f cF %.6f (member-3 reported 3.035760, 5.927409)'%(cS,cF),flush=True)
hS,hF=nullset(NEW_NULLS); M=len(hS)
rs=(hS>cS).astype(float); rf=(hF>cF).astype(float); d=rf-rs
print('held-out size on %d fresh nulls: S2 %.5f (SE %.5f) Fisher %.5f (SE %.5f) gap F-S2 %+.5f paired SE %.5f'%(
    M,rs.mean(),rs.std()/math.sqrt(M),rf.mean(),rf.std()/math.sqrt(M),d.mean(),d.std()/math.sqrt(M)),flush=True)
for k,ns in enumerate(NEW_NULLS):
    sl=slice(k*400000,(k+1)*400000)
    print('  stream %d: S2 %.5f Fisher %.5f gap %+.5f'%(ns,rs[sl].mean(),rf[sl].mean(),d[sl].mean()),flush=True)
r=math.sqrt(1-DELTA**2); PS=[];PF=[]
for sd in SEEDS:
    g=np.random.default_rng(sd)
    x=(DELTA*np.abs(g.standard_normal((R,n)))+r*g.standard_normal((R,n)))/np.sqrt(g.chisquare(10,(R,n))/10)
    s,f=vt(x); PS.append(s); PF.append(f)
PS=np.array(PS); PF=np.array(PF)
def report(tag,cS,cF):
    ms=((PF>cF).astype(float)-(PS>cS)).mean(1); ase=ms.std(ddof=1)/math.sqrt(len(ms))
    print('%s cS %.6f cF %.6f | mean margin %+.5f across-seed SE %.5f ratio %+.2f positive %d/10 | S2 power %.4f Fisher power %.4f'%(
        tag,cS,cF,ms.mean(),ase,ms.mean()/ase,(ms>0).sum(),(PS>cS).mean(),(PF>cF).mean()),flush=True)
report('member-3 pooled 1600000',cS,cF)
report('fresh 1600000 only     ',q(hS),q(hF))
report('all 3200000            ',q(np.concatenate([oS,hS])),q(np.concatenate([oF,hF])))
