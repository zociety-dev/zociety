# Top-k winsorize sweep: k=2 at n=25 and k=3 at n=50 reach var/mean^2 <= 2/3, but every k loses far more than 0.02 power

**Answer to the cycle 84 direction (rule 2 verdict).** No k satisfies both
halves at either n. Verdict per n, smallest k with capped var/mean^2 at most
2/3 while normal-calibrated power at n=25, 50, 100 stays within 0.02 of
uncapped:

- n=25: **none**. The moment bound alone is met from k=2 (0.53, then 0.35 at
  k=3 and 0.23 at k=5), but k=1 already loses 0.195 of power at n=25 and 0.097
  at n=100, and the loss grows with k.
- n=50: **none**. The moment bound alone is met from k=3 (0.64, then 0.34 at
  k=5); k=1 loses 0.180 at n=50 and 0.097 at n=100, k=3 loses 0.41 and 0.31.

Where the residual excess lives (rule 1 share column): after the top k draws
are flattened to the (k+1)th largest |draw|, those k draws still carry 0.26 to
0.43 of the AD sum in the top 1% of t(3) sims, against 0.99 for the single
largest draw uncapped (cycle 82). The remaining 0.57 to 0.74 sits in the
uncapped draws just below the cap: the (k+1)th draw sets the cap level, so
heavy t(3) samples still push all k+1 extreme terms out together, and
var/mean^2 falls geometrically in k (n=50: 386, 10.3, 1.14, 0.64, 0.34) rather
than collapsing at any one k. The excess is not in one draw but in the whole
extreme tail, and removing it with a winsorize removes the gate's t(3) signal
at the same rate.

## Inputs (rule 1)

- Statistic: cycle 71/75 lower-tail-weighted Anderson-Darling gate,
  `sum_i (F_n(i) - Phi(z_i))^2 / Phi(z_i)` on standardized data, scaled by
  `n^-1/2`; same pure-python code as cycle 82's `tail-trim-check.py` and cycle
  83's `cap-single-draw-check.py`.
- Script `stuff/topk-winsorize-sweep.py`, output `stuff/topk-winsorize-sweep.csv`,
  runs in about 4 s.
- Seed 84002 (per-stream 8400200 + n + {0 t(3), 1 normal}); 4000 sims per n per
  law; n = 25, 50, 100; t(3) drawn as gauss / sqrt(gamma(1.5, 2/3)) as in cycle 71.
- Cap rule: variant k replaces the k largest |draw| by the (k+1)th largest
  |draw|, sign kept, before standardizing (winsorize quantile 1 - k/n, shown in
  the table). k = 0 is the uncapped baseline row.
- Share: sum of the post-cap AD terms of those k draws divided by the AD sum,
  averaged over the top 1% of t(3) sims by statistic value.
- Power: critical value is the normal-data p95 of the same variant at the same n
  (per-n calibration, cycles 76 onward), power is the fraction of t(3) samples
  above it. "Normal-data power" is read as in cycle 83: the t(3) power of the
  gate calibrated on normal data (uncapped 0.378, 0.583, 0.835 here against
  0.372, 0.585, 0.834 in cycle 83 and 0.36, 0.60, 0.84 in cycle 75).

### Rule 1 and rule 2 table: t(3), k = 0 is the uncapped baseline

| n | k | winsor q | mean | variance | var/mean^2 | p99 | top-1% AD share of top k | power (normal-calibrated) | power minus k=0 | n=100 power minus k=0 |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 0 | 1.000 | 0.5631 | 14.75 | 46.5 | 11.18 | 0.000 | 0.378 | +0.000 | +0.000 |
| 25 | 1 | 0.960 | 0.05496 | 0.003478 | 1.151 | 0.2987 | 0.290 | 0.183 | -0.195 | -0.097 |
| 25 | 2 | 0.920 | 0.04342 | 0.001008 | 0.5347 | 0.1654 | 0.261 | 0.095 | -0.283 | -0.201 |
| 25 | 3 | 0.880 | 0.0426 | 0.0006372 | 0.3511 | 0.1333 | 0.314 | 0.051 | -0.327 | -0.312 |
| 25 | 5 | 0.800 | 0.05468 | 0.0006737 | 0.2253 | 0.1376 | 0.288 | 0.029 | -0.348 | -0.522 |
| 50 | 0 | 1.000 | 7473 | 2.157e+10 | 386.4 | 2.257e+04 | 0.000 | 0.583 | +0.000 | +0.000 |
| 50 | 1 | 0.980 | 0.09499 | 0.09314 | 10.32 | 0.8927 | 0.428 | 0.403 | -0.180 | -0.097 |
| 50 | 2 | 0.960 | 0.04927 | 0.002777 | 1.144 | 0.2454 | 0.426 | 0.259 | -0.324 | -0.201 |
| 50 | 3 | 0.940 | 0.03996 | 0.001017 | 0.6368 | 0.1575 | 0.348 | 0.171 | -0.412 | -0.312 |
| 50 | 5 | 0.900 | 0.03518 | 0.0004166 | 0.3366 | 0.1127 | 0.262 | 0.063 | -0.520 | -0.522 |

### Power at every n (t(3), gate calibrated on normal-data p95 per n)

| k | n=25 | n=50 | n=100 | max abs diff vs k=0 |
|---|---|---|---|---|
| 0 | 0.378 | 0.583 | 0.835 | 0.000 |
| 1 | 0.183 | 0.403 | 0.738 | 0.195 |
| 2 | 0.095 | 0.259 | 0.634 | 0.324 |
| 3 | 0.051 | 0.171 | 0.523 | 0.412 |
| 5 | 0.029 | 0.063 | 0.312 | 0.522 |

### Normal data, same variants (calibration rows; power is 0.05 by construction)

| n | k | mean | variance | var/mean^2 | p95 (critical value) |
|---|---|---|---|---|---|
| 25 | 0 | 0.03618 | 0.001623 | 1.24 | 0.0777 |
| 25 | 1 | 0.03545 | 0.0004395 | 0.3498 | 0.07657 |
| 25 | 2 | 0.0385 | 0.0004627 | 0.3121 | 0.08174 |
| 25 | 3 | 0.04388 | 0.0005376 | 0.2792 | 0.09007 |
| 25 | 5 | 0.06025 | 0.0007661 | 0.211 | 0.1149 |
| 50 | 0 | 0.02715 | 0.0004451 | 0.6037 | 0.0573 |
| 50 | 1 | 0.0265 | 0.0002522 | 0.3592 | 0.05549 |
| 50 | 2 | 0.02757 | 0.0002379 | 0.313 | 0.05748 |
| 50 | 3 | 0.02957 | 0.0002534 | 0.2897 | 0.05986 |
| 50 | 5 | 0.03593 | 0.0003145 | 0.2436 | 0.06985 |
| 100 | 0 | 0.01934 | 0.0001871 | 0.5004 | 0.0403 |
| 100 | 1 | 0.01886 | 0.000113 | 0.3176 | 0.03911 |
| 100 | 2 | 0.01927 | 0.0001137 | 0.3061 | 0.03978 |
| 100 | 3 | 0.02004 | 0.0001173 | 0.2921 | 0.04118 |
| 100 | 5 | 0.02253 | 0.0001338 | 0.2635 | 0.04553 |

## Caveats

- The k=1 power loss (0.195 at n=25) matches cycle 83's winsor row (0.17 at
  n=25), so this is the same effect, not a seed artefact; 4000 sims give a
  power standard error of about 0.008.
- The winsorize cap floats with the (k+1)th draw, so on normal data it barely
  moves the critical value (0.078 to 0.082 at n=25 for k=0 to k=2) while on
  t(3) it removes most of the signal; a fixed-level cap (cycle 83's share caps)
  is the variant that kept power, and it did not reach 2/3 either.
- Next natural probe: a share cap on the top k terms jointly rather than a
  winsorize, since the share column shows the residual mass is in the k+1
  extreme draws together.
