# Cycle 98: SW vs plain S2 at n=200, gamma crossover (seed 20261031)

Seed: 20261031 (third independent seed; member-2 used 20261201, member-3 used 20261021).
Script: `stuff/cycle98-sw-vs-s2-n200-seed20261031.py 20261031` (pure Python, same estimator as the other two files: Royston SW coefficients, S2 = m3^2 / m2^3). Runtime about 19 s.

Exact-size 5% critical values at n=200, calibrated on a 20000-draw N(0,1) run:

- Shapiro-Wilk: reject when W < 0.98629
- plain S2: reject when S2 > 0.11234

Separate 20000-draw N(0,1) size check at n=200 (paired, fresh draws after calibration):

| test | rejection rate | binomial SE |
|---|---|---|
| SW | 0.0481 | 0.0015 |
| S2 | 0.0483 | 0.0015 |

SW minus S2 under the null: -0.0003, paired SE 0.0015 (-0.2 SE). Both tests sit at 5%.

Power at n=200, 20000 paired draws per shape, gamma(shape, 1):

| shape | sqrt(beta1) = 2/sqrt(shape) | SW power (SE) | S2 power (SE) | SW - S2 | paired SE | z |
|---|---|---|---|---|---|---|
| 2 | 1.414 | 1.0000 (0.0000) | 1.0000 (0.0000) | +0.0000 | 0.0000 | 0.0 |
| 5 | 0.894 | 0.9978 (0.0003) | 0.9956 (0.0005) | +0.0022 | 0.0004 | +5.0 |
| 10 | 0.632 | 0.9093 (0.0020) | 0.9251 (0.0019) | -0.0158 | 0.0017 | -9.5 |
| 20 | 0.447 | 0.6146 (0.0034) | 0.6789 (0.0033) | -0.0644 | 0.0025 | -26.0 |
| 50 | 0.283 | 0.2846 (0.0032) | 0.3497 (0.0034) | -0.0651 | 0.0025 | -26.1 |

Margin against sqrt(beta1): nil at 1.41 (both tests saturated), a small positive SW edge at 0.89 (+0.2 points, 5 SE), then negative from 0.63 down with the S2 margin widening as skew weakens (-1.6 points at 0.63, -6.4 at 0.45, -6.5 at 0.28). The margin is flat between gamma(20) and gamma(50), so the S2 advantage has plateaued by sqrt(beta1) = 0.45 at this n.

Cross-seed check: all three seeds (20261201, 20261021, 20261031) put the sign change in the same bracket, with the gamma(5) edge for SW between +4 and +5 SE and the gamma(10) edge for S2 between -7 and -10 SE. The crossover is not a seed artefact.

Flip: SW minus S2 changes sign beyond two paired SE between gamma(5) (sqrt(beta1) = 0.894, margin +0.0022, +5.0 SE) and gamma(10) (sqrt(beta1) = 0.632, margin -0.0158, -9.5 SE).
