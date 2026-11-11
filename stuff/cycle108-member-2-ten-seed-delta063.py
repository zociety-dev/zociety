# Cycle 108 (member-2): DELTA 0.63 on ten new seeds, 20000 paired draws each, n=400,
# both cutoffs from one independent 400000-draw null sample (checked on a further 400000).
# Statistics are the numpy forms from stuff/cycle107-member-2-pooled-calibration.py (archived), unchanged.
# run: uv run --no-project --with numpy python3 stuff/cycle108-member-2-ten-seed-delta063.py
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
g=np.random.default_rng(NULL_SEED)
def draw(k):
    S=[];F=[]
    for _ in range(k): s,f=vt(g.standard_normal((20000,n))); S.append(s); F.append(f)
    return np.concatenate(S),np.concatenate(F)
S,F=draw(20); K=len(S); cS=np.sort(S)[int(0.95*K)]; cF=np.sort(F)[int(0.95*K)]
S,F=draw(20)
print('NULL seed %d, %d draws: S2 stat > %.6f (p < %.5f), F0.75 stat > %.6f; size on further %d: S2 %.4f F %.4f'%(
    NULL_SEED,K,cS,math.exp(-cS),cF,len(S),(S>cS).mean(),(F>cF).mean()))
r=math.sqrt(1-DELTA**2); ms=[]
for sd in SEEDS:
    g=np.random.default_rng(sd)
    x=(DELTA*np.abs(g.standard_normal((R,n)))+r*g.standard_normal((R,n)))/np.sqrt(g.chisquare(10,(R,n))/10)
    d=x-x.mean(); sk=(d**3).mean()/(d**2).mean()**1.5   # pooled over all R*n values
    s,f=vt(x); dd=(f>cF).astype(float)-(s>cS); mu=dd.mean(); se=dd.std(ddof=1)/math.sqrt(R); ms.append(mu)
    print('seed %d sqrt(beta1) %.3f powS2 %.4f powF %.4f margin %+.4f se %.4f (%+.1f SE)'%(
        sd,sk,(s>cS).mean(),(f>cF).mean(),mu,se,mu/se),flush=True)
ms=np.array(ms); mean=ms.mean(); ase=ms.std(ddof=1)/math.sqrt(len(ms))
print('mean %+.5f across-seed SD %.5f across-seed SE %.5f ratio %+.2f positive %d/10 exceeds 2 SE: %s'%(
    mean,ms.std(ddof=1),ase,mean/ase,(ms>0).sum(),'yes' if mean>2*ase else 'no'))
