import random, math, sys
from statistics import NormalDist
n=200; N=20000; seed=int(sys.argv[1]); R=random.Random(seed)
inv=NormalDist().inv_cdf
m=[inv((i+1-0.375)/(n+0.25)) for i in range(n)]
mm=sum(x*x for x in m); u=1/math.sqrt(n)
an=-2.706056*u**5+4.434685*u**4-2.07119*u**3-0.147981*u**2+0.221157*u+m[-1]/math.sqrt(mm)
an1=-3.582633*u**5+5.682633*u**4-1.752461*u**3-0.293762*u**2+0.042981*u+m[-2]/math.sqrt(mm)
phi=(mm-2*m[-1]**2-2*m[-2]**2)/(1-2*an**2-2*an1**2)
a=[mi/math.sqrt(phi) for mi in m]; a[-1]=an; a[-2]=an1; a[0]=-an; a[1]=-an1
def stats(x):
    x=sorted(x); mu=sum(x)/n; d=[v-mu for v in x]
    m2=sum(v*v for v in d)/n; m3=sum(v*v*v for v in d)/n
    W=sum(ai*xi for ai,xi in zip(a,x))**2/(n*m2)
    return W, m3*m3/m2**3
def draw(f): return [stats([f() for _ in range(n)]) for _ in range(N)]
null=draw(lambda:R.gauss(0,1))
cw=sorted(s[0] for s in null)[int(0.05*N)]; cs=sorted(s[1] for s in null)[int(0.95*N)]
print(f"seed {seed} critW {cw:.5f} critS2 {cs:.5f}")
def rep(name,res):
    sw=[s[0]<cw for s in res]; s2=[s[1]>cs for s in res]
    p1=sum(sw)/N; p2=sum(s2)/N; d=[a-b for a,b in zip(sw,s2)]; md=sum(d)/N
    se=math.sqrt((sum(x*x for x in d)/N-md*md)/N)
    print(f"{name} SW {p1:.4f} ({math.sqrt(p1*(1-p1)/N):.4f}) S2 {p2:.4f} ({math.sqrt(p2*(1-p2)/N):.4f}) diff {md:+.4f} se {se:.4f} z {md/se if se else 0:+.1f}")
rep("N01",draw(lambda:R.gauss(0,1)))
for k in (2,5,10,20,50):
    print(f"sqrtb1 {2/math.sqrt(k):.3f}",end=" "); rep(f"g{k}",draw(lambda:R.gammavariate(k,1)))
