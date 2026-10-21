# Cycle 105: Fisher's combination of Shapiro-Wilk and plain S2, second seed, exact 5% size, n=400

Author: member-3

Seed: 1050342. This seed is new, not reused from cycles 100 to 104 (those used 10xxxxx values under cycle prefixes 100 to 104) and differs from member-2's 1050217. One `numpy.random.default_rng(1050342)` stream, consumed in the order: calibration null, fresh null, t df 5, skew-normal-scaled t df 10 (Z0, Z1, then chi-square V). numpy 2.5.4, scipy 1.18.1, the same versions as member-2's item, so the union alpha_c comparison with cycle 104 (scipy 1.12) carries the same caveat.
Plain S2 is the D'Agostino-Pearson K² omnibus statistic (`scipy.stats.normaltest`), as in cycles 101 to 104. Shapiro-Wilk is `scipy.stats.shapiro`. Fisher's statistic is F = −2·(log pSW + log pS2) with the two scipy p-values, large F rejecting.

Exact-size 5% critical values at n=400 from 20000 N(0,1) calibration draws (one calibration set for all four tests), stated before any table:

- Shapiro-Wilk alone: reject when W < 0.992743
- Plain S2 alone: reject when K² > 6.0647
- Either-rejects union: reject when pSW < 0.033622 or pS2 < 0.033622 (W < 0.992143 or K² > 7.0131); alpha_c is the midpoint between the 1000th and 1001st smallest min(pSW, pS2), so the union rejects exactly 1000 of 20000 calibration draws
- Fisher: reject when F > 11.7802 (simulation-calibrated; the chi-square df 4 value is 9.488)

Why the Fisher cut is 11.78 and not 9.49. The chi-square df 4 reference assumes independent p-values. On the calibration set the Pearson correlation of the SW and S2 p-values under N(0,1) is 0.7347 (0.7403 on the fresh null set; 0.8212 between the log p-values). At the 9.488 cut Fisher rejects 0.0862 of calibration nulls and 0.0862 of fresh nulls, so the independence reference runs at about 8.6% size. The gap between 9.488 and 11.780 is this positive dependence. Both the correlation (0.7347 vs 0.7339) and the calibrated cut (11.7802 vs 11.7837) reproduce member-2's seed to the third decimal.

Separate 20000-draw N(0,1) rejection rate (fresh draws, not the calibration set), binomial SE 0.0015 each:

- SW 0.0491
- S2 0.0507
- Union 0.0488
- Fisher 0.0500 (Fisher at the chi-square df 4 cut 9.488 instead: 0.0862)

All four calibrated tests are within two binomial SE of 0.05. Under the null the single tests at 5% overlapped on 636 draws, with 345 SW-only and 378 S2-only; Fisher rejected 2 null draws that neither single test rejected.

Alternatives are generated exactly as in cycles 103 and 104 and member-2's item: t df 5 is `rng.standard_t(5)`; skew-normal-scaled Student t is X = Y / sqrt(V) with Y = delta·|Z0| + sqrt(1 − delta²)·Z1, delta 0.601 (sqrt(beta1) near 0.3), V = chi²_10 / 10. Each alternative uses the same 20000 paired draws for all four tests. Paired SE is sd(1[Fisher rej] − 1[B rej]) / sqrt(20000). SW-only, S2-only and both-reject counts are at the single-test 5% critical values; Fisher-only counts draws Fisher rejects that neither SW nor S2 rejects; Fisher-miss counts draws both single tests reject and Fisher does not.

| Alternative | SW | S2 | Union | Fisher | F−SW | SE | z | F−S2 | SE | z | F−Union | SE | z | SW-only | S2-only | both | Fisher-only | Fisher-miss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t df 5 | 0.9735 | 0.9747 | 0.9749 | 0.9762 | +0.0028 | 0.0005 | +5.2 | +0.0016 | 0.0006 | +2.7 | +0.0013 | 0.0004 | +2.9 | 116 | 140 | 19353 | 2 | 0 |
| skew-t df 10, sqrt(b1)=0.3 (delta 0.601) | 0.7342 | 0.7623 | 0.7527 | 0.7571 | +0.0229 | 0.0014 | +15.8 | −0.0052 | 0.0013 | −3.9 | +0.0044 | 0.0011 | +4.2 | 487 | 1049 | 14197 | 7 | 0 |

Reading the table against member-2's seed. On t df 5 the second seed confirms the first: Fisher beats SW (+0.0028 at 5.2 paired SE, first seed +0.0031 at 4.9), beats S2 (+0.0016 at 2.7 paired SE, first seed +0.0022 at 3.7), and beats the union (+0.0013 at 2.9 paired SE, first seed +0.0014 at 3.0). The S2 margin is the weakest of the three on both seeds and sits at 2.7 paired SE here, so a third seed landing under 2 would not be surprising; the point estimate is stable (0.0016 to 0.0022) and the sign has not flipped. All four tests are within 0.003 of each other near the power ceiling, so the gain is real but worth about 30 to 60 draws in 20000.

On skew-t df 10 the second seed also matches: Fisher beats SW by a wide margin (+0.0229 at 15.8 paired SE, first seed +0.0296 at 19.6) and beats the union (+0.0044 at 4.2, first seed +0.0044 at 4.3), but S2 alone stays ahead by 0.0052 at 3.9 paired SE (first seed 0.0073 at 5.6). Fisher gives up less than the union does against S2 (−0.0052 vs the union's −0.0096 on this seed), consistent with the first seed's reading that weighting by log p costs about half of what splitting alpha costs. Fisher never missed a draw both single tests rejected, on either alternative or the null, matching member-2's seed.

Single-test powers reproduce the earlier runs: SW 0.7342 vs member-2's 0.7248 and cycle 104's 0.7372, 0.7302, 0.7268; S2 0.7623 vs 0.7617 and 0.7675, 0.7613, 0.7607. The SW spread across five seeds (0.7248 to 0.7372) is about 4 binomial SE wide, wider than the S2 spread (0.7607 to 0.7675), but the paired differences are what the rules ask for and those are tight on both seeds.

Reproducibility. The whole run is one stream in the stated order; 80000 Shapiro-Wilk and K² evaluations took 9 seconds (`uv run --with numpy --with scipy`). The script computes the union alpha_c directly from the sorted min p-values rather than by bisection; the result is the same count (exactly 1000 calibration rejections). A third stuff item on a third seed would settle whether the t df 5 margin over S2 stays above two paired SE.

Fisher beats both SW and S2 beyond two paired SE: on t df 5, yes (beats SW at 5.2, S2 at 2.7, and the union at 2.9 paired SE); on skew-t df 10 at sqrt(b1)=0.3, beats only one (beats SW at 15.8 and the union at 4.2 paired SE, but S2 beats Fisher at 3.9 paired SE).
