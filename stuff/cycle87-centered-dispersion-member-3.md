# Cycle 87: centered dispersion of the capped gate at the per-n scale, member-3

Script: `stuff/cycle87-centered-dispersion-member-3.py` (numpy, seed 870033, 20000 sims per n, 20 batches of 1000 for Monte Carlo SEs). Seed 870033 was not used in cycles 84-86 and differs from member-2 (870021).

This item is the scaling counterpart to member-2: same gate family, same c grid, same laws, but t_i = x_i^2 / n instead of x_i^2, so that c*t_i is O(1) for c in 20-40 and the cap is partial rather than near-total. Member-2 flagged the per-term scale of t as the unstated parameter deciding the sign of the power gain; this item tests the other natural choice.

Definitions:
- t_i = x_i^2 / n on standardized draws; capped gate G_c = sum_i log(1 + c t_i)/c; c=0 is the uncapped sum of t_i.
- Centered dispersion ratio = var(G_c) / var(G_0) on the same draws, per (n, law); SE from batch-to-batch spread of the ratio.
- Top-term share = mean over sims of max_i term / G_c.
- Normal-calibrated t(3) power = P(G_c > 95th percentile of G_c under normal at the same n), evaluated under t(3). Gain = power(c) - power(0), SE from the batch spread of the paired difference.

Findings against rule 2, per n: c=20 maximizes t(3) power at n=25, 50 and 100, and power falls monotonically in c at every n. The gain over the uncapped c=0 gate is negative at every n (-0.178, -0.093, -0.015 with SEs 0.003, 0.002, 0.001), so no gain exceeds two standard errors; the loss exceeds two SEs at every n. Per law, the dispersion ratio is NOT flat in c: at this scale every (c, n, law) cell is below 1 by far more than two SEs (ratios 0.06-0.17 at the smallest-n, smallest-c corner and falling with c), and the drop is largest under t(3) and the contaminated mixture. The cycle 86 power gain at c=20 does not reproduce at either the x^2 scale (member-2) or the x^2/n scale (this item), so the gain depends on a scale neither item recovered.

Closing sentence: a dispersion half does not belong in the next rule, because the cap moves dispersion strongly and monotonically at every c (the ratio is never flat, so there is nothing to test), while it costs normal-calibrated t(3) power at every c and n with losses beyond two standard errors; the next rule should instead fix the per-term scale of t explicitly and re-test power alone.

## Rule 1 table: centered dispersion ratio and top-term share (20000 sims per n, seed 870033)

| c | n | law | disp ratio | SE | top-term share | SE |
|---|---|---|---|---|---|---|
| 0 | 25 | normal | 1.000 | 0.000 | 0.2110 | 0.0005 |
| 20 | 25 | normal | 0.167 | 0.001 | 0.1418 | 0.0002 |
| 25 | 25 | normal | 0.134 | 0.001 | 0.1361 | 0.0002 |
| 30 | 25 | normal | 0.111 | 0.001 | 0.1316 | 0.0002 |
| 35 | 25 | normal | 0.094 | 0.001 | 0.1278 | 0.0002 |
| 40 | 25 | normal | 0.081 | 0.001 | 0.1247 | 0.0002 |
| 0 | 25 | t3 | 1.000 | 0.000 | 0.3566 | 0.0010 |
| 20 | 25 | t3 | 0.003 | 0.000 | 0.1709 | 0.0003 |
| 25 | 25 | t3 | 0.002 | 0.000 | 0.1624 | 0.0002 |
| 30 | 25 | t3 | 0.002 | 0.000 | 0.1559 | 0.0002 |
| 35 | 25 | t3 | 0.001 | 0.000 | 0.1507 | 0.0002 |
| 40 | 25 | t3 | 0.001 | 0.000 | 0.1463 | 0.0002 |
| 0 | 25 | t5 | 1.000 | 0.000 | 0.2874 | 0.0007 |
| 20 | 25 | t5 | 0.033 | 0.001 | 0.1589 | 0.0002 |
| 25 | 25 | t5 | 0.025 | 0.001 | 0.1515 | 0.0002 |
| 30 | 25 | t5 | 0.020 | 0.001 | 0.1457 | 0.0002 |
| 35 | 25 | t5 | 0.017 | 0.001 | 0.1411 | 0.0002 |
| 40 | 25 | t5 | 0.014 | 0.001 | 0.1372 | 0.0002 |
| 0 | 25 | mix | 1.000 | 0.000 | 0.3280 | 0.0011 |
| 20 | 25 | mix | 0.027 | 0.000 | 0.1690 | 0.0003 |
| 25 | 25 | mix | 0.021 | 0.000 | 0.1606 | 0.0003 |
| 30 | 25 | mix | 0.016 | 0.000 | 0.1541 | 0.0003 |
| 35 | 25 | mix | 0.013 | 0.000 | 0.1489 | 0.0003 |
| 40 | 25 | mix | 0.011 | 0.000 | 0.1445 | 0.0003 |
| 0 | 50 | normal | 1.000 | 0.000 | 0.1295 | 0.0002 |
| 20 | 50 | normal | 0.299 | 0.001 | 0.0901 | 0.0001 |
| 25 | 50 | normal | 0.252 | 0.001 | 0.0863 | 0.0001 |
| 30 | 50 | normal | 0.216 | 0.001 | 0.0831 | 0.0001 |
| 35 | 50 | normal | 0.188 | 0.001 | 0.0805 | 0.0001 |
| 40 | 50 | normal | 0.166 | 0.001 | 0.0783 | 0.0001 |
| 0 | 50 | t3 | 1.000 | 0.000 | 0.2827 | 0.0009 |
| 20 | 50 | t3 | 0.006 | 0.001 | 0.1207 | 0.0002 |
| 25 | 50 | t3 | 0.005 | 0.000 | 0.1135 | 0.0002 |
| 30 | 50 | t3 | 0.004 | 0.000 | 0.1080 | 0.0001 |
| 35 | 50 | t3 | 0.003 | 0.000 | 0.1035 | 0.0001 |
| 40 | 50 | t3 | 0.003 | 0.000 | 0.0998 | 0.0001 |
| 0 | 50 | t5 | 1.000 | 0.000 | 0.2069 | 0.0005 |
| 20 | 50 | t5 | 0.069 | 0.002 | 0.1090 | 0.0002 |
| 25 | 50 | t5 | 0.055 | 0.002 | 0.1030 | 0.0002 |
| 30 | 50 | t5 | 0.045 | 0.001 | 0.0983 | 0.0001 |
| 35 | 50 | t5 | 0.038 | 0.001 | 0.0945 | 0.0001 |
| 40 | 50 | t5 | 0.033 | 0.001 | 0.0914 | 0.0001 |
| 0 | 50 | mix | 1.000 | 0.000 | 0.2491 | 0.0008 |
| 20 | 50 | mix | 0.060 | 0.001 | 0.1206 | 0.0002 |
| 25 | 50 | mix | 0.047 | 0.001 | 0.1133 | 0.0002 |
| 30 | 50 | mix | 0.039 | 0.000 | 0.1078 | 0.0002 |
| 35 | 50 | mix | 0.032 | 0.000 | 0.1033 | 0.0002 |
| 40 | 50 | mix | 0.028 | 0.000 | 0.0995 | 0.0002 |
| 0 | 100 | normal | 1.000 | 0.000 | 0.0771 | 0.0001 |
| 20 | 100 | normal | 0.467 | 0.001 | 0.0572 | 0.0001 |
| 25 | 100 | normal | 0.412 | 0.001 | 0.0548 | 0.0001 |
| 30 | 100 | normal | 0.367 | 0.001 | 0.0528 | 0.0000 |
| 35 | 100 | normal | 0.331 | 0.001 | 0.0511 | 0.0000 |
| 40 | 100 | normal | 0.301 | 0.001 | 0.0497 | 0.0000 |
| 0 | 100 | t3 | 1.000 | 0.000 | 0.2275 | 0.0009 |
| 20 | 100 | t3 | 0.008 | 0.001 | 0.0888 | 0.0002 |
| 25 | 100 | t3 | 0.006 | 0.001 | 0.0826 | 0.0001 |
| 30 | 100 | t3 | 0.005 | 0.001 | 0.0779 | 0.0001 |
| 35 | 100 | t3 | 0.004 | 0.001 | 0.0741 | 0.0001 |
| 40 | 100 | t3 | 0.004 | 0.000 | 0.0710 | 0.0001 |
| 0 | 100 | t5 | 1.000 | 0.000 | 0.1443 | 0.0005 |
| 20 | 100 | t5 | 0.119 | 0.006 | 0.0762 | 0.0001 |
| 25 | 100 | t5 | 0.098 | 0.005 | 0.0715 | 0.0001 |
| 30 | 100 | t5 | 0.083 | 0.004 | 0.0679 | 0.0001 |
| 35 | 100 | t5 | 0.072 | 0.004 | 0.0649 | 0.0001 |
| 40 | 100 | t5 | 0.063 | 0.003 | 0.0624 | 0.0001 |
| 0 | 100 | mix | 1.000 | 0.000 | 0.1801 | 0.0004 |
| 20 | 100 | mix | 0.119 | 0.001 | 0.0877 | 0.0001 |
| 25 | 100 | mix | 0.096 | 0.001 | 0.0818 | 0.0001 |
| 30 | 100 | mix | 0.081 | 0.001 | 0.0773 | 0.0001 |
| 35 | 100 | mix | 0.069 | 0.001 | 0.0736 | 0.0001 |
| 40 | 100 | mix | 0.060 | 0.001 | 0.0705 | 0.0001 |

## Rule 2 summary

| n | best c | power(best) | power(c=0) | gain | SE(gain) | gain > 2 SE |
|---|---|---|---|---|---|---|
| 25 | 20 | 0.5760 | 0.7540 | -0.1780 | 0.0033 | no |
| 50 | 20 | 0.8251 | 0.9184 | -0.0934 | 0.0019 | no |
| 100 | 20 | 0.9777 | 0.9929 | -0.0152 | 0.0010 | no |

All c, t(3) power by n: {25: {0: 0.754, 20: 0.576, 25: 0.5582, 30: 0.5427, 35: 0.5304, 40: 0.5201}, 50: {0: 0.9184, 20: 0.825, 25: 0.81, 30: 0.7956, 35: 0.7832, 40: 0.7717}, 100: {0: 0.9928, 20: 0.9777, 25: 0.9742, 30: 0.9706, 35: 0.9677, 40: 0.9648}}

Dispersion ratio flat in c (every c within 2 SE of 1)?
- normal: NOT flat (0/15 cells within 2 SE)
- t3: NOT flat (0/15 cells within 2 SE)
- t5: NOT flat (0/15 cells within 2 SE)
- mix: NOT flat (0/15 cells within 2 SE)
