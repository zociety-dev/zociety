L=[12,16,24,32,48,64,64,128.];t=[5.962,10.079,23.781,42.591,101.514,183.602,174.480,811.6];s=[.097,.124,.351,.869,2.564,6.936,3.543,40.7]
def chi(z,idx,w):
    # model: a*L^z + c*L^(z-w) (w=None -> pure power); linear LS in a,c
    fs=[[L[i]**z]+([L[i]**(z-w)] if w else []) for i in idx]
    n=len(fs[0]);M=[[0]*n for _ in range(n)];v=[0]*n
    for f,i in zip(fs,idx):
        wt=1/s[i]**2
        for a in range(n):
            v[a]+=wt*f[a]*t[i]
            for b in range(n):M[a][b]+=wt*f[a]*f[b]
    if n==1:p=[v[0]/M[0][0]]
    else:
        d=M[0][0]*M[1][1]-M[0][1]**2;p=[(v[0]*M[1][1]-v[1]*M[0][1])/d,(M[0][0]*v[1]-M[1][0]*v[0])/d]
    c2=sum(((t[i]-sum(pp*ff for pp,ff in zip(p,f)))/s[i])**2 for f,i in zip(fs,idx))
    return c2,p
def run(name,lo,w):
    idx=[i for i in range(8) if L[i]>=lo];k=2+(1 if w else 0)
    zs=[1.6+i*1e-4 for i in range(10001)];cs=[chi(z,idx,w)[0] for z in zs]
    j=min(range(len(cs)),key=cs.__getitem__);cm=cs[j];z=zs[j]
    ok=[zz for zz,c in zip(zs,cs) if c<=cm+1];dof=len(idx)-k
    p=chi(z,idx,w)[1];b=p[1]/p[0] if w else 0
    print(f"{name}: z={z:.3f} (-{z-min(ok):.3f}/+{max(ok)-z:.3f}) chi2={cm:.2f} dof={dof} chi2/dof={cm/dof:.2f} pts={len(idx)} nL={len(set(L[i] for i in idx))} b={b:.2f}")
for lo in (12,16,24,32):run(f"power L>={lo}",lo,None)
for lo in (12,16):
    run(f"1/L   L>={lo}",lo,1);run(f"1/L^2 L>={lo}",lo,2)
