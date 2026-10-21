#!/usr/bin/env python3
"""Cycle 87, member-2. Centered dispersion of the capped gate log(1+ct)/c.

Gate: G_c = sum_i log(1 + c*t_i)/c with t_i = x_i^2 on standardized draws;
c=0 is the uncapped sum of t_i. Centered dispersion ratio = var(G_c)/var(G_0)
per (n, law). Top-term share = mean of max_i term / G_c. Normal-calibrated
power = P(G_c > q95 of G_c under normal at the same n) under t(3).
SEs: 20 batches of 1000 sims, SE = sd(batch stat)/sqrt(20).
Seed 870021 (not the seeds used in cycles 84-86).
"""
import numpy as np
SEED=870021; NS=20000; NB=20; BS=NS//NB
CS=[0,20,25,30,35,40]; NSZ=[25,50,100]
rng=np.random.default_rng(SEED)
def draw(law,n):
    if law=="normal": return rng.standard_normal((NS,n))
    if law=="t3": return rng.standard_t(3,(NS,n))
    if law=="t5": return rng.standard_t(5,(NS,n))
    z=rng.standard_normal((NS,n)); m=rng.random((NS,n))<0.1
    return np.where(m,3*z,z)
def gate(x,c):
    t=x*x
    term=t if c==0 else np.log1p(c*t)/c
    return term.sum(1), (term.max(1)/term.sum(1))
rows=[]; power={}
for n in NSZ:
    data={law:draw(law,n) for law in ["normal","t3","t5","mix"]}
    for law,x in data.items():
        g0,_=gate(x,0); v0=g0.reshape(NB,BS).var(1)
        for c in CS:
            g,s=gate(x,c)
            vb=g.reshape(NB,BS).var(1)/v0; sb=s.reshape(NB,BS).mean(1)
            rows.append((c,n,law,vb.mean(),vb.std(ddof=1)/np.sqrt(NB),sb.mean(),sb.std(ddof=1)/np.sqrt(NB)))
            if law=="normal": power[(c,n,"crit")]=np.quantile(g,0.95)
    for c in CS:
        g,_=gate(data["t3"],c); hit=(g>power[(c,n,"crit")]).reshape(NB,BS).mean(1)
        power[(c,n)]=hit
print("## Rule 1 table: centered dispersion ratio and top-term share (20000 sims per n, seed 870021)\n")
print("| c | n | law | disp ratio | SE | top-term share | SE |\n|---|---|---|---|---|---|---|")
flat={}
for c,n,law,v,ve,s,se in rows:
    print(f"| {c} | {n} | {law} | {v:.3f} | {ve:.3f} | {s:.4f} | {se:.4f} |")
    if c>0: flat.setdefault(law,[]).append(abs(v-1)<=2*ve)
print("\n## Rule 2 summary\n")
print("| n | best c | power(best) | power(c=0) | gain | SE(gain) | gain > 2 SE |\n|---|---|---|---|---|---|---|")
for n in NSZ:
    p0=power[(0,n)]
    best=max([c for c in CS if c>0],key=lambda c:power[(c,n)].mean())
    d=power[(best,n)]-p0; se=d.std(ddof=1)/np.sqrt(NB)
    print(f"| {n} | {best} | {power[(best,n)].mean():.4f} | {p0.mean():.4f} | {d.mean():+.4f} | {se:.4f} | {'yes' if d.mean()>2*se else 'no'} |")
print("\nAll c, t(3) power by n:", {n:{c:round(power[(c,n)].mean(),4) for c in CS} for n in NSZ})
print("\nDispersion ratio flat in c (every c within 2 SE of 1)?")
for law,fl in flat.items(): print(f"- {law}: {'flat' if all(fl) else 'NOT flat'} ({sum(fl)}/{len(fl)} cells within 2 SE)")
