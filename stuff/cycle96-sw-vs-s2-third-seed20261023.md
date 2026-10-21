# Cycle 96: SW vs plain S2, gamma(100) to gamma(5000), third seed 20261023

Third run of the cycle 96 sweep, after `cycle96-sw-vs-s2-gamma100-5000-seed20261021.md` and `cycle96-sw-vs-s2-replication-seed20261022.md`. The question is whether the S2 lead at gamma(100) and gamma(200) survives a third seed, and whether any of the near-null rows (500, 1000, 5000) is more than noise.

**Seed:** 20261023 (paired sweep), 20261024 (null calibration stream), 20261025 (separate N(0,1) size check). **n:** 50. **Paired draws per shape:** 20000. **Null calibration:** 60000 N(0,1) draws.
**Exact-size 5% critical values at n=50:** Shapiro-Wilk rejects when W < 0.95415. Plain S2 (squared sample skewness b1 = m3^2 / m2^3, skewness only) rejects when b1 > 0.41682.

Method: pure Python, Royston (1992) AS R94 coefficients for the SW weights, `random.gammavariate` for the draws. Each replicate draws one gamma(shape) sample of 50 and scores it with both tests. The paired SE is sd(I_SW - I_S2)/sqrt(20000). Total run time about 6 seconds.

## N(0,1) size check (separate 20000 draws)

| test | rejection rate | binomial SE |
|---|---|---|
| SW | 0.0523 | 0.0015 |
| S2 | 0.0518 | 0.0015 |

Both tests sit within 1.6 SE of 0.05. The paired difference is +0.0005 (paired SE 0.0015).

## Power and margin against sqrt(beta1) = 2/sqrt(shape)

| shape | sqrt(beta1) | SW | S2 | SW - S2 | paired SE | z |
|---|---|---|---|---|---|---|
| 100 | 0.2000 | 0.0770 | 0.0837 | -0.0066 | 0.0016 | -4.05 |
| 200 | 0.1414 | 0.0653 | 0.0664 | -0.0010 | 0.0015 | -0.68 |
| 500 | 0.0894 | 0.0538 | 0.0555 | -0.0017 | 0.0015 | -1.14 |
| 1000 | 0.0632 | 0.0534 | 0.0521 | +0.0013 | 0.0015 | +0.89 |
| 5000 | 0.0283 | 0.0479 | 0.0491 | -0.0013 | 0.0014 | -0.88 |

## Across the three seeds

| shape | z (20261021) | z (20261022) | z (20261023) |
|---|---|---|---|
| 100 | about -5 | -5.85 | -4.05 |
| 200 | about -3 | -3.53 | -0.68 |
| 500 | within 2 | -1.59 | -1.14 |
| 1000 | within 2 | -2.64 | +0.89 |
| 5000 | within 2 | -1.34 | -0.88 |

The gamma(100) row is the only one that is stable: S2 beats SW by 4 to 6 paired SE on every seed, with a margin of about -0.007 to -0.010. The gamma(200) lead for S2 is weaker here (-0.68 SE) than on the first two seeds, so the true margin at gamma(200) is small, likely between -0.001 and -0.005, and this seed happens to land near zero.

The gamma(1000) row from seed 20261022 (S2 ahead by 2.6 SE) does not replicate: this seed gives SW ahead by 0.9 SE. That confirms the earlier reading that it was noise. From gamma(500) down, both tests reject at roughly 5% and no seed separates them beyond two SE in a consistent direction.

**Closing line (rule 2):** no shape from gamma(100) to gamma(5000) has SW ahead by more than two paired SE on this seed. The largest shape where SW leads beyond two paired SE remains gamma(50) from cycle 95 (sqrt(beta1)=0.28, margin +0.014, paired SE about 0.0018, about 8 paired SE). The margin reaches zero at a finite shape between gamma(50) and gamma(100), turns negative at gamma(100) on all three seeds, and is indistinguishable from zero from gamma(500) down to gamma(5000).
