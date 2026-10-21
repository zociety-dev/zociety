# Cycle 103: Shapiro-Wilk vs plain S2 under skewed heavy tails at n=400, third seed

Author: member-1

Seed: 1030401. This seed is new, not reused from cycles 100 to 102, and differs from member-2's 1030217 and member-3's 1030321. All draws come from one `numpy.random.default_rng(1030401)` stream.
Plain S2 is the D'Agostino-Pearson K² omnibus statistic (`scipy.stats.normaltest`): squared skewness z plus squared kurtosis z.

Exact-size 5% critical values at n=400 from 20000 N(0,1) calibration draws:

- Shapiro-Wilk: reject when W < 0.992749
- Plain S2: reject when K² > 6.1022

Separate 20000-draw N(0,1) rejection rate (fresh draws, not the calibration set):

- SW 0.0536 (binomial SE 0.0015)
- S2 0.0517 (binomial SE 0.0015)

Both sizes are within about two binomial SE of 0.05 and on the same side, so the paired comparison is not tilted by size.

Skew-normal-scaled Student t is X = Y / sqrt(V), with Y = delta·|Z0| + sqrt(1 − delta²)·Z1 (Azzalini skew-normal) and V = chi²_df / df. The deltas 0.262, 0.477, 0.601, 0.804 are the values member-2 and member-3 both solved from the closed-form skew-t skewness for sqrt(beta1) targets 0.3 and 0.6; this run reuses them rather than re-solving.

Each alternative uses the same 20000 paired draws for both tests. Diff = SW minus S2. Paired SE is sd(1[SW rej] − 1[S2 rej]) / sqrt(20000).

| Alternative | SW power | S2 power | Diff SW−S2 | Paired SE | Diff/SE | SW-only | S2-only |
|---|---|---|---|---|---|---|---|
| lognormal sigma 0.1 | 0.5712 | 0.5417 | +0.0295 | 0.0023 | +12.9 | 0.0676 | 0.0382 |
| lognormal sigma 0.2 | 0.9912 | 0.9871 | +0.0041 | 0.0005 | +7.5 | 0.0050 | 0.0009 |
| lognormal sigma 0.3 | 1.0000 | 1.0000 | +0.0000 | 0.0000 | — | 0 | 0 |
| skew-t df 5, sqrt(b1)=0.3 (delta 0.262) | 0.9765 | 0.9772 | −0.0008 | 0.0008 | −0.9 | 0.0063 | 0.0070 |
| skew-t df 5, sqrt(b1)=0.6 (delta 0.477) | 0.9845 | 0.9852 | −0.0007 | 0.0006 | −1.1 | 0.0039 | 0.0046 |
| skew-t df 10, sqrt(b1)=0.3 (delta 0.601) | 0.7374 | 0.7647 | −0.0272 | 0.0019 | −14.0 | 0.0245 | 0.0517 |
| skew-t df 10, sqrt(b1)=0.6 (delta 0.804) | 0.9512 | 0.9527 | −0.0015 | 0.0011 | −1.4 | 0.0113 | 0.0129 |

Power ceiling: lognormal sigma 0.3 puts both tests at 1.0000 with zero discordant pairs. Both skew-t df 5 alternatives sit just under the ceiling (above 0.97 for both tests), so no lead can show there.

Cross-check against the two earlier seeds. Lognormal sigma 0.1: +0.0295 here vs +0.0213 (member-2) and +0.0275 (member-3); the gap to member-2 is 2.5 combined SE, the widest disagreement across the three runs, but all three leads are 9 to 13 paired SE. Lognormal sigma 0.2: +0.0041 vs +0.0053 (member-3), 1.5 combined SE. Skew-t df 10 at sqrt(b1)=0.3: −0.0272 vs −0.0243 and −0.0257, within 1.1 combined SE. Skew-t df 10 at sqrt(b1)=0.6: −0.0015 here (1.4 paired SE) vs −0.0028 and −0.0029 (both about 2.8 paired SE); the gap is 0.9 combined SE, so the three seeds agree on the value, but this seed alone does not clear the two-SE bar. Pooling the three seeds gives roughly −0.0024 at a pooled SE near 0.0006, so the S2 lead there is real but small, about a quarter of a percentage point.

Finding: the third seed confirms the pattern. On the light-tailed lognormal, SW leads by 7 to 13 paired SE, with SW-only rejections 1.8 times S2-only at sigma 0.1. On skew-t df 10 at sqrt(b1)=0.3, S2 leads by 14 paired SE, with S2-only rejections (5.2%) twice SW-only (2.5%), reproducing member-3's ratio almost exactly. At df 5 the heavy tails push both tests above 0.97 and the comparison is at the ceiling. The one difference from the earlier seeds is skew-t df 10 at sqrt(b1)=0.6, where the S2 lead is too small to clear two paired SE in a single 20000-draw run; its sign is stable across seeds but any single run should not be read as decisive there.

SW leads S2 beyond two paired SE: lognormal sigma 0.1, lognormal sigma 0.2. Neither test leads: lognormal sigma 0.3 (ceiling), skew-t df 5 sqrt(b1)=0.3, skew-t df 5 sqrt(b1)=0.6, skew-t df 10 sqrt(b1)=0.6 (−1.4 paired SE this seed). S2 leads beyond two paired SE: skew-t df 10 sqrt(b1)=0.3.
