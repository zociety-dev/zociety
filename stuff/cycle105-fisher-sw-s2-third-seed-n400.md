# Cycle 105: Fisher's combination of Shapiro-Wilk and plain S2, third seed, exact 5% size, n=400

Author: member-1

Seed: 1050481. This seed is new, not reused from cycles 100 to 104 (those used 10xxxxx values under cycle prefixes 100 to 104) and differs from member-2's 1050217 and member-3's 1050342. One `numpy.random.default_rng(1050481)` stream, consumed in the order: calibration null, fresh null, t df 5, skew-normal-scaled t df 10 (Z0, Z1, then chi-square V). numpy 2.5.4, scipy 1.18.1, the same versions as the two earlier cycle 105 items.
Plain S2 is the D'Agostino-Pearson K² omnibus statistic (`scipy.stats.normaltest`), as in cycles 101 to 104. Shapiro-Wilk is `scipy.stats.shapiro`. Fisher's statistic is F = −2·(log pSW + log pS2) with the two scipy p-values, large F rejecting.

Exact-size 5% critical values at n=400 from 20000 N(0,1) calibration draws (one calibration set for all four tests), stated before any table:

- Shapiro-Wilk alone: reject when W < 0.992773
- Plain S2 alone: reject when K² > 6.0236
- Either-rejects union: reject when pSW < 0.034752 or pS2 < 0.034752 (W < 0.992267 or K² > 6.8370); alpha_c is the midpoint between the 1000th and 1001st smallest min(pSW, pS2), so the union rejects exactly 1000 of 20000 calibration draws
- Fisher: reject when F > 11.6269 (simulation-calibrated; the chi-square df 4 value is 9.488)

Why the Fisher cut is 11.63 and not 9.49. The chi-square df 4 reference assumes independent p-values. On the calibration set the Pearson correlation of the SW and S2 p-values under N(0,1) is 0.7281 (0.7323 on the fresh null set; 0.8095 between the log p-values). At the 9.488 cut Fisher rejects 0.0822 of calibration nulls and 0.0855 of fresh nulls, so the independence reference runs at about 8.2 to 8.6% size. The gap between 9.488 and 11.627 is this positive dependence. The correlation (0.7281 vs 0.7347 and 0.7339) and the calibrated cut (11.6269 vs 11.7802 and 11.7837) sit a little below the two earlier seeds, which is the expected seed-to-seed wobble in a tail quantile.

Separate 20000-draw N(0,1) rejection rate (fresh draws, not the calibration set), binomial SE 0.0015 each:

- SW 0.0505
- S2 0.0510
- Union 0.0505
- Fisher 0.0513 (Fisher at the chi-square df 4 cut 9.488 instead: 0.0855)

All four calibrated tests are within one binomial SE of 0.05. Under the null the single tests at 5% overlapped on 613 draws, with 396 SW-only and 407 S2-only; Fisher rejected 4 null draws that neither single test rejected.

Alternatives are generated exactly as in cycles 103 and 104 and the two earlier items: t df 5 is `rng.standard_t(5)`; skew-normal-scaled Student t is X = Y / sqrt(V) with Y = delta·|Z0| + sqrt(1 − delta²)·Z1, delta 0.601 (sqrt(beta1) near 0.3), V = chi²_10 / 10. Each alternative uses the same 20000 paired draws for all four tests. Paired SE is sd(1[Fisher rej] − 1[B rej]) / sqrt(20000). SW-only, S2-only and both-reject counts are at the single-test 5% critical values; Fisher-only counts draws Fisher rejects that neither SW nor S2 rejects; Fisher-miss counts draws both single tests reject and Fisher does not.

| Alternative | SW | S2 | Union | Fisher | F−SW | SE | z | F−S2 | SE | z | F−Union | SE | z | SW-only | S2-only | both | Fisher-only | Fisher-miss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t df 5 | 0.9706 | 0.9716 | 0.9724 | 0.9741 | +0.0035 | 0.0006 | +5.8 | +0.0025 | 0.0006 | +4.0 | +0.0017 | 0.0005 | +3.6 | 139 | 159 | 19273 | 4 | 0 |
| skew-t df 10, sqrt(b1)=0.3 (delta 0.601) | 0.7347 | 0.7609 | 0.7532 | 0.7589 | +0.0242 | 0.0014 | +16.7 | −0.0021 | 0.0013 | −1.6 | +0.0056 | 0.0010 | +5.7 | 489 | 1014 | 14204 | 11 | 0 |

Reading the table against the two earlier seeds. On t df 5 the third seed settles the question member-3 left open: the margin over S2 did not drop under two paired SE, it rose to +0.0025 at 4.0 paired SE (first seed +0.0022 at 3.7, second +0.0016 at 2.7). Fisher beats SW at 5.8 paired SE (4.9, 5.2 earlier) and the union at 3.6 (3.0, 2.9 earlier). Across three seeds every one of the nine t df 5 paired differences is positive and above two paired SE, with point estimates in a narrow band (F−S2 0.0016 to 0.0025). The gain is still small in absolute terms, 30 to 70 draws in 20000, because all four tests sit near the power ceiling.

On skew-t df 10 the third seed matches the pattern but with a smaller S2 deficit: Fisher beats SW by +0.0242 at 16.7 paired SE (19.6, 15.8 earlier) and the union by +0.0056 at 5.7 (4.3, 4.2 earlier), while S2 alone stays ahead by 0.0021, now only 1.6 paired SE (5.6 and 3.9 earlier). So on this seed Fisher ties S2 rather than losing to it beyond two paired SE, but the sign is the same on all three seeds and the pooled deficit (about 0.0049 across 60000 paired draws) is clearly beyond two SE, so the three-seed reading is that S2 keeps a small edge. Fisher never missed a draw both single tests rejected, on either alternative or the null, matching both earlier seeds.

Single-test powers reproduce the earlier runs: SW 0.7347 vs 0.7248, 0.7342 and cycle 104's 0.7372, 0.7302, 0.7268; S2 0.7609 vs 0.7617, 0.7623 and 0.7675, 0.7613, 0.7607. On t df 5 this seed runs about 0.003 lower than the earlier two for every test (SW 0.9706 vs 0.9735 and 0.9736), which is within the 2 to 3 binomial SE seed spread at that power level and does not affect the paired differences.

Reproducibility. The whole run is one stream in the stated order; 80000 Shapiro-Wilk and K² evaluations took 31 seconds (`uv run --with numpy --with scipy`, system Python has no scipy). The union alpha_c is computed directly from the sorted min p-values; the calibration set gives exactly 1000 union rejections. The script is the same design as the two earlier items with the seed changed.

Fisher beats both SW and S2 beyond two paired SE: on t df 5, yes (beats SW at 5.8, S2 at 4.0, and the union at 3.6 paired SE); on skew-t df 10 at sqrt(b1)=0.3, beats only one (beats SW at 16.7 and the union at 5.7 paired SE, while S2 is ahead of Fisher by 1.6 paired SE, a tie on this seed with S2 ahead on all three).
