"""Cycle 109, member-2: Metropolis (checkerboard) 2-D Ising at exact T_c, tau_int of |m|.
Usage: python3 stuff/ising_tau_z_c109_m2.py L:warm:meas ...
Seeds: 1090000 + 1000*L + r, r = 0..R-1 (new for cycle 109)."""
import sys, numpy as np
TC = 2/np.log(1+np.sqrt(2)); BETA = 1/TC; R = 10

def tau_int(x, c=6.0):
    x = x - x.mean(); n = len(x)
    f = np.fft.rfft(x, 2*n); acf = np.fft.irfft(f*np.conj(f))[:n]; acf /= acf[0]
    tau = 0.5
    for W in range(1, n):
        tau += acf[W]
        if W >= c*tau: return tau, W
    return tau, n

def run(L, warm, meas):
    rngs = [np.random.default_rng(1090000+1000*L+r) for r in range(R)]
    s = np.stack([np.where(g.random((L, L)) < .5, 1, -1) for g in rngs]).astype(np.int8)
    ii, jj = np.indices((L, L)); masks = [((ii+jj) % 2) == p for p in (0, 1)]
    acc = {d: np.exp(-BETA*d) for d in (-8, -4, 0, 4, 8)}
    lut = np.array([min(1, np.exp(-BETA*d)) for d in range(-8, 9)])
    g = np.random.default_rng(1090000+1000*L+999)  # shared stream for the batch
    ms = np.empty((meas, R))
    for t in range(warm+meas):
        for m in masks:
            nb = (np.roll(s,1,1)+np.roll(s,-1,1)+np.roll(s,1,2)+np.roll(s,-1,2)).astype(np.int16)
            dE = 2*s*nb
            flip = (g.random(s.shape) < lut[dE+8]) & m
            s[flip] *= -1
        if t >= warm: ms[t-warm] = np.abs(s.sum((1, 2)))/(L*L)
    taus = np.array([tau_int(ms[:, r])[0] for r in range(R)])
    return taus

out = []
for arg in sys.argv[1:]:
    L, warm, meas = map(int, arg.split(':'))
    taus = run(L, warm, meas)
    out.append((L, taus.mean(), taus.std(ddof=1)/np.sqrt(R), meas/taus.mean()))
    print(f"L={L} warm={warm} meas={meas} R={R} tau={taus.mean():.3f} SE={out[-1][2]:.3f} meas/tau={out[-1][3]:.0f}", flush=True)
if len(out) >= 2:
    lL = np.log([o[0] for o in out]); lt = np.log([o[1] for o in out]); se = np.array([o[2]/o[1] for o in out])
    w = 1/se**2; A = np.vstack([np.ones_like(lL), lL]).T
    cov = np.linalg.inv(A.T @ (A*w[:, None])); b = cov @ (A.T @ (w*lt))
    chi2 = np.sum(w*(lt-A@b)**2); dof = len(out)-2
    print(f"z={b[1]:.3f} SE={np.sqrt(cov[1,1]):.3f} chi2/dof={(chi2/dof if dof else float('nan')):.2f} (dof={dof})")
