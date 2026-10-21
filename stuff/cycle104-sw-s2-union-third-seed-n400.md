# Cycle 104: Union of Shapiro-Wilk and plain S2 at exact 5% size, n=400, third seed

Author: member-1

Seed: 1040555. This seed is new, not reused from cycles 100 to 103 (those used 10xxxxx values ending in 0217, 0321, 0401 under cycle prefixes 100 to 103), and is distinct from the cycle 104 seeds 1040217 (member-2) and 1040333 (member-3). All draws come from one `numpy.random.default_rng(1040555)` stream, consumed in the order: calibration null, fresh null, lognormal 0.1, lognormal 0.2, skew-t, t df 5. Run with numpy 1.26.4 and scipy 1.12.0.
Plain S2 is the D'Agostino-Pearson K² omnibus statistic (`scipy.stats.normaltest`), as in cycles 101 to 103 and the two earlier cycle 104 items. Shapiro-Wilk is `scipy.stats.shapiro`.

Exact-size 5% critical values at n=400 from 20000 N(0,1) calibration draws (one calibration set for all three tests):

- Shapiro-Wilk alone: reject when W < 0.992777
- Plain S2 alone: reject when K² > 6.0042
- Union: reject when W < 0.992275 or K² > 6.7925

Per-component level for the union: each component is run at alpha_c = 0.035852, found by bisection on the calibration set so that the union rejects exactly 1000 of 20000 calibration draws (rate 0.0500). Both components use the same alpha_c. This matches member-3's 0.035852 to six decimals and member-2's 0.035752 to the third decimal, so the null overlap of SW and S2 at n=400 is stable across all three seeds.

Separate 20000-draw N(0,1) rejection rate (fresh draws, not the calibration set), binomial SE 0.0015 each:

- SW 0.0513
- S2 0.0527
- Union 0.0517

All three are within two binomial SE of 0.05. Under the null the single tests at 5% overlapped on 654 draws, with 373 SW-only and 399 S2-only.

Alternatives are generated exactly as in the two earlier items: lognormal is exp(sigma·Z); skew-normal-scaled Student t is X = Y / sqrt(V) with Y = delta·|Z0| + sqrt(1 − delta²)·Z1, delta 0.601, V = chi²_10 / 10; t df 5 is `rng.standard_t(5)`. Each alternative uses the same 20000 paired draws for all three tests. Paired SE is sd(1[A rej] − 1[B rej]) / sqrt(20000). SW-only, S2-only and both-reject counts are at the single-test 5% critical values.

| Alternative | SW | S2 | Union | U−SW | SE | z | U−S2 | SE | z | SW-only | S2-only | both |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lognormal sigma 0.1 | 0.5756 | 0.5520 | 0.5618 | −0.0138 | 0.0016 | −8.7 | +0.0099 | 0.0018 | +5.4 | 1256 | 783 | 10256 |
| lognormal sigma 0.2 | 0.9914 | 0.9876 | 0.9897 | −0.0018 | 0.0004 | −4.5 | +0.0021 | 0.0005 | +4.1 | 102 | 26 | 19726 |
| skew-t df 10, sqrt(b1)=0.3 (delta 0.601) | 0.7372 | 0.7675 | 0.7587 | +0.0215 | 0.0015 | +14.2 | −0.0088 | 0.0014 | −6.2 | 482 | 1087 | 14263 |
| t df 5 | 0.9725 | 0.9741 | 0.9741 | +0.0017 | 0.0006 | +3.0 | +0.0000 | 0.0006 | +0.0 | 102 | 136 | 19347 |

Reading the table. The third seed reproduces the pattern of both earlier items on the three alternatives with a clear single-test winner: the union lands between SW and S2 each time. On lognormal sigma 0.1 and 0.2 it is below SW and above S2 beyond four paired SE on every comparison; on skew-t df 10 it is below S2 at 6.2 paired SE and above SW at 14.2. The single-test powers agree with the earlier seeds to within about two combined SE (SW on lognormal 0.1: 0.5756 vs 0.5746 and 0.5702; S2 on skew-t: 0.7675 vs 0.7613 and 0.7607).

On t df 5 the union again fails to beat both tests. This seed happens to have S2 ahead of SW by 0.0016, and the union exactly ties S2 (both 0.9741, zero discordant net) while beating SW at 3.0 paired SE. The three seeds now show the union gaining over SW by +0.0014, +0.0008 and +0.0017 and over S2 by +0.0014, +0.0013 and +0.0000. Pooling the three with paired SE near 0.0006 each gives roughly +0.0013 at about 3.7 pooled SE over SW and +0.0009 at about 2.6 pooled SE over S2. So a real gain of order one tenth of a percentage point near the power ceiling is likely, but it is below the resolution of a single 20000-draw seed, and in no single seed does the union clear two paired SE against both tests at once.

Union beats both SW and S2 beyond two paired SE: none. On lognormal sigma 0.1 and 0.2 the union is below SW and above S2; on skew-t df 10 at sqrt(b1)=0.3 the union is below S2 and above SW; on t df 5 the union is above SW at 3.0 paired SE but ties S2 at 0.0 paired SE.
