# Cycle 107 (member-2): redo member-1's nine cells with ONE pooled critical value pair,
# to separate calibration noise from alternative-draw noise.
# usage 1: python3 THIS cal            -> pooled crit from 400000 numpy null samples (+400000 check)
# usage 2: python3 THIS SEED cS cF     -> same alternative draws as member-1 (random.Random(SEED)),
#          margin under member-1's per-seed crit (recomputed, stream SEED+5000000) and under pooled cS, cF.
import math, random, sys
from statistics import NormalDist
N=400; R=20000; W=0.75; DELTAS=(0.63,0.68,0.75)
nd=NormalDist()
m=[nd.inv_cdf((i-0.375)/(N+0.25)) for i in range(1,N+1)]
mm=sum(x*x for x in m); c=[x/math.sqrt(mm) for x in m]; u=1/math.sqrt(N)
an=c[-1]+0.221157*u-0.147981*u**2-2.071190*u**3+4.434685*u**4-2.706056*u**5
an1=c[-2]+0.042981*u-0.293762*u**2-1.752461*u**3+5.682633*u**4-3.582633*u**5
phi=(mm-2*m[-1]**2-2*m[-2]**2)/(1-2*an**2-2*an1**2)
a=[x/math.sqrt(phi) for x in m]; a[-1]=an; a[-2]=an1; a[0]=-an; a[1]=-an1
ln=math.log(N); MU=0.0038915*ln**3-0.083751*ln**2-0.31082*ln-1.5861
SG=math.exp(0.0030302*ln**2-0.082676*ln-0.4803)
n=N; beta2=3*(n*n+27*n-70)*(n+1)*(n+3)/((n-2)*(n+5)*(n+7)*(n+9))
W2=-1+math.sqrt(2*(beta2-1)); dl=1/math.sqrt(math.log(math.sqrt(W2))); al=math.sqrt(2/(W2-1))
E=3*(n-1)/(n+1); V=24*n*(n-2)*(n-3)/((n+1)**2*(n+3)*(n+5))
sb=6*(n*n-5*n+2)/((n+7)*(n+9))*math.sqrt(6*(n+3)*(n+5)/(n*(n-2)*(n-3)))
A=6+8/sb*(2/sb+math.sqrt(1+4/sb**2)); yk=math.sqrt((n+1)*(n+3)/(6*(n-2)))
def tests(x):
    xs=sorted(x); mu=sum(xs)/n; d=[v-mu for v in xs]
    m2=sum(v*v for v in d)/n; m3=sum(v**3 for v in d)/n; m4=sum(v**4 for v in d)/n
    Wst=sum(ai*v for ai,v in zip(a,xs))**2/(m2*n)
    psw=max(1-nd.cdf((math.log(1-Wst)-MU)/SG),1e-300)
    Y=m3/m2**1.5*yk/al; Z1=dl*math.log(Y+math.sqrt(Y*Y+1))
    xk=(m4/m2**2-E)/math.sqrt(V); t=(1-2/A)/(1+xk*math.sqrt(2/(A-4)))
    t=math.copysign(abs(t)**(1/3),t); Z2=((1-2/(9*A))-t)/math.sqrt(2/(9*A))
    ps2=max(math.exp(-(Z1*Z1+Z2*Z2)/2),1e-300)
    return -math.log(ps2), -2*(W*math.log(ps2)+(1-W)*math.log(psw))
if sys.argv[1]=='cal':
    import numpy as np
    from math import erfc; ndtr=np.vectorize(lambda z: 0.5*erfc(-z/math.sqrt(2)))
    av=np.array(a)
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
    # agreement check of the numpy statistics against the pure-Python ones
    g=np.random.default_rng(1); x=g.standard_normal((50,n)); s,f=vt(x)
    md=max(max(abs(tests(list(x[i]))[0]-s[i]),abs(tests(list(x[i]))[1]-f[i])) for i in range(50))
    print('max |numpy - python| over 50 samples: %.2e'%md)
    g=np.random.default_rng(107107)
    def draw(k):
        S=[];F=[]
        for _ in range(k): s,f=vt(g.standard_normal((20000,n))); S.append(s); F.append(f)
        return np.concatenate(S),np.concatenate(F)
    S,F=draw(20); K=len(S); cS=np.sort(S)[int(0.95*K)]; cF=np.sort(F)[int(0.95*K)]
    S,F=draw(20)
    print('POOLED %d nulls: S2 p < %.5f (stat > %.6f) null %.4f | F0.75 stat > %.6f null %.4f'%(
        K,math.exp(-cS),cS,(S>cS).mean(),cF,(F>cF).mean()))
    # where member-1's per-seed cutoffs sit on this 400000-sample null check
    for sd,p,cf in ((107011,0.04714,6.0202),(107023,0.04860,5.9259),(107039,0.04844,5.8712)):
        print('seed %d cutoffs true size: S2 %.4f F %.4f'%(sd,(S>-math.log(p)).mean(),(F>cf).mean()))
    sys.exit()
SEED=int(sys.argv[1]); pS=float(sys.argv[2]); pF=float(sys.argv[3])
def run(rng, delta, reps):
    g=rng.gauss; out=[]
    for _ in range(reps):
        if delta is None: x=[g(0,1) for _ in range(n)]
        else:
            r=math.sqrt(1-delta*delta); x=[]
            for _ in range(n):
                z=delta*abs(g(0,1))+r*g(0,1)
                ch=0.0
                for _ in range(10): e=g(0,1); ch+=e*e
                x.append(z/math.sqrt(ch/10))
        out.append(tests(x))
    return out
cal=run(random.Random(SEED+5000000),None,R)
cS=sorted(r[0] for r in cal)[int(0.95*R)]; cF=sorted(r[1] for r in cal)[int(0.95*R)]
def marg(rows,kS,kF):
    d=[(r[1]>kF)-(r[0]>kS) for r in rows]; mu=sum(d)/R
    return mu, math.sqrt(sum((v-mu)**2 for v in d)/(R-1)/R), sum(r[0]>kS for r in rows)/R, sum(r[1]>kF for r in rows)/R
for dlt in DELTAS:
    rows=run(random.Random(SEED),dlt,R)
    a1=marg(rows,cS,cF); a2=marg(rows,pS,pF)
    print('SEED %d DELTA %.2f | per-seed crit diff %+.4f se %.4f | pooled crit powS2 %.4f powF %.4f diff %+.4f se %.4f (%+.1f SE)'%(
        SEED,dlt,a1[0],a1[1],a2[2],a2[3],a2[0],a2[1],a2[0]/a2[1]),flush=True)
