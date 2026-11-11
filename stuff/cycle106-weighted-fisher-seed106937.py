import math, random, sys
from statistics import NormalDist
N=400; R=20000; SEED=int(sys.argv[1]); WS=(0.25,0.5,0.75); DELTA=float(sys.argv[2])
nd=NormalDist(); rng=random.Random(SEED)
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
    W=sum(ai*v for ai,v in zip(a,xs))**2/(m2*n)
    psw=1-nd.cdf((math.log(1-W)-MU)/SG)
    Y=m3/m2**1.5*yk/al; Z1=dl*math.log(Y+math.sqrt(Y*Y+1))
    xk=(m4/m2**2-E)/math.sqrt(V); t=(1-2/A)/(1+xk*math.sqrt(2/(A-4)))
    t=math.copysign(abs(t)**(1/3),t); Z2=((1-2/(9*A))-t)/math.sqrt(2/(9*A))
    ps2=math.exp(-(Z1*Z1+Z2*Z2)/2)
    return max(psw,1e-300),max(ps2,1e-300)
def chi(k): return sum(rng.gauss(0,1)**2 for _ in range(k))
def gen(kind):
    if kind=='null': return [rng.gauss(0,1) for _ in range(n)]
    if kind=='t5': return [rng.gauss(0,1)/math.sqrt(chi(5)/5) for _ in range(n)]
    out=[]
    for _ in range(n):
        z=DELTA*abs(rng.gauss(0,1))+math.sqrt(1-DELTA**2)*rng.gauss(0,1)
        out.append(z/math.sqrt(chi(10)/10))
    return out
def stats(ps):
    psw,ps2=ps; s={'SW':-math.log(psw),'S2':-math.log(ps2),'F':-2*(math.log(ps2)+math.log(psw))}
    for w in WS: s['F%.2f'%w]=-2*(w*math.log(ps2)+(1-w)*math.log(psw))
    return s
NAMES=['SW','S2','F']+['F%.2f'%w for w in WS]
def run(kind): return [stats(tests(gen(kind))) for _ in range(R)]
cal=run('null'); crit={}
for k in NAMES:
    v=sorted(r[k] for r in cal); crit[k]=v[int(0.95*R)]
def rej(rows): return {k:[1 if r[k]>crit[k] else 0 for r in rows] for k in NAMES}
def pw(x): p=sum(x)/R; return p, math.sqrt(p*(1-p)/R)
def pd(x,y):
    d=[a-b for a,b in zip(x,y)]; mu=sum(d)/R; sd=math.sqrt(sum((v-mu)**2 for v in d)/(R-1))
    return mu, sd/math.sqrt(R), sum(1 for v in d if v)/R
lab={'SW':'SW','S2':'S2','F':'Fisher (w=0.5 unweighted, -2[ln pS2+ln pSW])'}
print('SEED',SEED,'DELTA',DELTA)
print('CRIT'); ver=rej(run('null'))
for k in NAMES:
    thr = ('p < %.5f'%math.exp(-crit[k])) if k in('SW','S2') else 'stat > %.4f'%crit[k]
    p,se=pw(ver[k]); print(k,thr,'%.4f'%p,'%.4f'%se)
for kind in ('t5','skt10'):
    rows=run(kind)
    if kind=='skt10':
        pass
    rj=rej(rows); print('ALT',kind)
    for k in NAMES: p,se=pw(rj[k]); print(' power',k,'%.4f'%p,'%.4f'%se)
    for k in ['F']+NAMES[3:]:
        for b in ('S2','SW','F'):
            if b==k: continue
            mu,se,dis=pd(rj[k],rj[b]); print(' diff',k,'-',b,'%+.4f'%mu,'%.4f'%se,'disagree %.4f'%dis,'%+.1fSE'%(mu/se if se else 0))
# pooled skewness of skt10
big=[x for _ in range(250) for x in gen('skt10')]; mu=sum(big)/len(big)
m2=sum((v-mu)**2 for v in big)/len(big); m3=sum((v-mu)**3 for v in big)/len(big)
print('pooled sqrt(beta1) skt10 over 100000 draws: %.3f'%(m3/m2**1.5))
