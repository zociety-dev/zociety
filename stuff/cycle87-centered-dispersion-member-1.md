# Cycle 87: centered dispersion of the capped gate at the absolute-draw scale, member-1

Script: `stuff/cycle87-centered-dispersion-member-1.py` (numpy, seed 870047, 20000 sims per n, 20 batches of 1000 for Monte Carlo SEs). Seed 870047 was not used in cycles 84-86 and differs from member-2 (870021) and member-3 (870033).

This item is the third scaling of the same experiment: same gate family, same c grid, same laws, but t_i = |x_i| (absolute standardized draw) instead of x_i^2 (member-2) or x_i^2/n (member-3). At this scale c*t_i is O(c) for a typical draw, so the cap is near-total for every c in 20-40 and log(1+ct)/c is close to log(ct)/c: the gate becomes an almost-log-of-absolute-value statistic, which is the scaling under which a heavy-tail cap is most plausibly a power device.

Definitions:
- t_i = |x_i| on standardized draws; capped gate G_c = sum_i log(1 + c t_i)/c; c=0 is the uncapped sum of t_i.
- Centered dispersion ratio = var(G_c) / var(G_0) on the same draws, per (n, law); SE from batch-to-batch spread of the ratio.
- Top-term share = mean over sims of max_i term / G_c.
- Normal-calibrated t(3) power = P(G_c > 95th percentile of G_c under normal at the same n), evaluated under t(3). Gain = power(c) - power(0), SE from the batch spread of the paired difference.

Findings against rule 2, per n: c=20 maximizes t(3) power at n=25, 50 and 100, and power falls monotonically in c at every n. The gain over the uncapped c=0 gate is negative at every n (-0.323, -0.401, -0.327 with SEs 0.003, 0.004, 0.003), so no gain exceeds two standard errors; the loss exceeds two SEs at every n by a wide margin, and is larger than at either of the other two scalings. Per law, the dispersion ratio is NOT flat in c: every (c, n, law) cell is at or below 0.005 with SE at or below 0.001, so every cell is more than two SEs below 1 under normal, t(3), t(5) and the contaminated mixture (0 of 15 cells within two SEs for each law). Top-term share roughly halves from c=0 to c=20 and then drifts down slowly in c.

Across the three scalings tried this cycle (x^2, x^2/n, |x|) the cycle 86 power gain at c=20 reproduces at none of them, so the scale cycle 86 used remains unrecovered; at every scale tried the cap costs normal-calibrated t(3) power and compresses dispersion by one to three orders of magnitude.

Closing sentence: a dispersion half does not belong in the next rule, because at every scale tried the cap collapses the centered dispersion ratio far below 1 at every c (nothing flat to test) while costing normal-calibrated t(3) power at every c and n by more than two standard errors; the next rule should fix the per-term scale of t explicitly and test power alone.

## Rule 1 table: centered dispersion ratio and top-term share (20000 sims per n, seed 870047)

| c | n | law | disp ratio | SE | top-term share | SE |
|---|---|---|---|---|---|---|
| 0 | 25 | normal | 1.000 | 0.000 | 0.1138 | 0.0002 |
| 20 | 25 | normal | 0.005 | 0.000 | 0.0606 | 0.0000 |
| 25 | 25 | normal | 0.004 | 0.000 | 0.0594 | 0.0000 |
| 30 | 25 | normal | 0.003 | 0.000 | 0.0585 | 0.0000 |
| 35 | 25 | normal | 0.002 | 0.000 | 0.0578 | 0.0000 |
| 40 | 25 | normal | 0.002 | 0.000 | 0.0572 | 0.0000 |
| 0 | 25 | t3 | 1.000 | 0.000 | 0.1702 | 0.0003 |
| 20 | 25 | t3 | 0.001 | 0.000 | 0.0665 | 0.0000 |
| 25 | 25 | t3 | 0.001 | 0.000 | 0.0650 | 0.0000 |
| 30 | 25 | t3 | 0.001 | 0.000 | 0.0638 | 0.0000 |
| 35 | 25 | t3 | 0.001 | 0.000 | 0.0629 | 0.0000 |
| 40 | 25 | t3 | 0.000 | 0.000 | 0.0622 | 0.0000 |
| 0 | 25 | t5 | 1.000 | 0.000 | 0.1416 | 0.0003 |
| 20 | 25 | t5 | 0.003 | 0.000 | 0.0638 | 0.0000 |
| 25 | 25 | t5 | 0.002 | 0.000 | 0.0624 | 0.0000 |
| 30 | 25 | t5 | 0.001 | 0.000 | 0.0614 | 0.0000 |
| 35 | 25 | t5 | 0.001 | 0.000 | 0.0606 | 0.0000 |
| 40 | 25 | t5 | 0.001 | 0.000 | 0.0599 | 0.0000 |
| 0 | 25 | mix | 1.000 | 0.000 | 0.1539 | 0.0005 |
| 20 | 25 | mix | 0.002 | 0.000 | 0.0649 | 0.0001 |
| 25 | 25 | mix | 0.002 | 0.000 | 0.0634 | 0.0001 |
| 30 | 25 | mix | 0.001 | 0.000 | 0.0623 | 0.0000 |
| 35 | 25 | mix | 0.001 | 0.000 | 0.0614 | 0.0000 |
| 40 | 25 | mix | 0.001 | 0.000 | 0.0607 | 0.0000 |
| 0 | 50 | normal | 1.000 | 0.000 | 0.0632 | 0.0001 |
| 20 | 50 | normal | 0.005 | 0.000 | 0.0311 | 0.0000 |
| 25 | 50 | normal | 0.004 | 0.000 | 0.0305 | 0.0000 |
| 30 | 50 | normal | 0.003 | 0.000 | 0.0300 | 0.0000 |
| 35 | 50 | normal | 0.002 | 0.000 | 0.0296 | 0.0000 |
| 40 | 50 | normal | 0.002 | 0.000 | 0.0293 | 0.0000 |
| 0 | 50 | t3 | 1.000 | 0.000 | 0.1100 | 0.0003 |
| 20 | 50 | t3 | 0.001 | 0.000 | 0.0351 | 0.0000 |
| 25 | 50 | t3 | 0.001 | 0.000 | 0.0342 | 0.0000 |
| 30 | 50 | t3 | 0.001 | 0.000 | 0.0335 | 0.0000 |
| 35 | 50 | t3 | 0.001 | 0.000 | 0.0330 | 0.0000 |
| 40 | 50 | t3 | 0.000 | 0.000 | 0.0326 | 0.0000 |
| 0 | 50 | t5 | 1.000 | 0.000 | 0.0853 | 0.0002 |
| 20 | 50 | t5 | 0.003 | 0.000 | 0.0333 | 0.0000 |
| 25 | 50 | t5 | 0.002 | 0.000 | 0.0325 | 0.0000 |
| 30 | 50 | t5 | 0.001 | 0.000 | 0.0319 | 0.0000 |
| 35 | 50 | t5 | 0.001 | 0.000 | 0.0315 | 0.0000 |
| 40 | 50 | t5 | 0.001 | 0.000 | 0.0311 | 0.0000 |
| 0 | 50 | mix | 1.000 | 0.000 | 0.0963 | 0.0002 |
| 20 | 50 | mix | 0.002 | 0.000 | 0.0342 | 0.0000 |
| 25 | 50 | mix | 0.002 | 0.000 | 0.0334 | 0.0000 |
| 30 | 50 | mix | 0.001 | 0.000 | 0.0327 | 0.0000 |
| 35 | 50 | mix | 0.001 | 0.000 | 0.0322 | 0.0000 |
| 40 | 50 | mix | 0.001 | 0.000 | 0.0318 | 0.0000 |
| 0 | 100 | normal | 1.000 | 0.000 | 0.0346 | 0.0000 |
| 20 | 100 | normal | 0.005 | 0.000 | 0.0159 | 0.0000 |
| 25 | 100 | normal | 0.004 | 0.000 | 0.0156 | 0.0000 |
| 30 | 100 | normal | 0.003 | 0.000 | 0.0153 | 0.0000 |
| 35 | 100 | normal | 0.002 | 0.000 | 0.0151 | 0.0000 |
| 40 | 100 | normal | 0.002 | 0.000 | 0.0149 | 0.0000 |
| 0 | 100 | t3 | 1.000 | 0.000 | 0.0704 | 0.0002 |
| 20 | 100 | t3 | 0.001 | 0.000 | 0.0184 | 0.0000 |
| 25 | 100 | t3 | 0.001 | 0.000 | 0.0179 | 0.0000 |
| 30 | 100 | t3 | 0.001 | 0.000 | 0.0175 | 0.0000 |
| 35 | 100 | t3 | 0.001 | 0.000 | 0.0172 | 0.0000 |
| 40 | 100 | t3 | 0.000 | 0.000 | 0.0170 | 0.0000 |
| 0 | 100 | t5 | 1.000 | 0.000 | 0.0506 | 0.0001 |
| 20 | 100 | t5 | 0.003 | 0.000 | 0.0173 | 0.0000 |
| 25 | 100 | t5 | 0.002 | 0.000 | 0.0169 | 0.0000 |
| 30 | 100 | t5 | 0.001 | 0.000 | 0.0165 | 0.0000 |
| 35 | 100 | t5 | 0.001 | 0.000 | 0.0163 | 0.0000 |
| 40 | 100 | t5 | 0.001 | 0.000 | 0.0161 | 0.0000 |
| 0 | 100 | mix | 1.000 | 0.000 | 0.0580 | 0.0001 |
| 20 | 100 | mix | 0.002 | 0.000 | 0.0179 | 0.0000 |
| 25 | 100 | mix | 0.002 | 0.000 | 0.0174 | 0.0000 |
| 30 | 100 | mix | 0.001 | 0.000 | 0.0170 | 0.0000 |
| 35 | 100 | mix | 0.001 | 0.000 | 0.0168 | 0.0000 |
| 40 | 100 | mix | 0.001 | 0.000 | 0.0165 | 0.0000 |

## Rule 2 summary

| n | best c | power(best) | power(c=0) | gain | SE(gain) | gain > 2 SE |
|---|---|---|---|---|---|---|
| 25 | 20 | 0.2854 | 0.6083 | -0.3228 | 0.0031 | no |
| 50 | 20 | 0.4193 | 0.8205 | -0.4013 | 0.0035 | no |
| 100 | 20 | 0.6345 | 0.9614 | -0.3268 | 0.0032 | no |

All c, t(3) power by n: {25: {0: 0.6083, 20: 0.2854, 25: 0.2787, 30: 0.2742, 35: 0.2711, 40: 0.2686}, 50: {0: 0.8205, 20: 0.4192, 25: 0.4104, 30: 0.4045, 35: 0.399, 40: 0.3966}, 100: {0: 0.9614, 20: 0.6345, 25: 0.623, 30: 0.6144, 35: 0.6078, 40: 0.6008}}

Dispersion ratio flat in c (every c within 2 SE of 1)?
- normal: NOT flat (0/15 cells within 2 SE)
- t3: NOT flat (0/15 cells within 2 SE)
- t5: NOT flat (0/15 cells within 2 SE)
- mix: NOT flat (0/15 cells within 2 SE)
