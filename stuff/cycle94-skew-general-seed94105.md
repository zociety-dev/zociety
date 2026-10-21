# Cycle 94, stuff 3 (member-1): third-seed replication of SW vs plain AD vs plain S2 on skew, seed 94105

Same runner as stuff 1 (`stuff/cycle94_skew_general.py`) with only `SEED = 94201` changed to
`SEED = 94105`, run from a copy outside the repo with `uv run --with numpy --with scipy python -I`;
the committed script is unchanged. 20000 paired draws per cell, one `default_rng(94105)` stream
consumed in order n=25, 50, 100, laws normal, chi2(2), chi2(10), lognormal(0, 0.5), beta(2, 5).
Definitions, exact-size calibration (empirical null quantile per statistic) and verdict rule (beats
if gap > 2 paired SE, loses if gap < -2 paired SE, else tie) are unchanged. Wall clock 25 s.
Tables are the script's output verbatim.

## Seed and exact-size 5% critical values (rule 2): seed 94105, 20000 N(0,1) draws per n

| n | W 5% crit | W null rate | A2 5% crit | A2 null rate | S2 5% crit | S2 null rate |
|---|---|---|---|---|---|---|
| 25 | 0.9192 | 0.0500 | 0.7260 | 0.0500 | 13.3951 | 0.0500 |
| 50 | 0.9534 | 0.0500 | 0.7415 | 0.0500 | 26.5091 | 0.0500 |
| 100 | 0.9749 | 0.0500 | 0.7430 | 0.0500 | 52.7091 | 0.0500 |

All three null rates are exactly 0.0500 by construction. W and S2 critical values agree with seeds
94201 and 94303 to within 0.0007 and 0.007. The A2 critical value at n=100 is 0.7430 against 0.7605
for seed 94303, a 0.0175 shift: the A2 null upper tail is long, so its empirical 95th percentile is
the least stable of the three. It does not change any power verdict below.

## Power at exact 5% size (rule 1), 20000 paired draws per cell

| n | law | SW | AD | S2 | SW-AD (SE) | vs AD | SW-S2 (SE) | vs S2 |
|---|---|---|---|---|---|---|---|---|
| 25 | chi2_2 | 0.9233 | 0.8767 | 0.8363 | +0.0466 (0.0015) | beats | +0.0870 (0.0020) | beats |
| 25 | chi2_10 | 0.3023 | 0.2578 | 0.2682 | +0.0445 (0.0020) | beats | +0.0341 (0.0018) | beats |
| 25 | lognormal_0_0.5 | 0.6303 | 0.5722 | 0.5802 | +0.0581 (0.0020) | beats | +0.0501 (0.0019) | beats |
| 25 | beta_2_5 | 0.2182 | 0.1871 | 0.1422 | +0.0311 (0.0018) | beats | +0.0759 (0.0021) | beats |
| 50 | chi2_2 | 0.9993 | 0.9966 | 0.9802 | +0.0027 (0.0004) | beats | +0.0192 (0.0010) | beats |
| 50 | chi2_10 | 0.5814 | 0.4807 | 0.4415 | +0.1007 (0.0025) | beats | +0.1398 (0.0026) | beats |
| 50 | lognormal_0_0.5 | 0.9196 | 0.8701 | 0.8311 | +0.0495 (0.0017) | beats | +0.0886 (0.0020) | beats |
| 50 | beta_2_5 | 0.4869 | 0.3940 | 0.2139 | +0.0928 (0.0024) | beats | +0.2730 (0.0032) | beats |
| 100 | chi2_2 | 1.0000 | 1.0000 | 0.9997 | +0.0000 (0.0000) | tie | +0.0003 (0.0001) | beats |
| 100 | chi2_10 | 0.9070 | 0.8077 | 0.6696 | +0.0993 (0.0022) | beats | +0.2373 (0.0030) | beats |
| 100 | lognormal_0_0.5 | 0.9990 | 0.9945 | 0.9754 | +0.0044 (0.0005) | beats | +0.0236 (0.0011) | beats |
| 100 | beta_2_5 | 0.9061 | 0.7641 | 0.3191 | +0.1420 (0.0025) | beats | +0.5870 (0.0035) | beats |

## Replication against seeds 94201 and 94303

1. **23 of 24 verdicts match both earlier seeds.** The one difference is SW minus S2 at chi2(2),
   n=100: here +0.0003 with paired SE 0.0001 (6 discordant draws out of 20000, SW rejecting where
   S2 does not, none the other way), which the rule calls "beats" at 3 SE; seeds 94201 and 94303
   had +0.0001 (0.0001) and called it a tie. This is a saturation cell where SW rejects all 20000
   draws and S2 rejects 19994, so the verdict flips on a handful of draws. It is not evidence of a
   real gap and should be read as a tie in substance.
2. **SW minus AD at chi2(2), n=100 is a tie again**, as in both earlier seeds: both reject every
   draw, gap and SE are both zero.
3. **Largest power shift between this seed and either earlier seed is 0.0181** (SW, beta(2, 5),
   n=50: 0.4869 here against 0.5050 for seed 94201), about 3.9 SE of an independent-seed difference
   (sqrt(2) x 0.0033). Next largest is 0.0172 (AD, beta(2, 5), n=100, against seed 94303). Both are
   in beta(2, 5), the law with the lowest SW power at n=25, and neither moves a verdict: the smallest
   non-saturated SW gap in this seed is +0.0027 (0.0004) at chi2(2), n=50, 6.8 SE.
4. **SW never loses.** No cell at any n has SW below AD or S2 by more than two paired SE; no cell
   has SW below either test by any amount.

## Closing line (rule 2)

SW does not win every skew cell at every n: it beats AD and S2 in 23 of 24 cells and ties SW minus
AD at chi-square(2), n=100 (paired difference +0.0000, 0.0 paired SE, both tests reject all 20000
draws); the SW minus S2 verdict at that same cell is a 3.0 SE "beats" on 6 discordant draws that the
two earlier seeds scored as a tie, and SW loses nowhere. Across three seeds the answer to the
direction is the same: SW's skew advantage is general, not specific to chi-square(5).
