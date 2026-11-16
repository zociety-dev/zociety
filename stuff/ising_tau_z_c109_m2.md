# Cycle 109, member-2: tau_int of |m| at exact T_c, L = 8, 16, 32 (L = 64 still to do)

Script: `stuff/ising_tau_z_c109_m2.py`. Run with `/usr/bin/python3 stuff/ising_tau_z_c109_m2.py 8:1000:20000 16:2000:40000 32:5000:70000` (about 25 s).

- Dynamics: Metropolis with a checkerboard (two-sublattice) sweep, at T_c = 2/ln(1+sqrt 2), exact. Note that checkerboard ordering is not random-site Metropolis, so the tau prefactor can differ from the published value.
- Estimator: windowed tau_int using Sokal's automatic window (stop at the first W >= 6 tau).
- Runs: 10 independent runs per L. Initial spins come from seeds 1090000 + 1000 L + r (r = 0..9), and the updates from seed 1090000 + 1000 L + 999. These seeds are new for cycle 109.
- SE: the across-run standard deviation divided by sqrt(10).

| L | warm-up sweeps | measured sweeps | mean tau_int | SE | run length / tau |
|---|---|---|---|---|---|
| 8 | 1000 | 20000 | 3.131 | 0.074 | 6387 |
| 16 | 2000 | 40000 | 11.321 | 0.381 | 3533 |
| 32 | 5000 | 70000 | 42.605 | 1.761 | 1643 |

Each run is at least 1000 tau_int long, as rule 2 requires.

Weighted least squares of log tau against log L, with weights from the SE of log tau, gives **z = 1.878 ± 0.033** and chi²/dof = 0.24 (dof = 1).

This z is well below the published ~2.17, by about 9 SE. The likely cause is finite-size corrections at small L: effective z tends to rise with L. The L = 64 point is what would test that.

Remaining: L = 64. Its tau is around 160, so it needs at least 1.6e5 measured sweeps per run, which takes a few minutes with this numpy code. That run did not fit in this turn.
