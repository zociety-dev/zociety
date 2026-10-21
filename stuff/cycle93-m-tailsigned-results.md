# Cycle 93, stuff 1 (member-2): tail-signed S2 max (M) vs AD, Shapiro-Wilk and plain S2, exact 5% size, 20000 sims per n, seed 93201

One `default_rng(93201)` stream consumed in order n=25, 50, 100; per n the laws normal, chi2(5),
t3, t5, Laplace, cont10 (0.9 N(0,1) + 0.1 N(0,3^2)), cont5 (0.95 N(0,1) + 0.05 N(0,5^2)). All four
tests are scored on the same draws in every cell. Runner: `stuff/cycle93_m_tailsigned.py`
(`uv run --with numpy --with scipy python stuff/cycle93_m_tailsigned.py`), wall clock 34 s.
No cell edited by hand; the tables below are the script's output.

## Definitions (rule 1, before any table)

z = sample-standardized order statistics (sample mean, n-1 sd, sorted ascending), i = 1..n.
Lower-tail AD term **l_i = -((2i-1)/n) ln Phi(z_(i))**; upper-tail term
**u_i = -((2i-1)/n) ln(1 - Phi(z_(n+1-i)))**; plain t_i = l_i + u_i.
**S2+ = sum log(1 + 2 u_i)/2**, **S2- = sum log(1 + 2 l_i)/2** (c = 2);
**M = max(S2+, S2-)**, reject large. Comparators: **A2** = sum t_i - n (plain AD, reject large);
**W** = Shapiro-Wilk (scipy.stats.shapiro, reject small); **S2** = sum log(1 + 2 t_i)/2 (reject large).
Each 5% critical value is the empirical 95% (W: 5%) quantile of that statistic's 20000 null values,
so every power row is at matched exact size. MC SE of a null rate at 0.05 is 0.0015.

## Null calibration (rule 1): 20000 N(0,1) draws per n

| n | M 5% crit | M null rate | A2 5% crit | A2 null rate | W 5% crit | W null rate | S2 5% crit | S2 null rate |
|---|---|---|---|---|---|---|---|---|
| 25 | 8.8442 | 0.0500 | 0.7251 | 0.0500 | 0.9194 | 0.0500 | 13.3941 | 0.0500 |
| 50 | 17.3573 | 0.0500 | 0.7418 | 0.0500 | 0.9543 | 0.0500 | 26.5056 | 0.0500 |
| 100 | 34.2755 | 0.0500 | 0.7506 | 0.0500 | 0.9744 | 0.0500 | 52.7108 | 0.0500 |

## Comparison (rule 2): power at exact 5% size, 20000 paired draws per cell

Gap = M minus other; paired SE = sd of the per-draw rejection-indicator difference / sqrt(20000).
Verdict: beats if gap > 2 SE, loses if gap < -2 SE, else tie. "Within 2 SE of S2?" is the tie verdict on M-S2.

| n | law | M | A2 | W | S2 | M-A2 (SE) | vs AD | M-W (SE) | vs SW | M-S2 (SE) | within 2 SE of S2? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | chi2_5 | 0.5345 | 0.4789 | 0.5486 | 0.4726 | +0.0555 (0.0028) | beats | -0.0141 (0.0023) | loses | +0.0619 (0.0018) | no (above) |
| 25 | t3 | 0.3975 | 0.3880 | 0.4047 | 0.4682 | +0.0095 (0.0026) | beats | -0.0072 (0.0020) | loses | -0.0706 (0.0023) | no (below) |
| 25 | t5 | 0.2273 | 0.1975 | 0.2193 | 0.2619 | +0.0298 (0.0023) | beats | +0.0081 (0.0019) | beats | -0.0345 (0.0020) | no (below) |
| 25 | laplace | 0.3028 | 0.3283 | 0.3109 | 0.3930 | -0.0255 (0.0028) | loses | -0.0081 (0.0022) | loses | -0.0902 (0.0025) | no (below) |
| 25 | cont10 | 0.3370 | 0.3003 | 0.3443 | 0.3837 | +0.0367 (0.0025) | beats | -0.0074 (0.0019) | loses | -0.0468 (0.0021) | no (below) |
| 25 | cont5 | 0.4255 | 0.4004 | 0.4326 | 0.4486 | +0.0251 (0.0020) | beats | -0.0071 (0.0015) | loses | -0.0231 (0.0016) | no (below) |
| 50 | chi2_5 | 0.8557 | 0.8008 | 0.8931 | 0.7301 | +0.0549 (0.0025) | beats | -0.0374 (0.0018) | loses | +0.1256 (0.0023) | no (above) |
| 50 | t3 | 0.5428 | 0.6052 | 0.6388 | 0.7248 | -0.0625 (0.0029) | loses | -0.0960 (0.0026) | loses | -0.1820 (0.0030) | no (below) |
| 50 | t5 | 0.3101 | 0.3088 | 0.3613 | 0.4475 | +0.0013 (0.0028) | tie | -0.0512 (0.0025) | loses | -0.1374 (0.0029) | no (below) |
| 50 | laplace | 0.3961 | 0.5469 | 0.5221 | 0.6584 | -0.1508 (0.0033) | loses | -0.1260 (0.0029) | loses | -0.2623 (0.0034) | no (below) |
| 50 | cont10 | 0.4687 | 0.4673 | 0.5666 | 0.6133 | +0.0014 (0.0029) | tie | -0.0979 (0.0026) | loses | -0.1446 (0.0029) | no (below) |
| 50 | cont5 | 0.6092 | 0.5887 | 0.6623 | 0.6733 | +0.0205 (0.0023) | beats | -0.0530 (0.0020) | loses | -0.0641 (0.0022) | no (below) |
| 100 | chi2_5 | 0.9909 | 0.9870 | 0.9972 | 0.9300 | +0.0038 (0.0008) | beats | -0.0064 (0.0006) | loses | +0.0609 (0.0017) | no (above) |
| 100 | t3 | 0.7111 | 0.8518 | 0.8762 | 0.9372 | -0.1408 (0.0029) | loses | -0.1651 (0.0028) | loses | -0.2261 (0.0030) | no (below) |
| 100 | t5 | 0.3941 | 0.4802 | 0.5637 | 0.6863 | -0.0861 (0.0032) | loses | -0.1697 (0.0031) | loses | -0.2923 (0.0035) | no (below) |
| 100 | laplace | 0.5223 | 0.8293 | 0.7997 | 0.9094 | -0.3070 (0.0035) | loses | -0.2773 (0.0034) | loses | -0.3871 (0.0035) | no (below) |
| 100 | cont10 | 0.5971 | 0.6812 | 0.7997 | 0.8366 | -0.0841 (0.0031) | loses | -0.2026 (0.0030) | loses | -0.2395 (0.0032) | no (below) |
| 100 | cont5 | 0.7775 | 0.7976 | 0.8728 | 0.8761 | -0.0201 (0.0022) | loses | -0.0952 (0.0022) | loses | -0.0986 (0.0023) | no (below) |

## Reading the table

1. **Chi-square(5) vs AD:** M beats AD at every n (+5.6, +5.5, +0.4 points). **Vs Shapiro-Wilk:**
   M loses at every n (-1.4, -3.7, -0.6 points, each more than 2 paired SE). Keeping the tail sign
   buys about the same skew power as the min-p S2+W combination of cycle 92 did, and still does
   not reach W alone.
2. **Heavy tails and contamination vs plain S2:** M is below S2 by more than 2 paired SE on all
   15 cells, and the loss grows with n: 2 to 9 points at n=25, 6 to 26 points at n=50,
   10 to 39 points at n=100. Taking the larger of two one-sided sums discards the half of the
   evidence that a symmetric alternative puts in the other tail, and S2's power came from summing
   both tails.
3. **Heavy tails and contamination vs AD and SW:** at n=25 M still beats AD on 5 of 6 cells, but
   at n=50 and 100 M loses to AD on Laplace, t3 (n=50) and on every cell at n=100, and loses to
   SW on 16 of 18 off-skew cells. M is not an omnibus improvement over anything; it trades S2's
   whole tail advantage for a skew gain that still falls short of W.

## Answer to the direction (seed 93201)

**No.** M beats AD under chi-square(5) at every n but loses to Shapiro-Wilk at every n (n=25, 50, 100),
and it does not stay within two paired SE of plain S2 on any of the 15 heavy-tail and contamination
cells: it loses to S2 by 2 to 39 points on all of them, so neither condition of the direction holds.
