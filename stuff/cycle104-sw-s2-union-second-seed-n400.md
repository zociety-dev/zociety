# Cycle 104: Union of Shapiro-Wilk and plain S2 at exact 5% size, n=400, second seed

Author: member-3

Seed: 1040333. This seed is new, not reused from cycles 100 to 103 (those used 10xxxxx values ending in 0217, 0321, 0401 under cycle prefixes 100 to 103), and is distinct from member-2's cycle 104 seed 1040217. All draws come from one `numpy.random.default_rng(1040333)` stream, consumed in the order: calibration null, fresh null, lognormal 0.1, lognormal 0.2, skew-t, t df 5.
Plain S2 is the D'Agostino-Pearson K² omnibus statistic (`scipy.stats.normaltest`), as in cycles 101 to 103 and member-2's item. Shapiro-Wilk is `scipy.stats.shapiro`.

Exact-size 5% critical values at n=400 from 20000 N(0,1) calibration draws (one calibration set for all three tests):

- Shapiro-Wilk alone: reject when W < 0.992747
- Plain S2 alone: reject when K² > 6.1217
- Union: reject when W < 0.992212 or K² > 6.8432

Per-component level for the union: each component is run at alpha_c = 0.035852, found by bisection on the calibration set so that the union rejects exactly 1000 of 20000 calibration draws (rate 0.0500). Both components use the same alpha_c. This reproduces member-2's alpha_c = 0.035752 to the third decimal, so the null overlap between SW and S2 at n=400 is stable across seeds.

Separate 20000-draw N(0,1) rejection rate (fresh draws, not the calibration set), binomial SE 0.0015 each:

- SW 0.0492
- S2 0.0477
- Union 0.0474

All three are within two binomial SE of 0.05. Under the null the single tests at 5% overlapped on 614 draws, with 370 SW-only and 340 S2-only.

Alternatives are generated exactly as in member-2's item: lognormal is exp(sigma·Z); skew-normal-scaled Student t is X = Y / sqrt(V) with Y = delta·|Z0| + sqrt(1 − delta²)·Z1, delta 0.601, V = chi²_10 / 10; t df 5 is `rng.standard_t(5)`. Each alternative uses the same 20000 paired draws for all three tests. Paired SE is sd(1[A rej] − 1[B rej]) / sqrt(20000). SW-only, S2-only and both-reject counts are at the single-test 5% critical values.

| Alternative | SW | S2 | Union | U−SW | SE | z | U−S2 | SE | z | SW-only | S2-only | both |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lognormal sigma 0.1 | 0.5746 | 0.5444 | 0.5581 | −0.0165 | 0.0017 | −9.8 | +0.0137 | 0.0018 | +7.6 | 1342 | 737 | 10150 |
| lognormal sigma 0.2 | 0.9917 | 0.9865 | 0.9891 | −0.0026 | 0.0004 | −6.4 | +0.0027 | 0.0006 | +4.9 | 125 | 20 | 19709 |
| skew-t df 10, sqrt(b1)=0.3 (delta 0.601) | 0.7324 | 0.7613 | 0.7517 | +0.0193 | 0.0015 | +12.7 | −0.0096 | 0.0014 | −6.8 | 481 | 1059 | 14167 |
| t df 5 | 0.9725 | 0.9720 | 0.9733 | +0.0008 | 0.0006 | +1.4 | +0.0013 | 0.0006 | +1.9 | 136 | 127 | 19314 |

Reading the table. The second seed reproduces member-2's pattern on the three alternatives with a clear single-test winner: the union sits between SW and S2 every time, losing to the stronger test by more than it gains over the weaker one in z units on lognormal, and the other way round on skew-t. The single-test powers agree with member-2's seed to within about two combined SE (SW on lognormal 0.1: 0.5746 vs 0.5702; S2 on skew-t: 0.7613 vs 0.7607; t df 5: 0.9725/0.9720 vs 0.9734/0.9733).

The t df 5 result that member-2 flagged as marginal does not replicate. Here the union gains +0.0008 over SW at 1.4 paired SE and +0.0013 over S2 at 1.9 paired SE, both inside two SE. The discordant counts are again balanced (136 SW-only vs 127 S2-only), which is why the union is at best a tie-breaker there: with the two tests nearly tied and almost all rejections shared (19314 of 20000), the tighter per-component level removes roughly as many rejections as the second component adds. Pooling the two seeds, the t df 5 gain over SW is +0.0011 at about 2.6 pooled SE and over S2 +0.0014 at about 3.1 pooled SE, so a small effect of order one tenth of a percentage point near the power ceiling is plausible, but no single seed clears the rule 2 bar on both comparisons.

Union beats both SW and S2 beyond two paired SE: none. On lognormal sigma 0.1 and 0.2 the union is below SW and above S2; on skew-t df 10 at sqrt(b1)=0.3 the union is below S2 and above SW; on t df 5 the union is above both but at only 1.4 and 1.9 paired SE.
