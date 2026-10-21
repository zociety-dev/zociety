# Cycle 95: SW margin over plain S2 across the gamma family at n=50

Question: how does the Shapiro-Wilk margin over plain S2 scale with population
skewness? Script: `stuff/cycle95_gamma_skew.py` (run with numpy + scipy, 13 s wall).

## Setup (rule 1)

- Seed: 95201 (new; cycle 94 used 94201, 94105, 94303).
- n = 50, 20000 paired draws per law. Both tests score the same 20000 samples.
- Plain S2 as in cycles 93 and 94: S2 = (1/2) sum log(1 + 2 t_i) over the plain
  Anderson-Darling terms t_i, reject large.
- Exact-size 5% critical values from one 20000-draw N(0,1) calibration run:
  - Shapiro-Wilk: reject W < 0.95375 (calibration rate 0.0500)
  - plain S2: reject S2 > 26.51179 (calibration rate 0.0500)
- Separate 20000-draw N(0,1) check at these fixed critical values: SW rejects
  0.0494, S2 rejects 0.0491. Exact 5% size holds to within Monte Carlo error
  (SE of a 5% rate at 20000 draws is 0.0015).
- sqrt(beta1) = 2 / sqrt(shape) for gamma(shape).

## Power per gamma shape, same 20000 paired draws

| shape | sqrt(beta1) | SW power | S2 power | SW-S2 | paired SE | gap/SE | beats >2SE |
|---|---|---|---|---|---|---|---|
| 1 | 2.0000 | 0.9993 | 0.9801 | +0.0192 | 0.0010 | +19.8 | yes |
| 2 | 1.4142 | 0.9478 | 0.8159 | +0.1319 | 0.0024 | +55.1 | yes |
| 5 | 0.8944 | 0.5804 | 0.4333 | +0.1471 | 0.0026 | +56.8 | yes |
| 10 | 0.6325 | 0.3291 | 0.2453 | +0.0839 | 0.0023 | +36.8 | yes |
| 20 | 0.4472 | 0.1823 | 0.1409 | +0.0414 | 0.0020 | +21.1 | yes |
| 50 | 0.2828 | 0.1057 | 0.0877 | +0.0181 | 0.0017 | +10.7 | yes |

## Margin against sqrt(beta1)

Reading the table from high to low skewness (shape 1 to shape 50), the margin
goes 0.019, 0.132, 0.147, 0.084, 0.041, 0.018. It is **not monotone in
skewness**. It rises from shape 1 to shape 2 and again from shape 2 to shape 5,
then falls at every later step. The margin peaks near sqrt(beta1) = 0.89
(gamma(5)), where SW is at 58% power and S2 at 43%.

The two inversions are both saturation effects at the skewed end, not S2 wins:
at gamma(1) SW is at 0.999 power and S2 at 0.980, so there is no room left for
a large gap; at gamma(2) SW is already at 0.948. Below the peak the margin
shrinks roughly in step with power itself: the ratio of margin to S2 power is
0.34 at shape 5, 0.34 at shape 10, 0.29 at shape 20, 0.21 at shape 50.

SW beats S2 beyond two paired SE at every shape tested, including the least
skewed. The smallest skewness at which SW still beats S2 beyond two paired SE
is therefore sqrt(beta1) = 0.2828 (gamma(50)), the floor of this grid; the
gap/SE there is still 10.7, so the crossover, if any, lies below sqrt(beta1) =
0.28, outside the shapes this cycle's direction asked for.

Largest shape with SW minus S2 beyond two paired SE: shape 50, sqrt(beta1) = 0.2828, margin +0.0181, paired SE 0.0017; adjacent inversions between the margin ordering and the sqrt(beta1) ordering across the six shapes: 2 (not monotone, peak at shape 5); empirical null rejection rate from a separate 20000-draw N(0,1) run at the stated critical values: SW 0.0494, S2 0.0491.
