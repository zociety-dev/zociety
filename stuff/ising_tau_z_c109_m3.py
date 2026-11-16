# Cycle 109, member-3: batched checkerboard Metropolis, 2-D Ising at exact T_c, tau_int of |M|.
import numpy as np, sys, json
Tc = 2/np.log(1+np.sqrt(2)); beta = 1/Tc
R = 10
PLAN = {8: (20000, 100000), 16: (20000, 100000), 32: (30000, 120000), 64: (60000, 250000)}
def seeds(L): return [1093000 + 100*L + r for r in range(R)]   # new, cycle-109 member-3 range
acc = {d: np.float32(min(1.0, np.exp(-beta*d))) for d in (-8,-4,0,4,8)}
def run(L, warm, meas):
    gens = [np.random.default_rng(s) for s in seeds(L)]
    s = np.ones((R, L, L), np.int8)
    ii, jj = np.indices((L, L)); masks = [((ii+jj) % 2 == p) for p in (0, 1)]
    table = np.array([acc[d] for d in (-8,-4,0,4,8)], np.float32)
    out = np.empty((R, meas), np.float32); CH = 500; tot = warm + meas; t = 0
    while t < tot:
        n = min(CH, tot - t)
        U = np.stack([g.random((n, 2, L, L), dtype=np.float32) for g in gens], 1)
        for k in range(n):
            for p in (0, 1):
                nb = np.roll(s,1,1)+np.roll(s,-1,1)+np.roll(s,1,2)+np.roll(s,-1,2)
                dE = 2*s*nb  # in {-8..8}
                flip = masks[p] & (U[k, :, p] < table[(dE.astype(np.int16)+8)//4])
                s = np.where(flip, -s, s).astype(np.int8)
            if t >= warm: out[:, t-warm] = np.abs(s.sum((1, 2), dtype=np.int32))/(L*L)
            t += 1
    return out
def tau_int(x, c=6):
    x = x - x.mean(); n = len(x); f = np.fft.rfft(x, 2*n)
    rho = np.fft.irfft(f*np.conj(f))[:n]; rho /= rho[0]; tau = 0.5
    for W in range(1, n):
        tau += rho[W]
        if W >= c*tau: return tau, W
    return tau, n
res = {}
for L in map(int, sys.argv[1:]):
    w, m = PLAN[L]; M = run(L, w, m)
    taus = np.array([tau_int(M[r].astype(np.float64))[0] for r in range(R)])
    res[L] = dict(warm=w, meas=m, seeds=seeds(L), taus=taus.tolist(), mean=taus.mean(),
                  se=taus.std(ddof=1)/np.sqrt(R), min_len_in_tau=m/taus.max())
    print(L, res[L]['mean'], res[L]['se'], res[L]['min_len_in_tau'], flush=True)
json.dump(res, open(f"/tmp/z3/res_{'_'.join(sys.argv[1:])}.json", "w"))
