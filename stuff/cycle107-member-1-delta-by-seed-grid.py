# Cycle 107: w=0.75 weighted Fisher vs plain S2, n=400, skew-normal-scaled t df 10.
# usage: python3 stuff/cycle107-member-1-delta-by-seed-grid.py SEED
# One seed per process; DELTA 0.63, 0.68, 0.75 each restart random.Random(SEED), so the
# underlying normal and chi-square draws are identical across DELTA within a seed.
# Calibration and null check use a separate stream, random.Random(SEED + 5000000).
import math, random, sys
from statistics import NormalDist
N=400; R=20000; SEED=int(sys.argv[1]); W=0.75; DELTAS=(0.63,0.68,0.75)
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
def run(rng, delta):
    g=rng.gauss; out=[]; s1=s2=s3=0.0
    for _ in range(R):
        if delta is None: x=[g(0,1) for _ in range(n)]
        else:
            r=math.sqrt(1-delta*delta); x=[]
            for _ in range(n):
                z=delta*abs(g(0,1))+r*g(0,1)
                ch=0.0
                for _ in range(10): e=g(0,1); ch+=e*e
                x.append(z/math.sqrt(ch/10))
            for v in x: s1+=v; s2+=v*v; s3+=v*v*v
        out.append(tests(x))
    sk=None
    if delta is not None:
        T=R*n; mu=s1/T; v2=s2/T-mu*mu; v3=s3/T-3*mu*s2/T+2*mu**3; sk=v3/v2**1.5
    return out, sk
nrng=random.Random(SEED+5000000)
cal,_=run(nrng,None)
cS=sorted(r[0] for r in cal)[int(0.95*R)]; cF=sorted(r[1] for r in cal)[int(0.95*R)]
ver,_=run(nrng,None)
pS=sum(r[0]>cS for r in ver)/R; pF=sum(r[1]>cF for r in ver)/R
print('SEED %d CRIT S2 p < %.5f null %.4f | F0.75 stat > %.4f null %.4f'%(SEED,math.exp(-cS),pS,cF,pF),flush=True)
for dlt in DELTAS:
    rows,sk=run(random.Random(SEED),dlt)
    rs=[1 if r[0]>cS else 0 for r in rows]; rf=[1 if r[1]>cF else 0 for r in rows]
    d=[x-y for x,y in zip(rf,rs)]; mu=sum(d)/R
    se=math.sqrt(sum((v-mu)**2 for v in d)/(R-1)/R)
    print('SEED %d DELTA %.2f sqrtb1 %.3f powS2 %.4f powF75 %.4f diff %+.4f se %.4f ratio %+.1fSE disagree %.4f'%(
        SEED,dlt,sk,sum(rs)/R,sum(rf)/R,mu,se,mu/se if se else 0,sum(1 for v in d if v)/R),flush=True)
