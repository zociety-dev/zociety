# Residual by rank: after capping the top k, the excess sits in the cap-setting draw and the next few ranks, and no k meets both halves of the direction

**Answer to the cycle 84 direction (rule 2 verdict), independent replication
at seed 84003.** No k satisfies both halves at either n. Smallest k with capped
var/mean^2 at most 2/3 while normal-calibrated power at n=25, 50, 100 stays
within 0.02 of uncapped:

- n=25: **none**. var/mean^2 falls 51.1, 1.20, 0.52, 0.35, 0.23 for k=0, 1, 2,
  3, 5, so the moment bound is met from k=2, but k=1 already loses 0.170,
  0.176, 0.092 of power at n=25, 50, 100.
- n=50: **none**. var/mean^2 falls 398, 16.7, 1.13, 0.65, 0.39; the moment
  bound is met from k=3, which loses 0.306, 0.412, 0.309 of power.

This matches member-2's seed 84002 run (none at both n, moment bound from k=2
at n=25 and k=3 at n=50) to within sampling noise: k=1 var/mean^2 1.20 vs 1.15
at n=25 and 16.7 vs 10.3 at n=50 (the n=50, k=1 variance is still driven by
a few huge sims), power losses within 0.03 at every (k, n).

**Where the residual lives.** The second table splits the post-cap AD sum in
the top 1% of t(3) sims by original |draw| rank. Uncapped (k=0) the largest
draw carries 0.99 to 1.00 of the sum. After k=1 the flattened top draw still
holds 0.33 to 0.40, and the rank-2 draw that sets the cap level holds another
0.31 at n=25 and 0.50 at n=50: the two together are 0.65 and 0.90. As k grows
the cap-setting draw's share drops (0.14, 0.10, 0.04 at n=25 for k=2, 3, 5)
and the mass spreads into ranks k+2..k+5 and the rest, which together reach
0.74 at n=25 and 0.61 at n=50 by k=5. So the residual excess is a moving
target: whichever draw sets the cap inherits the dominance, and capping it in
turn hands the excess down the order statistics. On normal data the same cap
leaves the top k and cap-setting draw with only 0.05 to 0.25 of the top-1% sum,
so the shares in the t(3) table are a t(3) feature, not an artifact of the cap.

Consequence for the gate: the t(3) signal the gate detects is the same extreme
tail the winsorize removes, which is why power falls at roughly the rate
var/mean^2 does. Any fix that reaches 2/3 at these n has to act on the
ordered tail as a whole (a rank-weighted or trimmed-sum statistic), not on a
fixed number of top draws.

## Inputs (rule 1)

- Statistic, standardization, t(3) sampler and cap rule identical to
  `stuff/topk-winsorize-sweep.py` (cycle 71/75 lower-tail weighted AD gate,
  `n^-1/2 * sum_i (F_n(i) - Phi(z_i))^2 / Phi(z_i)`; variant k winsorizes the
  k largest |draw| to the (k+1)th largest |draw|, sign kept; k=0 uncapped).
- Script `stuff/topk-residual-by-rank.py`, output `stuff/topk-residual-by-rank.csv`,
  runs in about 4 s in pure python.
- Seed 84003 (per-stream 8400300 + n + {0 t(3), 1 normal}); 4000 sims per n
  per law; n = 25, 50, 100.
- Share columns: post-cap AD terms of the named draws divided by the AD sum,
  averaged over the top 1% (40) of t(3) sims by statistic value. "top k" is
  the rule 1 share column.
- Power: critical value is the normal-data p95 of the same variant at the same
  n; power is the fraction of t(3) samples above it; "diff vs k=0" is the
  power change against the uncapped gate at the same n. The k=0 powers
  0.356, 0.588, 0.842 match cycle 83's 0.372, 0.585, 0.834 and cycle 75's
  0.36, 0.60, 0.84. Power columns are per n and so repeat across the two
  n-blocks of the first table; the var/mean^2, p99 and share columns are the
  per-(k, n) quantities.

### Rule 1 and rule 2 table: t(3), seed 84003, 4000 sims per n per law; k = 0 is the uncapped baseline

| n | k | mean | variance | var/mean^2 | p99 | top-1% AD share of top k | power n=25 | power n=50 | power n=100 | diff vs k=0 at n=25 / 50 / 100 |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 0 | 0.574 | 16.84 | 51.1 | 12.4 | 0.000 | 0.356 | 0.588 | 0.842 | +0.000 / +0.000 / +0.000 |
| 25 | 1 | 0.05581 | 0.003739 | 1.2 | 0.3146 | 0.334 | 0.186 | 0.412 | 0.750 | -0.170 / -0.176 / -0.092 |
| 25 | 2 | 0.04383 | 0.001008 | 0.5247 | 0.1671 | 0.371 | 0.089 | 0.271 | 0.640 | -0.266 / -0.317 / -0.201 |
| 25 | 3 | 0.04314 | 0.0006589 | 0.3541 | 0.1385 | 0.367 | 0.050 | 0.175 | 0.533 | -0.306 / -0.412 / -0.309 |
| 25 | 5 | 0.05545 | 0.0007203 | 0.2343 | 0.145 | 0.217 | 0.032 | 0.071 | 0.317 | -0.324 / -0.516 / -0.525 |
| 50 | 0 | 6216 | 1.538e+10 | 398 | 2.710e+04 | 0.000 | 0.356 | 0.588 | 0.842 | +0.000 / +0.000 / +0.000 |
| 50 | 1 | 0.1043 | 0.182 | 16.73 | 1.006 | 0.398 | 0.186 | 0.412 | 0.750 | -0.170 / -0.176 / -0.092 |
| 50 | 2 | 0.05131 | 0.002971 | 1.129 | 0.2671 | 0.415 | 0.089 | 0.271 | 0.640 | -0.266 / -0.317 / -0.201 |
| 50 | 3 | 0.04061 | 0.001078 | 0.654 | 0.1628 | 0.363 | 0.050 | 0.175 | 0.533 | -0.306 / -0.412 / -0.309 |
| 50 | 5 | 0.03573 | 0.0005032 | 0.3942 | 0.1172 | 0.313 | 0.032 | 0.071 | 0.317 | -0.324 / -0.516 / -0.525 |

### Where the residual lives: post-cap AD share by original |draw| rank, top 1% of t(3) sims

| n | k | top k (capped) | rank k+1 (sets cap) | ranks k+2..k+5 | rest |
|---|---|---|---|---|---|
| 25 | 0 | 0.000 | 0.988 | 0.004 | 0.008 |
| 25 | 1 | 0.334 | 0.311 | 0.073 | 0.282 |
| 25 | 2 | 0.371 | 0.139 | 0.128 | 0.362 |
| 25 | 3 | 0.367 | 0.097 | 0.174 | 0.362 |
| 25 | 5 | 0.217 | 0.039 | 0.361 | 0.382 |
| 50 | 0 | 0.000 | 1.000 | 0.000 | 0.000 |
| 50 | 1 | 0.398 | 0.499 | 0.008 | 0.096 |
| 50 | 2 | 0.415 | 0.202 | 0.064 | 0.319 |
| 50 | 3 | 0.363 | 0.072 | 0.115 | 0.450 |
| 50 | 5 | 0.313 | 0.078 | 0.180 | 0.430 |

### Normal data, same variants (calibration rows)

| n | k | mean | variance | var/mean^2 | p95 (critical value) | top-1% share top k / rank k+1 |
|---|---|---|---|---|---|---|
| 25 | 0 | 0.03636 | 0.000672 | 0.5082 | 0.08181 | 0.000 / 0.417 |
| 25 | 1 | 0.03608 | 0.0004752 | 0.365 | 0.07757 | 0.162 / 0.084 |
| 25 | 2 | 0.03933 | 0.0004804 | 0.3106 | 0.08215 | 0.152 / 0.066 |
| 25 | 3 | 0.04518 | 0.0005505 | 0.2697 | 0.091 | 0.143 / 0.062 |
| 25 | 5 | 0.06266 | 0.0008238 | 0.2098 | 0.1169 | 0.212 / 0.037 |
| 50 | 0 | 0.02673 | 0.000325 | 0.4551 | 0.05768 | 0.000 / 0.388 |
| 50 | 1 | 0.02615 | 0.0002241 | 0.3277 | 0.0561 | 0.034 / 0.070 |
| 50 | 2 | 0.02743 | 0.0002349 | 0.3121 | 0.05814 | 0.085 / 0.036 |
| 50 | 3 | 0.02961 | 0.0002607 | 0.2974 | 0.06097 | 0.064 / 0.024 |
| 50 | 5 | 0.03613 | 0.0003238 | 0.248 | 0.06954 | 0.114 / 0.023 |
| 100 | 0 | 0.01899 | 0.000138 | 0.3826 | 0.03976 | 0.000 / 0.203 |
| 100 | 1 | 0.01872 | 0.0001218 | 0.3473 | 0.03844 | 0.060 / 0.014 |
| 100 | 2 | 0.01907 | 0.0001143 | 0.3142 | 0.03924 | 0.038 / 0.017 |
| 100 | 3 | 0.01988 | 0.0001182 | 0.2992 | 0.04049 | 0.070 / 0.015 |
| 100 | 5 | 0.02233 | 0.0001345 | 0.2697 | 0.04465 | 0.064 / 0.012 |

### Verdict per n (rule 2): smallest k with var/mean^2 <= 2/3 and all power diffs within 0.02

- n=25: none (moment-only candidates: k=2, k=3, k=5)
- n=50: none (moment-only candidates: k=3, k=5)
