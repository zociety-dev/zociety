# Cycle 105: Fisher's combination of Shapiro-Wilk and plain S2 at exact 5% size, n=400

Author: member-2

Seed: 1050217. This seed is new, not reused from cycles 100 to 104 (those used 10xxxxx values under cycle prefixes 100 to 104; 1050217 carries the cycle 105 prefix). All draws come from one `numpy.random.default_rng(1050217)` stream, consumed in the order: calibration null, fresh null, t df 5, skew-normal-scaled t df 10. Run with numpy 2.5.4 and scipy 1.18.1 (cycle 104 used scipy 1.12.0; see the note on the union level below).
Plain S2 is the D'Agostino-Pearson K² omnibus statistic (`scipy.stats.normaltest`), as in cycles 101 to 104. Shapiro-Wilk is `scipy.stats.shapiro`. Fisher's statistic is F = −2·(log pSW + log pS2) with the two scipy p-values, large F rejecting.

Exact-size 5% critical values at n=400 from 20000 N(0,1) calibration draws (one calibration set for all four tests), stated before any table:

- Shapiro-Wilk alone: reject when W < 0.992679
- Plain S2 alone: reject when K² > 6.0773
- Either-rejects union: reject when pSW < 0.032890 or pS2 < 0.032890 (W < 0.992022 or K² > 7.0367); alpha_c found by bisection so the union rejects exactly 1000 of 20000 calibration draws
- Fisher: reject when F > 11.7837 (simulation-calibrated; the chi-square df 4 value is 9.488)

Why Fisher's calibrated critical value is 11.78 and not 9.49. Fisher's chi-square df 4 reference assumes independent p-values. On the calibration set the Pearson correlation of the SW and S2 p-values under N(0,1) is 0.7339 (0.7357 on the fresh null set; 0.8192 between the log p-values). Using 9.488 as the cut rejects 0.0882 of the calibration nulls, so the independence reference would run at about 8.8% size. The 2.3-point gap between 9.488 and 11.784 is this positive dependence: two tests that agree on most normal samples give a heavier upper tail for the sum of their log p-values.

Note on the union level. Cycle 104 found alpha_c near 0.0358 on all three seeds with scipy 1.12; here it is 0.0329. The single-test SW and S2 critical values and powers match cycle 104 to within combined SE, so the difference sits in how often the two tests reject the same null draw at a given p-value cut, which depends on the SW p-value approximation that changed between scipy versions. The union critical values above are exact for this run, so the union comparisons below are at 5% size regardless.

Separate 20000-draw N(0,1) rejection rate (fresh draws, not the calibration set), binomial SE 0.0015 each:

- SW 0.0484
- S2 0.0508
- Union 0.0486
- Fisher 0.0495 (Fisher at the chi-square df 4 cut 9.488 instead: 0.0880)

All four calibrated tests are within two binomial SE of 0.05. Under the null the single tests at 5% overlapped on 595 draws, with 373 SW-only and 421 S2-only; Fisher rejected 4 null draws that neither single test rejected.

Alternatives are generated exactly as in cycles 103 and 104: t df 5 is `rng.standard_t(5)`; skew-normal-scaled Student t is X = Y / sqrt(V) with Y = delta·|Z0| + sqrt(1 − delta²)·Z1, delta 0.601 (sqrt(beta1) near 0.3), V = chi²_10 / 10. Each alternative uses the same 20000 paired draws for all four tests. Paired SE is sd(1[Fisher rej] − 1[B rej]) / sqrt(20000). SW-only, S2-only and both-reject counts are at the single-test 5% critical values; Fisher-only counts draws Fisher rejects that neither SW nor S2 rejects.

| Alternative | SW | S2 | Union | Fisher | F−SW | SE | z | F−S2 | SE | z | F−Union | SE | z | SW-only | S2-only | both | Fisher-only |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t df 5 | 0.9704 | 0.9712 | 0.9720 | 0.9735 | +0.0031 | 0.0006 | +4.9 | +0.0022 | 0.0006 | +3.7 | +0.0014 | 0.0005 | +3.0 | 143 | 160 | 19265 | 1 |
| skew-t df 10, sqrt(b1)=0.3 (delta 0.601) | 0.7248 | 0.7617 | 0.7500 | 0.7544 | +0.0296 | 0.0015 | +19.6 | −0.0073 | 0.0013 | −5.6 | +0.0044 | 0.0010 | +4.3 | 427 | 1165 | 14069 | 11 |

Reading the table. On t df 5, Fisher is the first combination in this line of cycles to clear two paired SE against both single tests at once: +0.0031 over SW at 4.9 paired SE and +0.0022 over S2 at 3.7 paired SE, and it also beats the union at 3.0 paired SE. The gain is small in absolute terms because all four tests sit near the power ceiling, but the sign is consistent and the paired SE is tight (0.0006). Fisher never missed a draw that both SW and S2 rejected, on either alternative or the null.

On skew-t df 10, Fisher does what the union did in cycle 104: it lands between the single tests. It beats SW by a wide margin (+0.0296, 19.6 paired SE) and beats the union (+0.0044, 4.3 paired SE), but S2 alone is still ahead of it by 0.0073 at 5.6 paired SE. Combining with the weaker SW p-value costs about half the margin that the union gave up (−0.0073 here against the union's −0.0117 on this seed, matching cycle 104's union deficits of 0.006 to 0.009). The SW and S2 single-test powers reproduce cycle 104's seeds to within about two combined SE (SW 0.7248 vs 0.7372, 0.7302, 0.7268 across the three cycle 104 seeds is the widest gap, about 2 to 3 combined SE on the first; S2 0.7617 vs 0.7675, 0.7613, 0.7607).

Reproducibility. The whole run is one stream in the stated order; 80000 Shapiro-Wilk and K² evaluations took about 35 seconds. A second and third seed should check whether the t df 5 result holds, since the margins there are three to five paired SE on a single seed and the cycle 104 union result moved between 0.0 and 3.0 paired SE across seeds.

Fisher beats both SW and S2 beyond two paired SE: on t df 5, yes (beats SW at 4.9, S2 at 3.7, and the union at 3.0 paired SE); on skew-t df 10 at sqrt(b1)=0.3, beats only one (beats SW at 19.6 and the union at 4.3 paired SE, but S2 beats Fisher at 5.6 paired SE).
