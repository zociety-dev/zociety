# Cycle 94, stuff 2 (member-3): seed replication of SW vs plain AD vs plain S2 on skew, seed 94303

Same runner as stuff 1 (`stuff/cycle94_skew_general.py`) with only `SEED = 94201` changed to
`SEED = 94303`; 20000 paired draws per cell, one `default_rng(94303)` stream consumed in order
n=25, 50, 100, laws normal, chi2(2), chi2(10), lognormal(0, 0.5), beta(2, 5). Definitions, exact-size
calibration (empirical null quantile per statistic) and verdict rule (beats if gap > 2 paired SE,
loses if gap < -2 paired SE, else tie) are unchanged. Wall clock 25 s. Tables are the script's output.

## Seed and exact-size 5% critical values (rule 2): seed 94303, 20000 N(0,1) draws per n

| n | W 5% crit | W null rate | A2 5% crit | A2 null rate | S2 5% crit | S2 null rate |
|---|---|---|---|---|---|---|
| 25 | 0.9199 | 0.0500 | 0.7301 | 0.0500 | 13.3940 | 0.0500 |
| 50 | 0.9539 | 0.0500 | 0.7414 | 0.0500 | 26.5028 | 0.0500 |
| 100 | 0.9745 | 0.0500 | 0.7605 | 0.0500 | 52.7118 | 0.0500 |

All three null rates are exactly 0.0500 (MC SE 0.0015); critical values agree with seed 94201 to
within 0.0005 (W), 0.010 (A2) and 0.005 (S2).

## Power at exact 5% size (rule 1), 20000 paired draws per cell

| n | law | SW | AD | S2 | SW-AD (SE) | vs AD | SW-S2 (SE) | vs S2 |
|---|---|---|---|---|---|---|---|---|
| 25 | chi2_2 | 0.9253 | 0.8747 | 0.8354 | +0.0506 (0.0016) | beats | +0.0899 (0.0020) | beats |
| 25 | chi2_10 | 0.3091 | 0.2555 | 0.2715 | +0.0536 (0.0020) | beats | +0.0376 (0.0018) | beats |
| 25 | lognormal_0_0.5 | 0.6363 | 0.5697 | 0.5800 | +0.0666 (0.0020) | beats | +0.0563 (0.0019) | beats |
| 25 | beta_2_5 | 0.2225 | 0.1814 | 0.1451 | +0.0411 (0.0018) | beats | +0.0774 (0.0021) | beats |
| 50 | chi2_2 | 0.9990 | 0.9962 | 0.9828 | +0.0028 (0.0004) | beats | +0.0162 (0.0009) | beats |
| 50 | chi2_10 | 0.5855 | 0.4790 | 0.4479 | +0.1064 (0.0025) | beats | +0.1376 (0.0026) | beats |
| 50 | lognormal_0_0.5 | 0.9224 | 0.8703 | 0.8387 | +0.0520 (0.0017) | beats | +0.0836 (0.0020) | beats |
| 50 | beta_2_5 | 0.5023 | 0.3976 | 0.2190 | +0.1048 (0.0025) | beats | +0.2833 (0.0032) | beats |
| 100 | chi2_2 | 1.0000 | 1.0000 | 0.9999 | +0.0000 (0.0000) | tie | +0.0001 (0.0001) | tie |
| 100 | chi2_10 | 0.8993 | 0.7982 | 0.6629 | +0.1011 (0.0022) | beats | +0.2364 (0.0030) | beats |
| 100 | lognormal_0_0.5 | 0.9989 | 0.9940 | 0.9776 | +0.0048 (0.0005) | beats | +0.0213 (0.0010) | beats |
| 100 | beta_2_5 | 0.8957 | 0.7469 | 0.3203 | +0.1488 (0.0025) | beats | +0.5754 (0.0035) | beats |

## Replication against seed 94201

Every one of the 24 verdicts matches stuff 1. Largest power shift between seeds is 0.0118 (S2,
chi2(10), n=100), about 2.5 SE of an independent-seed difference (sqrt(2) x 0.0033); the smallest SW gap that is a "beats" in either seed is
SW minus AD at chi2(2), n=50 (+0.0028 here, +0.0030 there, about 7 paired SE both times). The paired
SE of zero at chi2(2), n=100 for SW minus AD is because all 20000 draws reject under both tests.

## Answer to the direction (seed 94303)

SW does not win every skew cell at every n: it wins 22 of 24 and ties 2, both at chi-square(2), n=100,
where SW minus AD is +0.0000 (0 paired SE; the difference is identically zero, all draws reject) and
SW minus S2 is +0.0001 (+1.4 paired SE) at the power ceiling; SW loses nowhere, same as seed 94201.
