# Cycle 96: SW vs plain S2, gamma(100) to gamma(5000), replication on seed 20261022

This reruns the sweep in `cycle96-sw-vs-s2-gamma100-5000-seed20261021.md` with a fresh seed. It checks whether the sign flip found there, where S2 beats SW at mild skew, holds up.

**Seed:** 20261022. **n:** 50. **Paired draws per shape:** 20000. **Null calibration:** 60000 N(0,1) draws.
**Exact-size 5% critical values at n=50:** Shapiro-Wilk rejects when W < 0.95401. Plain S2 (squared sample skewness b1, skewness-only) rejects when b1 > 0.41603.

Method: pure Python, with Royston (1992) AS R94 SW coefficients. Each replicate draws one gamma(shape) sample of 50 and scores it with both tests. The paired SE is sd(I_SW - I_S2)/sqrt(20000).

## N(0,1) size check (separate 20000 draws)

| test | rejection rate | binomial SE |
|---|---|---|
| SW | 0.0485 | 0.0015 |
| S2 | 0.0495 | 0.0015 |

Both tests are within one SE of 0.05. The paired difference is -0.0010 (paired SE 0.0015).

## Power and margin against sqrt(beta1) = 2/sqrt(shape)

| shape | sqrt(beta1) | SW | S2 | SW - S2 | paired SE | z |
|---|---|---|---|---|---|---|
| 100 | 0.2000 | 0.0747 | 0.0843 | -0.0096 | 0.0016 | -5.85 |
| 200 | 0.1414 | 0.0626 | 0.0683 | -0.0056 | 0.0016 | -3.53 |
| 500 | 0.0894 | 0.0576 | 0.0600 | -0.0023 | 0.0015 | -1.59 |
| 1000 | 0.0632 | 0.0498 | 0.0536 | -0.0038 | 0.0014 | -2.64 |
| 5000 | 0.0283 | 0.0490 | 0.0510 | -0.0020 | 0.0015 | -1.34 |

## Agreement with seed 20261021

The sign flip replicates. With this seed S2 beats SW by 5.9 paired SE at gamma(100) and by 3.5 at gamma(200). The original seed gave about 5 and 3. All five margins are negative, so SW is ahead at no shape.

The gamma(1000) row is the one new detail. There S2 is ahead by 2.6 paired SE, while gamma(500) and gamma(5000) stay within two SE. One row past two SE out of three near-null rows is consistent with noise, because the true power of both tests is close to 5% at that shape.

**Closing line (rule 2):** no shape from gamma(100) to gamma(5000) has SW ahead by more than two paired SE. The largest shape where SW leads beyond two SE is still gamma(50) from cycle 95 (sqrt(beta1)=0.28, +0.014, about 8 paired SE). The margin reaches zero at a finite shape between gamma(50) and gamma(100), then turns negative.
