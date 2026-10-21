# Cycle 98: SW vs plain S2 at n=200, gamma crossover (seed 20261021)

Seed: 20261021 (new seed, independent of member-2's 20261201 run).
Script: `stuff/cycle98-sw-vs-s2-n200-seed20261021.py 20261021` (pure Python, same estimator as member-2's file: Royston SW coefficients, S2 = m3^2 / m2^3).

Exact-size 5% critical values at n=200, calibrated on a 20000-draw N(0,1) run:

- Shapiro-Wilk: reject when W < 0.98630
- plain S2: reject when S2 > 0.11505

Separate 20000-draw N(0,1) size check at n=200 (paired, fresh draws after calibration):

| test | rejection rate | binomial SE |
|---|---|---|
| SW | 0.0505 | 0.0015 |
| S2 | 0.0486 | 0.0015 |

SW minus S2 under the null: +0.0019, paired SE 0.0015 (1.3 SE). Both tests sit at 5%.

Power at n=200, 20000 paired draws per shape, gamma(shape, 1):

| shape | sqrt(beta1) = 2/sqrt(shape) | SW power (SE) | S2 power (SE) | SW - S2 | paired SE | z |
|---|---|---|---|---|---|---|
| 2 | 1.414 | 1.0000 (0.0000) | 1.0000 (0.0000) | +0.0000 | 0.0000 | 0.0 |
| 5 | 0.894 | 0.9976 (0.0003) | 0.9958 (0.0005) | +0.0018 | 0.0004 | +4.3 |
| 10 | 0.632 | 0.9072 (0.0021) | 0.9186 (0.0019) | -0.0115 | 0.0016 | -7.1 |
| 20 | 0.447 | 0.6186 (0.0034) | 0.6727 (0.0033) | -0.0541 | 0.0025 | -22.0 |
| 50 | 0.283 | 0.2867 (0.0032) | 0.3454 (0.0034) | -0.0587 | 0.0024 | -24.0 |

Margin against sqrt(beta1): the SW advantage is nil at sqrt(beta1) = 1.41 (both saturated), small but positive at 0.89, and negative from 0.63 down, with the S2 margin widening as skew weakens (-1.2 points at 0.63, -5.4 at 0.45, -5.9 at 0.28). This agrees with the cycle 97 learning that S2 beats SW for mild skew at n=200 and extends it: the crossover sits at moderate skew, not at the edge of saturation.

Crossover: SW minus S2 changes sign beyond two paired SE between gamma(5) (sqrt(beta1) 0.894, margin +0.0018, +4.3 SE) and gamma(10) (sqrt(beta1) 0.632, margin -0.0115, -7.1 SE).
