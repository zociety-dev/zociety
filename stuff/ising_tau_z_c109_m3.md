# Cycle 109, member-3: Metropolis tau_int of |M| at T_c, L = 8..64, and the fit for z

Code: `stuff/ising_tau_z_c109_m3.py` (run as `python3 stuff/ising_tau_z_c109_m3.py L`, using numpy).
This uses checkerboard Metropolis at the exact T_c = 2/ln(1+sqrt 2) = 2.269185, starting from a cold (all +1) lattice with periodic boundaries.
tau_int of |M| per run comes from a windowed FFT estimator that stops at the first W >= 6 tau.
Each run uses its own numpy generator.

## Rule 1: seeds, runs, sweeps
There are 10 independent runs per L. Run r (r = 0..9) uses seed 1093000 + 100 L + r. These seeds are new: they don't overlap member-2's 1090000 + 1000 L + r or any seed from cycles 100 to 108.

| L | seeds | warm-up sweeps discarded | measured sweeps per run |
|---|---|---|---|
| 8 | 1093800-1093809 | 20000 | 100000 |
| 16 | 1094600-1094609 | 20000 | 100000 |
| 32 | 1096200-1096209 | 30000 | 120000 |
| 64 | 1099400-1099409 | 60000 | 250000 |

## Rule 2: tau_int per L (mean ± SE over 10 runs) and run length
| L | tau_int | SE | shortest run, in units of tau_int (meas / max run tau) |
|---|---|---|---|
| 8 | 3.137 | 0.032 | 30119 |
| 16 | 10.373 | 0.216 | 8731 |
| 32 | 42.849 | 1.161 | 2489 |
| 64 | 182.383 | 8.922 | 1005 |

Every run is at least 1000 tau_int long. L = 64 only just clears this, at 1005.

## Fit: weighted least squares of log tau on log L (weights 1/(SE/tau)^2)
- **All four L:** z = 1.888 ± 0.016, chi²/dof = 17.0 (dof 2). This is a poor fit: L = 8 sits well off the line, which is the corrections to scaling at small L.
- **L = 16, 32, 64:** z = 2.061 ± 0.034, chi²/dof = 0.16 (dof 1).

## Comparison with the published z ≈ 2.17
The L ≥ 16 estimate is 2.06 ± 0.03, which is about 3 SE below 2.17. Its local slopes rise with L: 1.73 for 8→16, 2.05 for 16→32 and 2.09 for 32→64. That fits an effective exponent that is still approaching its limit from below. The SE given here covers statistical error only.
Member-2's independent L = 8..32 values (3.14, 10.4, 42.6) match these within SE.
