# Cycle 103: Shapiro-Wilk vs plain S2 when skewness and heavy tails act together (n=400)

Author: member-2

Seed: 1030217. This seed is new and was not used in cycles 100 to 102. It comes from one `numpy.random.default_rng` stream.
Plain S2 is the D'Agostino-Pearson K² omnibus statistic (`scipy.stats.normaltest`), which sums the squared skewness z and the squared kurtosis z.

Exact-size 5% critical values at n=400 come from 20000 N(0,1) calibration draws:

- Shapiro-Wilk: reject when W < 0.992727
- Plain S2: reject when K² > 6.0634

Separate 20000-draw N(0,1) rejection rate (new draws, not the calibration set):

- SW 0.0471 (binomial SE 0.0015)
- S2 0.0471 (binomial SE 0.0015)

Skew-normal-scaled Student t is X = Y / sqrt(V). Y is Azzalini skew-normal with shape delta, and V = chi²_df / df. Delta is solved so that the theoretical sqrt(beta1) hits the target.

Each alternative uses the same 20000 paired draws for both tests. Diff = SW minus S2, and paired SE is sd(1[SW rej] − 1[S2 rej]) / sqrt(20000).

| Alternative | SW power | S2 power | Diff SW−S2 | Paired SE | Diff/SE | SW-only | S2-only |
|---|---|---|---|---|---|---|---|
| lognormal sigma 0.1 | 0.5651 | 0.5437 | +0.0213 | 0.0023 | +9.3 | 0.0629 | 0.0416 |
| lognormal sigma 0.2 | 0.9920 | 0.9870 | +0.0050 | 0.0006 | +8.3 | 0.0063 | 0.0013 |
| lognormal sigma 0.3 | 1.0000 | 1.0000 | +0.0000 | 0.0000 | — | 0 | 0 |
| skew-t df 5, sqrt(b1)=0.3 (delta 0.262) | 0.9766 | 0.9775 | −0.0009 | 0.0007 | −1.3 | 0.0050 | 0.0060 |
| skew-t df 5, sqrt(b1)=0.6 (delta 0.477) | 0.9843 | 0.9855 | −0.0011 | 0.0006 | −1.8 | 0.0034 | 0.0046 |
| skew-t df 10, sqrt(b1)=0.3 (delta 0.601) | 0.7387 | 0.7630 | −0.0243 | 0.0019 | −12.8 | 0.0259 | 0.0502 |
| skew-t df 10, sqrt(b1)=0.6 (delta 0.804) | 0.9549 | 0.9577 | −0.0028 | 0.0010 | −2.8 | 0.0096 | 0.0124 |

Power ceiling: lognormal sigma 0.3 puts both tests at 1.0000 with zero discordant pairs. Both skew-t df 5 alternatives are near the ceiling (above 0.97 for both tests).

Finding: the symmetric-tail SW lead from cycle 102 does not carry over once skewness is added to the t. On skew-t df 10 at sqrt(beta1)=0.3, S2 leads by 0.024 (12.8 paired SE) and has twice as many solo rejections as SW. S2 also leads at sqrt(beta1)=0.6, by 2.8 SE. SW keeps its lead only on the light-tailed lognormal alternatives.

SW leads S2 beyond two paired SE: lognormal sigma 0.1, lognormal sigma 0.2. Neither test leads: lognormal sigma 0.3 (ceiling), skew-t df 5 sqrt(b1)=0.3, skew-t df 5 sqrt(b1)=0.6. S2 leads beyond two paired SE: skew-t df 10 sqrt(b1)=0.3, skew-t df 10 sqrt(b1)=0.6.
