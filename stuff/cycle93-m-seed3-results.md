# Cycle 93, stuff 3 (member-1): third-seed replication of the tail-signed S2 max (M), seed 93403

Same runner as stuff 2 with only the seed changed (`stuff/cycle93_m_seed3.py`,
`uv run --with numpy --with scipy python stuff/cycle93_m_seed3.py`, wall clock 39 s). 20000 sims per
cell; per n: null (calibration), independent null (out-of-sample size), then chi2(5), t3, t5, Laplace,
cont10 (0.9 N(0,1) + 0.1 N(0,9)), cont5 (0.95 N(0,1) + 0.05 N(0,25)). All four tests are scored on the
same draws in every cell. Tables are the script's output, unedited.

## Definitions (rule 1, before any table)

z = sample-standardized order statistics (sample mean, n-1 sd, sorted ascending), i = 1..n.
Lower-tail AD term **l_i = -((2i-1)/n) ln Phi(z_(i))**; upper-tail term
**u_i = -((2i-1)/n) ln(1 - Phi(z_(n+1-i)))**; plain t_i = l_i + u_i.
**S2+ = sum log(1 + 2 u_i)/2**, **S2- = sum log(1 + 2 l_i)/2** (c = 2); **M = max(S2+, S2-)**, reject
large. Comparators: **A2** = sum t_i - n (plain AD, reject large); **W** = Shapiro-Wilk (reject small);
**S2** = sum log(1 + 2 t_i)/2 (reject large). Each 5% critical value is the empirical 95% (W: 5%)
quantile of that statistic's 20000 null values, so in-sample null rates are 0.0500 by construction;
the out-of-sample table tests calibration (MC SE 0.0015 at 0.05).

## Calibration, out-of-sample size, power with paired SE (rules 1 and 2), and paired SE cross-check

Gap = M minus other; paired SE = sd of the per-draw rejection-indicator difference / sqrt(20000);
beats if gap > 2 SE, loses if gap < -2 SE, else tie.

| n | M 5% crit | M null rate | A2 5% crit | A2 null rate | W 5% crit | W null rate | S2 5% crit | S2 null rate |
|---|---|---|---|---|---|---|---|---|
| 25 | 8.8426 | 0.0500 | 0.7213 | 0.0500 | 0.9194 | 0.0500 | 13.3934 | 0.0500 |
| 50 | 17.3552 | 0.0500 | 0.7489 | 0.0500 | 0.9543 | 0.0500 | 26.5066 | 0.0500 |
| 100 | 34.2707 | 0.0500 | 0.7428 | 0.0500 | 0.9745 | 0.0500 | 52.7056 | 0.0500 |

| n | M oos size | A2 oos size | W oos size | S2 oos size |
|---|---|---|---|---|
| 25 | 0.0525 | 0.0525 | 0.0510 | 0.0502 |
| 50 | 0.0483 | 0.0450 | 0.0491 | 0.0471 |
| 100 | 0.0488 | 0.0505 | 0.0490 | 0.0509 |

| n | law | M | A2 | W | S2 | M-A2 (SE) | vs AD | M-W (SE) | vs SW | M-S2 (SE) | within 2 SE of S2? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | chi2_5 | 0.5367 | 0.4802 | 0.5484 | 0.4699 | +0.0565 (0.0030) | beats | -0.0117 (0.0024) | loses | +0.0668 (0.0019) | no (above) |
| 25 | t3 | 0.3947 | 0.3889 | 0.4027 | 0.4664 | +0.0058 (0.0026) | beats | -0.0080 (0.0020) | loses | -0.0717 (0.0024) | no (below) |
| 25 | t5 | 0.2286 | 0.1984 | 0.2182 | 0.2671 | +0.0302 (0.0024) | beats | +0.0103 (0.0018) | beats | -0.0385 (0.0021) | no (below) |
| 25 | laplace | 0.2969 | 0.3306 | 0.3093 | 0.3891 | -0.0337 (0.0028) | loses | -0.0124 (0.0022) | loses | -0.0922 (0.0025) | no (below) |
| 25 | cont10 | 0.3329 | 0.2962 | 0.3373 | 0.3769 | +0.0367 (0.0025) | beats | -0.0044 (0.0019) | loses | -0.0440 (0.0021) | no (below) |
| 25 | cont5 | 0.4242 | 0.3953 | 0.4279 | 0.4471 | +0.0289 (0.0021) | beats | -0.0037 (0.0016) | loses | -0.0228 (0.0017) | no (below) |
| 50 | chi2_5 | 0.8543 | 0.8021 | 0.8929 | 0.7306 | +0.0522 (0.0025) | beats | -0.0386 (0.0019) | loses | +0.1237 (0.0023) | no (above) |
| 50 | t3 | 0.5444 | 0.6004 | 0.6369 | 0.7257 | -0.0560 (0.0029) | loses | -0.0926 (0.0026) | loses | -0.1814 (0.0030) | no (below) |
| 50 | t5 | 0.3106 | 0.2977 | 0.3605 | 0.4442 | +0.0129 (0.0029) | beats | -0.0499 (0.0025) | loses | -0.1336 (0.0029) | no (below) |
| 50 | laplace | 0.4040 | 0.5405 | 0.5265 | 0.6586 | -0.1365 (0.0033) | loses | -0.1225 (0.0029) | loses | -0.2546 (0.0033) | no (below) |
| 50 | cont10 | 0.4677 | 0.4602 | 0.5631 | 0.6106 | +0.0076 (0.0029) | beats | -0.0953 (0.0026) | loses | -0.1429 (0.0029) | no (below) |
| 50 | cont5 | 0.6064 | 0.5845 | 0.6623 | 0.6715 | +0.0220 (0.0023) | beats | -0.0559 (0.0020) | loses | -0.0651 (0.0021) | no (below) |
| 100 | chi2_5 | 0.9920 | 0.9868 | 0.9976 | 0.9296 | +0.0052 (0.0008) | beats | -0.0056 (0.0006) | loses | +0.0624 (0.0017) | no (above) |
| 100 | t3 | 0.7088 | 0.8508 | 0.8761 | 0.9375 | -0.1421 (0.0029) | loses | -0.1673 (0.0028) | loses | -0.2287 (0.0030) | no (below) |
| 100 | t5 | 0.3959 | 0.4800 | 0.5618 | 0.6826 | -0.0841 (0.0032) | loses | -0.1659 (0.0031) | loses | -0.2867 (0.0035) | no (below) |
| 100 | laplace | 0.5275 | 0.8262 | 0.7945 | 0.9119 | -0.2987 (0.0035) | loses | -0.2670 (0.0033) | loses | -0.3844 (0.0035) | no (below) |
| 100 | cont10 | 0.5910 | 0.6810 | 0.7973 | 0.8350 | -0.0900 (0.0031) | loses | -0.2063 (0.0030) | loses | -0.2440 (0.0032) | no (below) |
| 100 | cont5 | 0.7808 | 0.8058 | 0.8767 | 0.8783 | -0.0251 (0.0022) | loses | -0.0959 (0.0022) | loses | -0.0976 (0.0023) | no (below) |

| n | law | M-A2 paired SE (indicator sd) | closed form | unpaired SE | M-S2 paired SE | closed form | unpaired SE |
|---|---|---|---|---|---|---|---|
| 25 | chi2_5 | 0.00295 | 0.00295 | 0.00499 | 0.00190 | 0.00190 | 0.00499 |
| 25 | t3 | 0.00256 | 0.00256 | 0.00488 | 0.00236 | 0.00236 | 0.00494 |
| 25 | t5 | 0.00236 | 0.00236 | 0.00409 | 0.00208 | 0.00208 | 0.00431 |
| 25 | laplace | 0.00276 | 0.00276 | 0.00464 | 0.00253 | 0.00253 | 0.00472 |
| 25 | cont10 | 0.00249 | 0.00249 | 0.00464 | 0.00209 | 0.00209 | 0.00478 |
| 25 | cont5 | 0.00209 | 0.00209 | 0.00492 | 0.00167 | 0.00167 | 0.00496 |
| 50 | chi2_5 | 0.00248 | 0.00248 | 0.00376 | 0.00233 | 0.00233 | 0.00401 |
| 50 | t3 | 0.00288 | 0.00288 | 0.00494 | 0.00297 | 0.00297 | 0.00473 |
| 50 | t5 | 0.00286 | 0.00286 | 0.00460 | 0.00293 | 0.00293 | 0.00480 |
| 50 | laplace | 0.00332 | 0.00332 | 0.00495 | 0.00334 | 0.00334 | 0.00483 |
| 50 | cont10 | 0.00292 | 0.00292 | 0.00499 | 0.00287 | 0.00287 | 0.00493 |
| 50 | cont5 | 0.00230 | 0.00230 | 0.00491 | 0.00214 | 0.00214 | 0.00479 |
| 100 | chi2_5 | 0.00083 | 0.00083 | 0.00102 | 0.00171 | 0.00171 | 0.00192 |
| 100 | t3 | 0.00291 | 0.00291 | 0.00408 | 0.00304 | 0.00304 | 0.00364 |
| 100 | t5 | 0.00323 | 0.00323 | 0.00494 | 0.00347 | 0.00347 | 0.00477 |
| 100 | laplace | 0.00349 | 0.00349 | 0.00443 | 0.00350 | 0.00350 | 0.00406 |
| 100 | cont10 | 0.00313 | 0.00313 | 0.00479 | 0.00321 | 0.00321 | 0.00436 |
| 100 | cont5 | 0.00219 | 0.00219 | 0.00405 | 0.00228 | 0.00228 | 0.00373 |


## Three-seed agreement (seeds 93201, 93302, 93403)

Out-of-sample sizes are all within 0.0050 of 0.05 (worst A2 at n=50, 0.0450, 3.3 SE conservative;
M worst 0.0525). M critical values agree with both earlier seeds to within 0.012 at every n.
Every chi-square(5) verdict is the same on all three seeds: M beats AD (+0.057, +0.052, +0.005) and
loses to SW (-0.012, -0.039, -0.006) at every n, each beyond two paired SE. Every M-S2 verdict on the
15 heavy-tail and contamination cells is the same on all three seeds: below, by 0.023 to 0.384.
The only seed-sensitive verdicts are M vs AD at n=50 under t5 and cont10 (tie, loses/tie, and now
beats at +0.013 and +0.008): the true gap there is near zero.

Why the max fails: on symmetric heavy tails both S2+ and S2- carry evidence, and the max keeps only
one while its critical value (about 0.65 of S2's) is set for the larger of two near-independent sums,
so M discards roughly half the signal S2 pools. Under chi2(5) only the upper tail carries signal and M
beats S2 and AD but still not W, whose skew sensitivity is not confined to the extreme order
statistics. Tail-signing by max is exhausted; any further S2 variant needs a pooled statistic, not a
selected one.

## Closing line (rule 2)

No: under a third seed M again beats AD but loses to Shapiro-Wilk under chi-square(5) at every n by
more than two paired SE, and falls below plain S2 by more than two paired SE on all 15 heavy-tail and
contamination cells; the direction fails on both clauses, identically on all three seeds.
