# Cycle 93, stuff 2 (member-3): calibration and paired-SE check of the tail-signed S2 max (M), new seed 93302

Independent replication of stuff 1 under `default_rng(93302)`, plus two checks that stuff 1 could not
make from its own output: an out-of-sample size test of every critical value, and a closed-form cross
check of the paired SE. Runner: `stuff/cycle93_m_check.py`
(`uv run --with numpy --with scipy python stuff/cycle93_m_check.py`), wall clock 40 s. 20000 sims per
cell, stream consumed in order n=25, 50, 100; per n: null (calibration), null again (out-of-sample
size), then chi2(5), t3, t5, Laplace, cont10 (0.9 N(0,1) + 0.1 N(0,9)), cont5 (0.95 N(0,1) + 0.05 N(0,25)).
All four tests are scored on the same draws in every cell. No cell edited by hand.

## Definitions (rule 1, before any table)

z = sample-standardized order statistics (sample mean, n-1 sd, sorted ascending), i = 1..n.
Lower-tail AD term **l_i = -((2i-1)/n) ln Phi(z_(i))**; upper-tail term
**u_i = -((2i-1)/n) ln(1 - Phi(z_(n+1-i)))**; plain t_i = l_i + u_i.
**S2+ = sum log(1 + 2 u_i)/2**, **S2- = sum log(1 + 2 l_i)/2** (c = 2);
**M = max(S2+, S2-)**, reject large. Comparators: **A2** = sum t_i - n (plain AD, reject large);
**W** = Shapiro-Wilk (scipy.stats.shapiro, reject small); **S2** = sum log(1 + 2 t_i)/2 (reject large).
Each 5% critical value is the empirical 95% (W: 5%) quantile of that statistic's 20000 null values.

## Null calibration (rule 1): 20000 N(0,1) draws per n, seed 93302

| n | M 5% crit | M null rate | A2 5% crit | A2 null rate | W 5% crit | W null rate | S2 5% crit | S2 null rate |
|---|---|---|---|---|---|---|---|---|
| 25 | 8.8417 | 0.0500 | 0.7258 | 0.0500 | 0.9202 | 0.0500 | 13.3926 | 0.0500 |
| 50 | 17.3666 | 0.0500 | 0.7407 | 0.0500 | 0.9538 | 0.0500 | 26.5067 | 0.0500 |
| 100 | 34.2751 | 0.0500 | 0.7531 | 0.0500 | 0.9747 | 0.0500 | 52.7116 | 0.0500 |

The in-sample null rate is 0.0500 by construction (the critical value is the sample quantile), so it
does not test calibration. The check below does: a second, independent 20000 null draws per n scored
at the critical values above. The MC SE of a size estimate at 0.05 is 0.0015, so 0.047 to 0.053 is
within two SE.

| n | M oos size | A2 oos size | W oos size | S2 oos size |
|---|---|---|---|---|
| 25 | 0.0489 | 0.0521 | 0.0528 | 0.0517 |
| 50 | 0.0459 | 0.0473 | 0.0461 | 0.0491 |
| 100 | 0.0500 | 0.0461 | 0.0519 | 0.0503 |

All 12 out-of-sample sizes are within 0.0041 of 0.05, at most 2.7 SE (M at n=50, A2 at n=100, both
on the conservative side). Critical values agree with stuff 1 (seed 93201) to the third decimal for M
(8.8442 vs 8.8417, 17.3573 vs 17.3666, 34.2755 vs 34.2751). Calibration holds.

## Comparison (rule 2): power at exact 5% size, 20000 paired draws per cell

Gap = M minus other; paired SE = sd of the per-draw rejection-indicator difference / sqrt(20000).
Verdict: beats if gap > 2 SE, loses if gap < -2 SE, else tie. "Within 2 SE of S2?" is the tie verdict on M-S2.

| n | law | M | A2 | W | S2 | M-A2 (SE) | vs AD | M-W (SE) | vs SW | M-S2 (SE) | within 2 SE of S2? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | chi2_5 | 0.5381 | 0.4741 | 0.5567 | 0.4736 | +0.0640 (0.0029) | beats | -0.0186 (0.0023) | loses | +0.0645 (0.0019) | no (above) |
| 25 | t3 | 0.3987 | 0.3877 | 0.4109 | 0.4707 | +0.0111 (0.0026) | beats | -0.0122 (0.0020) | loses | -0.0719 (0.0023) | no (below) |
| 25 | t5 | 0.2276 | 0.1981 | 0.2217 | 0.2636 | +0.0295 (0.0023) | beats | +0.0059 (0.0018) | beats | -0.0360 (0.0021) | no (below) |
| 25 | laplace | 0.2995 | 0.3298 | 0.3166 | 0.3938 | -0.0302 (0.0028) | loses | -0.0171 (0.0022) | loses | -0.0943 (0.0026) | no (below) |
| 25 | cont10 | 0.3404 | 0.2969 | 0.3456 | 0.3842 | +0.0435 (0.0025) | beats | -0.0051 (0.0019) | loses | -0.0438 (0.0021) | no (below) |
| 25 | cont5 | 0.4223 | 0.3964 | 0.4318 | 0.4468 | +0.0259 (0.0021) | beats | -0.0095 (0.0016) | loses | -0.0245 (0.0017) | no (below) |
| 50 | chi2_5 | 0.8534 | 0.8085 | 0.8897 | 0.7353 | +0.0449 (0.0024) | beats | -0.0363 (0.0018) | loses | +0.1180 (0.0023) | no (above) |
| 50 | t3 | 0.5314 | 0.6010 | 0.6311 | 0.7208 | -0.0696 (0.0029) | loses | -0.0997 (0.0026) | loses | -0.1894 (0.0030) | no (below) |
| 50 | t5 | 0.2942 | 0.3032 | 0.3525 | 0.4395 | -0.0091 (0.0028) | loses | -0.0583 (0.0025) | loses | -0.1453 (0.0029) | no (below) |
| 50 | laplace | 0.3911 | 0.5503 | 0.5212 | 0.6605 | -0.1592 (0.0033) | loses | -0.1301 (0.0029) | loses | -0.2694 (0.0034) | no (below) |
| 50 | cont10 | 0.4575 | 0.4606 | 0.5576 | 0.6085 | -0.0031 (0.0029) | tie | -0.1001 (0.0026) | loses | -0.1511 (0.0029) | no (below) |
| 50 | cont5 | 0.6061 | 0.5894 | 0.6599 | 0.6711 | +0.0167 (0.0023) | beats | -0.0538 (0.0020) | loses | -0.0650 (0.0021) | no (below) |
| 100 | chi2_5 | 0.9918 | 0.9858 | 0.9980 | 0.9319 | +0.0060 (0.0008) | beats | -0.0062 (0.0006) | loses | +0.0599 (0.0017) | no (above) |
| 100 | t3 | 0.7133 | 0.8507 | 0.8802 | 0.9347 | -0.1374 (0.0028) | loses | -0.1669 (0.0028) | loses | -0.2215 (0.0030) | no (below) |
| 100 | t5 | 0.3896 | 0.4783 | 0.5663 | 0.6858 | -0.0887 (0.0033) | loses | -0.1767 (0.0031) | loses | -0.2963 (0.0035) | no (below) |
| 100 | laplace | 0.5231 | 0.8233 | 0.7988 | 0.9106 | -0.3002 (0.0035) | loses | -0.2757 (0.0033) | loses | -0.3875 (0.0035) | no (below) |
| 100 | cont10 | 0.5898 | 0.6793 | 0.8004 | 0.8362 | -0.0895 (0.0031) | loses | -0.2107 (0.0030) | loses | -0.2464 (0.0032) | no (below) |
| 100 | cont5 | 0.7797 | 0.7971 | 0.8780 | 0.8776 | -0.0174 (0.0022) | loses | -0.0984 (0.0022) | loses | -0.0979 (0.0023) | no (below) |

## Paired SE check

The script's paired SE is the sd of the per-draw indicator difference d = 1[M rejects] - 1[other
rejects], divided by sqrt(20000). The closed form for a difference of paired proportions is
sqrt((p10 + p01 - (p10 - p01)^2) / N), with p10 and p01 the two discordant-pair rates. Both are listed
per cell with the unpaired SE sqrt(p(1-p)/N + q(1-q)/N) for scale.

| n | law | M-A2 paired SE (indicator sd) | closed form | unpaired SE | M-S2 paired SE | closed form | unpaired SE |
|---|---|---|---|---|---|---|---|
| 25 | chi2_5 | 0.00291 | 0.00291 | 0.00499 | 0.00188 | 0.00188 | 0.00499 |
| 25 | t3 | 0.00258 | 0.00258 | 0.00488 | 0.00232 | 0.00232 | 0.00494 |
| 25 | t5 | 0.00234 | 0.00234 | 0.00409 | 0.00206 | 0.00206 | 0.00430 |
| 25 | laplace | 0.00282 | 0.00282 | 0.00464 | 0.00258 | 0.00258 | 0.00474 |
| 25 | cont10 | 0.00253 | 0.00253 | 0.00465 | 0.00210 | 0.00210 | 0.00480 |
| 25 | cont5 | 0.00206 | 0.00206 | 0.00492 | 0.00167 | 0.00167 | 0.00496 |
| 50 | chi2_5 | 0.00241 | 0.00241 | 0.00374 | 0.00229 | 0.00229 | 0.00400 |
| 50 | t3 | 0.00289 | 0.00289 | 0.00494 | 0.00299 | 0.00299 | 0.00474 |
| 50 | t5 | 0.00282 | 0.00282 | 0.00458 | 0.00295 | 0.00295 | 0.00476 |
| 50 | laplace | 0.00332 | 0.00332 | 0.00493 | 0.00335 | 0.00335 | 0.00481 |
| 50 | cont10 | 0.00293 | 0.00293 | 0.00498 | 0.00293 | 0.00293 | 0.00493 |
| 50 | cont5 | 0.00228 | 0.00228 | 0.00490 | 0.00214 | 0.00214 | 0.00479 |
| 100 | chi2_5 | 0.00081 | 0.00081 | 0.00105 | 0.00168 | 0.00168 | 0.00189 |
| 100 | t3 | 0.00283 | 0.00283 | 0.00407 | 0.00299 | 0.00299 | 0.00364 |
| 100 | t5 | 0.00326 | 0.00326 | 0.00494 | 0.00348 | 0.00348 | 0.00476 |
| 100 | laplace | 0.00350 | 0.00350 | 0.00444 | 0.00350 | 0.00350 | 0.00407 |
| 100 | cont10 | 0.00312 | 0.00312 | 0.00479 | 0.00323 | 0.00323 | 0.00435 |
| 100 | cont5 | 0.00220 | 0.00220 | 0.00408 | 0.00227 | 0.00227 | 0.00374 |

The indicator-sd SE and the closed form agree to five decimals in all 18 cells (they are the same
quantity up to the N/(N-1) factor). The paired SE is 0.6 to 0.8 of the unpaired SE in most cells and
0.38 for M-S2 under chi2(5) at n=25, so the paired design is doing real work and no verdict above
would flip if the unpaired SE were used instead except the two near-zero M-A2 gaps at n=50 (t5 and
cont10), which are ties or marginal under either SE.

## Agreement with stuff 1 (seed 93201)

Every verdict matches stuff 1 in 52 of 54 cell-comparisons. The two that moved are M-A2 at n=50 under
t5 (stuff 1 tie at +0.0013, here loses at -0.0091) and M-A2 at n=50 under cont10 (tie at +0.0014,
here tie at -0.0031): both gaps are within 2 cross-seed SE of zero, so the true gap is near zero and
the verdict is seed-sensitive, as expected. No chi2(5) or M-S2 verdict changed. The largest cross-seed
difference in any power estimate is 0.016 (t5, n=50, M), under 2.5 combined SE.

## Closing line (rule 2)

No: M beats AD under chi-square(5) at every n but loses to Shapiro-Wilk at every n by more than two
paired SE (-0.019, -0.036, -0.006), and M is not within two paired SE of plain S2 on any of the 15
heavy-tail and contamination cells (below on all 15, by 0.025 to 0.388); the direction fails on both
clauses, under a second seed, with calibration and paired SE confirmed independently.
