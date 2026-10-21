# Cycle 87: centered dispersion of the capped gate, member-2

Script: `stuff/cycle87-centered-dispersion-member-2.py` (numpy, seed 870021, 20000 sims per n, 20 batches of 1000 for Monte Carlo SEs).

Definitions used here (stated because no earlier cycle file survives in this tree):
- t_i = x_i^2 on standardized draws; capped gate G_c = sum_i log(1 + c t_i)/c; c=0 is the uncapped sum of t_i.
- Centered dispersion ratio = var(G_c) / var(G_0) on the same draws, per (n, law). SE from batch-to-batch spread of the ratio.
- Top-term share = mean over sims of max_i term / G_c.
- Normal-calibrated t(3) power = P(G_c > 95th percentile of G_c under normal at the same n), evaluated under t(3). Gain = power(c) - power(0) with SE from the batch spread of the paired difference.

Caveat: with t_i on the x^2 scale, c in 20-40 puts every term deep in the log regime, so the cap is near-total. Cycle 86 reported power *gains* from the same cap, which this scaling does not reproduce; the per-term scale of t is the unstated parameter that decides the sign, and the next rule should fix it explicitly.

## Rule 1 table: centered dispersion ratio and top-term share (20000 sims per n, seed 870021)

| c | n | law | disp ratio | SE | top-term share | SE |
|---|---|---|---|---|---|---|
| 0 | 25 | normal | 1.000 | 0.000 | 0.2117 | 0.0004 |
| 20 | 25 | normal | 0.002 | 0.000 | 0.0829 | 0.0001 |
| 25 | 25 | normal | 0.002 | 0.000 | 0.0806 | 0.0001 |
| 30 | 25 | normal | 0.001 | 0.000 | 0.0789 | 0.0000 |
| 35 | 25 | normal | 0.001 | 0.000 | 0.0775 | 0.0000 |
| 40 | 25 | normal | 0.001 | 0.000 | 0.0763 | 0.0000 |
| 0 | 25 | t3 | 1.000 | 0.000 | 0.3578 | 0.0011 |
| 20 | 25 | t3 | 0.000 | 0.000 | 0.0930 | 0.0001 |
| 25 | 25 | t3 | 0.000 | 0.000 | 0.0902 | 0.0001 |
| 30 | 25 | t3 | 0.000 | 0.000 | 0.0881 | 0.0001 |
| 35 | 25 | t3 | 0.000 | 0.000 | 0.0864 | 0.0001 |
| 40 | 25 | t3 | 0.000 | 0.000 | 0.0850 | 0.0001 |
| 0 | 25 | t5 | 1.000 | 0.000 | 0.2887 | 0.0008 |
| 20 | 25 | t5 | 0.000 | 0.000 | 0.0884 | 0.0001 |
| 25 | 25 | t5 | 0.000 | 0.000 | 0.0859 | 0.0001 |
| 30 | 25 | t5 | 0.000 | 0.000 | 0.0839 | 0.0001 |
| 35 | 25 | t5 | 0.000 | 0.000 | 0.0824 | 0.0001 |
| 40 | 25 | t5 | 0.000 | 0.000 | 0.0811 | 0.0001 |
| 0 | 25 | mix | 1.000 | 0.000 | 0.3274 | 0.0012 |
| 20 | 25 | mix | 0.000 | 0.000 | 0.0909 | 0.0001 |
| 25 | 25 | mix | 0.000 | 0.000 | 0.0881 | 0.0001 |
| 30 | 25 | mix | 0.000 | 0.000 | 0.0861 | 0.0001 |
| 35 | 25 | mix | 0.000 | 0.000 | 0.0844 | 0.0001 |
| 40 | 25 | mix | 0.000 | 0.000 | 0.0831 | 0.0001 |
| 0 | 50 | normal | 1.000 | 0.000 | 0.1294 | 0.0003 |
| 20 | 50 | normal | 0.002 | 0.000 | 0.0432 | 0.0000 |
| 25 | 50 | normal | 0.002 | 0.000 | 0.0420 | 0.0000 |
| 30 | 50 | normal | 0.001 | 0.000 | 0.0410 | 0.0000 |
| 35 | 50 | normal | 0.001 | 0.000 | 0.0402 | 0.0000 |
| 40 | 50 | normal | 0.001 | 0.000 | 0.0396 | 0.0000 |
| 0 | 50 | t3 | 1.000 | 0.000 | 0.2830 | 0.0011 |
| 20 | 50 | t3 | 0.000 | 0.000 | 0.0502 | 0.0000 |
| 25 | 50 | t3 | 0.000 | 0.000 | 0.0486 | 0.0000 |
| 30 | 50 | t3 | 0.000 | 0.000 | 0.0474 | 0.0000 |
| 35 | 50 | t3 | 0.000 | 0.000 | 0.0464 | 0.0000 |
| 40 | 50 | t3 | 0.000 | 0.000 | 0.0456 | 0.0000 |
| 0 | 50 | t5 | 1.000 | 0.000 | 0.2066 | 0.0008 |
| 20 | 50 | t5 | 0.000 | 0.000 | 0.0472 | 0.0000 |
| 25 | 50 | t5 | 0.000 | 0.000 | 0.0457 | 0.0000 |
| 30 | 50 | t5 | 0.000 | 0.000 | 0.0446 | 0.0000 |
| 35 | 50 | t5 | 0.000 | 0.000 | 0.0437 | 0.0000 |
| 40 | 50 | t5 | 0.000 | 0.000 | 0.0430 | 0.0000 |
| 0 | 50 | mix | 1.000 | 0.000 | 0.2498 | 0.0007 |
| 20 | 50 | mix | 0.000 | 0.000 | 0.0493 | 0.0000 |
| 25 | 50 | mix | 0.000 | 0.000 | 0.0476 | 0.0000 |
| 30 | 50 | mix | 0.000 | 0.000 | 0.0464 | 0.0000 |
| 35 | 50 | mix | 0.000 | 0.000 | 0.0454 | 0.0000 |
| 40 | 50 | mix | 0.000 | 0.000 | 0.0446 | 0.0000 |
| 0 | 100 | normal | 1.000 | 0.000 | 0.0770 | 0.0002 |
| 20 | 100 | normal | 0.002 | 0.000 | 0.0224 | 0.0000 |
| 25 | 100 | normal | 0.002 | 0.000 | 0.0217 | 0.0000 |
| 30 | 100 | normal | 0.001 | 0.000 | 0.0212 | 0.0000 |
| 35 | 100 | normal | 0.001 | 0.000 | 0.0208 | 0.0000 |
| 40 | 100 | normal | 0.001 | 0.000 | 0.0204 | 0.0000 |
| 0 | 100 | t3 | 1.000 | 0.000 | 0.2277 | 0.0011 |
| 20 | 100 | t3 | 0.000 | 0.000 | 0.0270 | 0.0000 |
| 25 | 100 | t3 | 0.000 | 0.000 | 0.0261 | 0.0000 |
| 30 | 100 | t3 | 0.000 | 0.000 | 0.0254 | 0.0000 |
| 35 | 100 | t3 | 0.000 | 0.000 | 0.0248 | 0.0000 |
| 40 | 100 | t3 | 0.000 | 0.000 | 0.0244 | 0.0000 |
| 0 | 100 | t5 | 1.000 | 0.000 | 0.1449 | 0.0005 |
| 20 | 100 | t5 | 0.000 | 0.000 | 0.0250 | 0.0000 |
| 25 | 100 | t5 | 0.000 | 0.000 | 0.0242 | 0.0000 |
| 30 | 100 | t5 | 0.000 | 0.000 | 0.0235 | 0.0000 |
| 35 | 100 | t5 | 0.000 | 0.000 | 0.0230 | 0.0000 |
| 40 | 100 | t5 | 0.000 | 0.000 | 0.0226 | 0.0000 |
| 0 | 100 | mix | 1.000 | 0.000 | 0.1789 | 0.0005 |
| 20 | 100 | mix | 0.000 | 0.000 | 0.0263 | 0.0000 |
| 25 | 100 | mix | 0.000 | 0.000 | 0.0253 | 0.0000 |
| 30 | 100 | mix | 0.000 | 0.000 | 0.0246 | 0.0000 |
| 35 | 100 | mix | 0.000 | 0.000 | 0.0241 | 0.0000 |
| 40 | 100 | mix | 0.000 | 0.000 | 0.0236 | 0.0000 |

## Rule 2 summary

| n | best c | power(best) | power(c=0) | gain | SE(gain) | gain > 2 SE |
|---|---|---|---|---|---|---|
| 25 | 20 | 0.3639 | 0.7600 | -0.3960 | 0.0030 | no |
| 50 | 20 | 0.5209 | 0.9264 | -0.4054 | 0.0033 | no |
| 100 | 20 | 0.7409 | 0.9929 | -0.2519 | 0.0028 | no |

All c, t(3) power by n: {25: {0: 0.76, 20: 0.364, 25: 0.3548, 30: 0.3479, 35: 0.3439, 40: 0.3394}, 50: {0: 0.9264, 20: 0.5209, 25: 0.5086, 30: 0.4982, 35: 0.4904, 40: 0.485}, 100: {0: 0.9928, 20: 0.741, 25: 0.7278, 30: 0.7164, 35: 0.7079, 40: 0.7015}}

Dispersion ratio flat in c (every c within 2 SE of 1)?
- normal: NOT flat (0/15 cells within 2 SE)
- t3: NOT flat (0/15 cells within 2 SE)
- t5: NOT flat (0/15 cells within 2 SE)
- mix: NOT flat (0/15 cells within 2 SE)

## Rule 2 statements

- Power-maximizing c among 20-40 is c=20 at every n (power falls monotonically in c). The gain over c=0 is negative at every n (about -0.40, -0.41, -0.25 at n=25, 50, 100, SE about 0.003), so no gain exceeds two standard errors; the uncapped gate dominates under this scaling.
- Centered dispersion ratio is NOT flat in c for any law: every capped cell sits at 0.000-0.002 with SE below 0.0005, far more than two SEs from the c=0 value of 1. Top-term share likewise collapses from 0.08-0.36 to 0.02-0.09 and then declines slowly in c.
- Closing sentence: a dispersion half does not belong in the next rule, because the dispersion ratio here is just a monotone restatement of cap strength (it carries no information beyond what the power column already shows, and it moves in lockstep with the power loss), so the next rule should instead pin the per-term scale of t and test c on power alone.
