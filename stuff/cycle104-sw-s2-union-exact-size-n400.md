# Cycle 104: Union of Shapiro-Wilk and plain S2 at exact 5% size, n=400

Author: member-2

Seed: 1040217. This seed is new, not reused from cycles 100 to 103 (those used 10xxxxx values ending in 0217, 0321, 0401 under cycle prefixes 100 to 103; 1040217 is a cycle 104 prefix). All draws come from one `numpy.random.default_rng(1040217)` stream.
Plain S2 is the D'Agostino-Pearson K² omnibus statistic (`scipy.stats.normaltest`): squared skewness z plus squared kurtosis z, as in cycles 101 to 103.

Exact-size 5% critical values at n=400 from 20000 N(0,1) calibration draws (the same calibration set for all three tests):

- Shapiro-Wilk alone: reject when W < 0.992709
- Plain S2 alone: reject when K² > 6.1048
- Union: reject when W < 0.992220 or K² > 6.8360

Per-component level for the union: each component is run at alpha_c = 0.035752, found by bisection on the calibration set so that the union rejects exactly 1000 of 20000 calibration draws (rate 0.0500). The two components use the same alpha_c, so neither is favoured; under the null they overlap enough that 2 × 0.0358 = 0.0715 collapses to 0.0500 for the union.

Separate 20000-draw N(0,1) rejection rate (fresh draws, not the calibration set), binomial SE 0.0015 each:

- SW 0.0491
- S2 0.0469
- Union 0.0476

All three sizes are within about two binomial SE of 0.05, so the paired comparison is not tilted by size. Under the null the single tests at 5% overlapped on 576 draws, with 405 SW-only and 363 S2-only.

Skew-normal-scaled Student t is X = Y / sqrt(V), with Y = delta·|Z0| + sqrt(1 − delta²)·Z1 (Azzalini skew-normal) and V = chi²_df / df, with delta 0.601 for df 10 at sqrt(beta1) near 0.3, the value solved in cycle 103. Lognormal is exp(sigma·Z). t df 5 is `rng.standard_t(5)`.

Each alternative uses the same 20000 paired draws for all three tests. Paired SE is sd(1[A rej] − 1[B rej]) / sqrt(20000). SW-only, S2-only and both-reject counts are at the single-test 5% critical values.

| Alternative | SW | S2 | Union | U−SW | SE | z | U−S2 | SE | z | SW-only | S2-only | both |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lognormal sigma 0.1 | 0.5702 | 0.5444 | 0.5584 | −0.0118 | 0.0017 | −7.1 | +0.0140 | 0.0018 | +7.9 | 1306 | 789 | 10098 |
| lognormal sigma 0.2 | 0.9919 | 0.9882 | 0.9905 | −0.0014 | 0.0004 | −4.1 | +0.0022 | 0.0005 | +4.8 | 94 | 21 | 19744 |
| skew-t df 10, sqrt(b1)=0.3 (delta 0.601) | 0.7325 | 0.7607 | 0.7544 | +0.0220 | 0.0015 | +14.7 | −0.0063 | 0.0014 | −4.6 | 479 | 1043 | 14171 |
| t df 5 | 0.9734 | 0.9733 | 0.9748 | +0.0014 | 0.0006 | +2.3 | +0.0014 | 0.0007 | +2.1 | 147 | 145 | 19321 |

Reading the table. Where cycle 103 found a clear single-test winner, the union lands between the two: on lognormal sigma 0.1 it gives up 0.012 against SW while gaining 0.014 over S2, and on skew-t df 10 it gives up 0.006 against S2 while gaining 0.022 over SW. The cost of the union is the tighter per-component level (0.0358 instead of 0.05), which loses more draws from the stronger test than the weaker test's extra rejections add back. The single-test SW and S2 powers reproduce cycle 103's third seed to within 1 to 2 combined SE (SW 0.5702 vs 0.5712, S2 0.7607 vs 0.7647).

The one place the union wins is t df 5, where the two single tests are tied (0.9734 vs 0.9733) and their discordant rejections are balanced (147 SW-only vs 145 S2-only). There the union picks up 0.0014 over each, at 2.3 and 2.1 paired SE. That gain is a seventh of a percentage point near the power ceiling and only just clears the bar, so a second seed should check it before it is treated as more than a tie-breaker.

Union beats both SW and S2 beyond two paired SE: t df 5 (U−SW +2.3 SE, U−S2 +2.1 SE). On lognormal sigma 0.1 and 0.2 the union is below SW and above S2; on skew-t df 10 at sqrt(b1)=0.3 the union is below S2 and above SW, so it beats neither pair there.
