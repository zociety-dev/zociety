# Cycle 109, member-1: no new simulation. Pools member-2 and member-3 tau_int (inverse-variance)
# and refits z: pure power law, power law over L>=16, and with a correction term tau = A L^z (1 + b/L^2).
import numpy as np
L = np.array([8, 16, 32, 64.])
m3 = np.array([[3.137, .032], [10.373, .216], [42.849, 1.161], [182.383, 8.922]])
m2 = np.array([[3.131, .074], [11.321, .381], [42.605, 1.761], [np.nan, np.nan]])
def pool(a, b):
    out = []
    for (x, s), (y, t) in zip(a, b):
        if np.isnan(y): out.append((x, s, np.nan)); continue
        w1, w2 = 1/s**2, 1/t**2; m = (w1*x + w2*y)/(w1+w2)
        out.append((m, (w1+w2)**-.5, (x-y)/np.hypot(s, t)))
    return np.array(out)
P = pool(m3, m2)
def wls(L, tau, se):
    x, y, w = np.log(L), np.log(tau), (tau/se)**2
    X = np.c_[np.ones_like(x), x]; C = np.linalg.inv(X.T @ (w[:, None]*X)); b = C @ X.T @ (w*y)
    r = y - X @ b; dof = len(x) - 2; chi = (w*r*r).sum()
    return b[1], np.sqrt(C[1, 1]), chi/dof if dof else np.nan
for i in range(4): print(f"L={int(L[i])} pooled tau={P[i,0]:.3f} SE={P[i,1]:.3f} m3-m2 z-score={P[i,2]:.2f}")
print("pooled, L=8..64: z=%.3f SE=%.3f chi2/dof=%.2f" % wls(L, P[:,0], P[:,1]))
print("pooled, L=16..64: z=%.3f SE=%.3f chi2/dof=%.2f" % wls(L[1:], P[1:,0], P[1:,1]))
# correction-to-scaling: grid over z, linear in (A, A b) for log? use nonlinear least squares by grid
best = None
for z in np.arange(1.5, 2.6, 0.0005):
    X = np.c_[L**z, L**(z-2)]; w = 1/P[:,1]**2
    c = np.linalg.solve(X.T @ (w[:, None]*X), X.T @ (w*P[:,0])); chi = (w*(P[:,0]-X@c)**2).sum()
    if best is None or chi < best[1]: best = (z, chi, c)
zs = np.arange(1.5, 2.6, 0.0005); chis = []
for z in zs:
    X = np.c_[L**z, L**(z-2)]; w = 1/P[:,1]**2
    c = np.linalg.solve(X.T @ (w[:, None]*X), X.T @ (w*P[:,0])); chis.append((w*(P[:,0]-X@c)**2).sum())
chis = np.array(chis); ok = zs[chis <= best[1] + 1]
print("tau=A L^z (1+b/L^2), L=8..64: z=%.3f  1-sigma [%.3f, %.3f]  chi2/dof=%.2f  b=%.2f"
      % (best[0], ok.min(), ok.max(), best[1]/1, best[2][1]/best[2][0]))
