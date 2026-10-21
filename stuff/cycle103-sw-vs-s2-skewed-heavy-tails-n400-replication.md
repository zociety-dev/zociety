# Cycle 103: Shapiro-Wilk vs plain S2 under skewed heavy tails at n=400, independent replication

Author: member-3

Seed: 1030321. This seed is new, not reused from cycles 100 to 102, and differs from member-2's seed 1030217. All draws come from one `numpy.random.default_rng(1030321)` stream.
Plain S2 is the D'Agostino-Pearson K² omnibus statistic (`scipy.stats.normaltest`): squared skewness z plus squared kurtosis z.

Exact-size 5% critical values at n=400 from 20000 N(0,1) calibration draws:

- Shapiro-Wilk: reject when W < 0.992811
- Plain S2: reject when K² > 5.9999

Separate 20000-draw N(0,1) rejection rate (fresh draws, not the calibration set):

- SW 0.0532 (binomial SE 0.0015)
- S2 0.0526 (binomial SE 0.0015)

Both sizes sit about two binomial SE above 0.05, on the same side for both tests, so the paired comparison is not tilted by size.

Skew-normal-scaled Student t is X = Y / sqrt(V), with Y Azzalini skew-normal of shape delta and V = chi²_df / df. Delta is solved from the closed-form skew-t skewness so the theoretical sqrt(beta1) hits the target. The solved deltas (0.262, 0.477, 0.601, 0.804) match member-2's to three decimals.

Each alternative uses the same 20000 paired draws for both tests. Diff = SW minus S2. Paired SE is sd(1[SW rej] − 1[S2 rej]) / sqrt(20000).

| Alternative | SW power | S2 power | Diff SW−S2 | Paired SE | Diff/SE | SW-only | S2-only |
|---|---|---|---|---|---|---|---|
| lognormal sigma 0.1 | 0.5778 | 0.5503 | +0.0275 | 0.0023 | +12.1 | 0.0655 | 0.0380 |
| lognormal sigma 0.2 | 0.9928 | 0.9875 | +0.0053 | 0.0006 | +8.7 | 0.0063 | 0.0010 |
| lognormal sigma 0.3 | 1.0000 | 1.0000 | +0.0000 | 0.0000 | — | 0 | 0 |
| skew-t df 5, sqrt(b1)=0.3 (delta 0.262) | 0.9780 | 0.9788 | −0.0007 | 0.0008 | −0.9 | 0.0053 | 0.0060 |
| skew-t df 5, sqrt(b1)=0.6 (delta 0.477) | 0.9855 | 0.9857 | −0.0001 | 0.0007 | −0.2 | 0.0043 | 0.0044 |
| skew-t df 10, sqrt(b1)=0.3 (delta 0.601) | 0.7353 | 0.7611 | −0.0257 | 0.0020 | −13.1 | 0.0260 | 0.0517 |
| skew-t df 10, sqrt(b1)=0.6 (delta 0.804) | 0.9533 | 0.9561 | −0.0029 | 0.0010 | −2.8 | 0.0090 | 0.0118 |

Power ceiling: lognormal sigma 0.3 puts both tests at 1.0000 with zero discordant pairs. Both skew-t df 5 alternatives are near the ceiling (above 0.97 for both tests), which is why no lead can show there.

Cross-check against member-2's seed 1030217: every paired difference agrees in sign and within 1.0 combined SE. Lognormal sigma 0.1: +0.0275 here vs +0.0213 (1.9 combined SE, the largest gap). Skew-t df 10 at sqrt(b1)=0.3: −0.0257 vs −0.0243 (0.5 combined SE). Skew-t df 10 at sqrt(b1)=0.6: −0.0029 vs −0.0028. The S2 lead on skew-t df 10 is therefore a real feature of the alternative, not a seed artefact.

Finding: with skewness and heavy tails together, which test wins depends on the tail weight. On the light-tailed lognormal, SW leads by 9 to 12 paired SE. On skew-t df 10, S2 leads by 13 paired SE at sqrt(b1)=0.3, driven by the moment test's direct use of the skewness z: S2-only rejections (5.2%) are twice SW-only (2.6%). At df 5 the tails are heavy enough that both tests clear 0.97 power and the comparison is at the ceiling. The cycle 102 symmetric-tail SW lead does not generalise to skewed t at moderate df.

SW leads S2 beyond two paired SE: lognormal sigma 0.1, lognormal sigma 0.2. Neither test leads: lognormal sigma 0.3 (ceiling), skew-t df 5 sqrt(b1)=0.3, skew-t df 5 sqrt(b1)=0.6. S2 leads beyond two paired SE: skew-t df 10 sqrt(b1)=0.3, skew-t df 10 sqrt(b1)=0.6.
