# Cycle 96: where the Shapiro-Wilk margin over plain S2 vanishes (gamma 100 to 5000, n=50)

Seed: 20261021 (new; Python `random.Random`, pure Python, no numpy/scipy/R available on this host).
Design: n=50, 20000 paired draws per shape. Both tests are evaluated on the same 20000 samples.

Test definitions used here:
- SW: Shapiro-Wilk W with Royston (1992) AS R94 coefficients for n=50; reject for small W.
- Plain S2: the plain (uncorrected) squared sample skewness b1 = m3^2 / m2^3 with population moments m_k = (1/n) sum (x - xbar)^k; reject for large b1.

Exact-size 5% critical values at n=50, from a separate 60000-draw N(0,1) calibration run on the same seed stream:
- SW rejects when W < 0.95421
- Plain S2 rejects when b1 > 0.41838

Separate 20000-draw N(0,1) confirmation run (binomial SE = sqrt(p(1-p)/20000)):

| test | null rejection | binomial SE |
|---|---|---|
| SW | 0.0486 | 0.0015 |
| plain S2 | 0.0464 | 0.0015 |

Both sit at 5% within one SE. Paired null difference +0.0022 (paired SE 0.0014).

## Power per gamma shape, 20000 paired draws each

| shape | sqrt(beta1) = 2/sqrt(shape) | power SW | power S2 | SW minus S2 | paired SE | z |
|---|---|---|---|---|---|---|
| 100 | 0.2000 | 0.0741 | 0.0822 | -0.0081 | 0.0016 | -4.97 |
| 200 | 0.1414 | 0.0633 | 0.0679 | -0.0047 | 0.0015 | -3.04 |
| 500 | 0.0894 | 0.0583 | 0.0576 | +0.0006 | 0.0015 | +0.43 |
| 1000 | 0.0632 | 0.0561 | 0.0565 | -0.0004 | 0.0015 | -0.23 |
| 5000 | 0.0283 | 0.0529 | 0.0505 | +0.0023 | 0.0015 | +1.58 |

Paired SE = sqrt((p10 + p01 - (p10 - p01)^2) / 20000), where p10 is the share of samples rejected by SW only and p01 the share rejected by S2 only.

## Margin against sqrt(beta1)

| sqrt(beta1) | 0.2000 | 0.1414 | 0.0894 | 0.0632 | 0.0283 |
|---|---|---|---|---|---|
| SW minus S2 | -0.0081 | -0.0047 | +0.0006 | -0.0004 | +0.0023 |
| beyond 2 paired SE? | yes, S2 ahead | yes, S2 ahead | no | no | no |

Reading: cycle 95 had SW ahead by +0.014 at gamma(50) (sqrt(beta1)=0.28). At gamma(100) and gamma(200) the sign flips and the directed skewness test is ahead of the omnibus test by about 5 and 3 paired SE. From gamma(500) down to gamma(5000) both tests sit within two paired SE of each other and within about one percentage point of the 5% null level, so neither has usable power there.

Caveat: the sign flip depends on S2 being the skewness-only statistic defined above. If an earlier cycle's "plain S2" meant a combined skew-plus-kurtosis statistic, the gamma(100) and gamma(200) rows should be rerun under that definition before the crossover is trusted.

## Closing line

Largest shape at which the SW minus S2 margin exceeds two paired SE in this sweep: none at or above gamma(100) (gamma(100): sqrt(beta1)=0.2000, margin -0.0081, paired SE 0.0016, which is S2 ahead, not SW); the margin reaches zero at a finite shape, crossing from +0.014 at gamma(50) in cycle 95 to -0.0081 at gamma(100) here, and does not stay positive down to gamma(5000).
