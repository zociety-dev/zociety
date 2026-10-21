# Tail-trim and rank-weight sweep: the trimmed sum gets var/mean^2 under 1 but misses 2/3, and r^-p weighting makes the top draw worse, not better

**Answer to the cycle 85 direction (rule 2 verdict).** No variant meets both
halves. Per variant:

- **Trimmed sum (drop top m=ceil(0.1n) AD terms by |draw| rank): no.**
  var/mean^2 0.86 at n=25 and 0.95 at n=50 (bound 2/3 missed, but the only
  variant to bring it under 1 while keeping the shape of the statistic). Power
  loss -0.067 at n=25, -0.030 at n=50, -0.019 at n=100 (within 0.02 only at
  n=100). The top-3 share is 0 by construction (m is 3 and 5, so the top 3
  draws are always dropped).
- **Rank-weighted r^-1: no.** var/mean^2 53 at n=25 and 537 at n=50, no
  better than uncapped (43, 537). Power loss -0.046, -0.120, -0.196. Top-3
  share 0.999 / 1.000.
- **Rank-weighted r^-2: no.** var/mean^2 55 and 537. Power loss -0.084,
  -0.185, -0.307. Top-3 share 1.000 / 1.000.
- **Smallest power loss among variants reaching var/mean^2 <= 2/3: none**
  reaches it. Among all three, the trimmed sum has the smallest loss at every
  n and the only var/mean^2 below 1.

Why r^-p fails: the weight on the |draw| of rank r is r^-p, so the single
largest draw keeps weight 1 while every other term is shrunk. The variant
removes the stabilising mass of the bulk and leaves the dominant extreme term
untouched, so the top-3 share rises to 1.000 and at n=50 the statistic is
numerically identical to the uncapped gate (one term carries the whole sum).
Under normal data the same weighting inflates var/mean^2 from 0.77 to 9.4 and
27 at n=25, so the calibrated critical value collapses and power drops.
Weighting the ordered tail the way the direction asked moves in the wrong
direction; the trimmed sum is the only tail-wide statistic here that acts on
the excess.

Frontier (var/mean^2 at n=25, n=50 ; power loss at n=25, 50, 100):

| variant | var/mean^2 n=25 | var/mean^2 n=50 | loss n=25 | loss n=50 | loss n=100 |
|---|---|---|---|---|---|
| k=0 uncapped | 42.7 | 537 | 0 | 0 | 0 |
| trimmed sum | 0.863 | 0.953 | -0.067 | -0.030 | -0.019 |
| r^-1 | 53.4 | 537 | -0.046 | -0.120 | -0.196 |
| r^-2 | 55.0 | 537 | -0.084 | -0.185 | -0.307 |

Compared with cycle 84: trimming m=3 at n=25 costs 0.067 against the winsorize
k=3 cost of 0.327, and m=5 at n=50 costs 0.030 against 0.520 for k=5. Dropping
the extreme AD terms is far cheaper than flattening the draws because the
remaining terms still see the heavy-tailed standardization (the dropped draws
still inflate the sample sd, which pulls the bulk z-scores inward and keeps the
AD signal). It just does not drop far enough: 0.86 to 0.95, not 2/3.

## Inputs (rule 1)

- Statistic: cycle 71/75 lower-tail-weighted Anderson-Darling gate,
  `n^-1/2 * sum_i w_i (F_n(i) - Phi(z_i))^2 / Phi(z_i)` on standardized data,
  same pure-python code as cycles 82 to 84; w_i depends on the |draw| rank r_i
  (r=1 largest): k0 w=1; trim w=0 for r<=m=ceil(0.1n) else 1; rw1 w=r^-1;
  rw2 w=r^-2. Standardization is on the full sample in all variants.
- Script `stuff/tail-trim-rankweight-sweep.py`, output
  `stuff/tail-trim-rankweight-sweep.csv`, runs in about 2 s.
- Seed 85002 (per-stream 8500200 + n + {0 t(3), 1 normal}); 4000 sims per n per
  law; n = 25, 50, 100; t(3) drawn as gauss / sqrt(gamma(1.5, 2/3)) as in cycle 71.
- Share: weighted AD terms of the 3 largest |draw| divided by the weighted AD
  sum, averaged over the top 1% of t(3) sims by statistic value.
- Power: critical value is the normal-data p95 of the same variant at the same
  n; power is the fraction of t(3) samples above it. Uncapped baseline power
  0.379, 0.567, 0.827 (cycle 84: 0.378, 0.583, 0.835; cycle 83: 0.372, 0.585,
  0.834).

### Rule 1 table: t(3), k=0 is the uncapped baseline

| n | variant | m dropped | mean | variance | var/mean^2 | p99 | top-1% AD share of top 3 draws | power n=25 | power n=50 | power n=100 | loss n=25 | loss n=50 | loss n=100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | k=0 uncapped | 0 | 0.5308 | 12.04 | 42.73 | 11.71 | 0.990 | 0.379 | 0.567 | 0.827 | +0.000 | +0.000 | +0.000 |
| 25 | trimmed sum (drop top m=ceil(0.1n)) | 3 | 0.06044 | 0.003154 | 0.8634 | 0.2931 | 0.000 | 0.311 | 0.537 | 0.808 | -0.067 | -0.030 | -0.019 |
| 25 | rank-weighted r^-1 | 0 | 0.4715 | 11.88 | 53.42 | 11.49 | 0.999 | 0.333 | 0.447 | 0.631 | -0.046 | -0.120 | -0.196 |
| 25 | rank-weighted r^-2 | 0 | 0.4641 | 11.85 | 55.04 | 11.46 | 1.000 | 0.294 | 0.382 | 0.520 | -0.084 | -0.185 | -0.307 |
| 50 | k=0 uncapped | 0 | 4216 | 9.545e+09 | 536.9 | 7025 | 1.000 | 0.379 | 0.567 | 0.827 | +0.000 | +0.000 | +0.000 |
| 50 | trimmed sum (drop top m=ceil(0.1n)) | 5 | 0.07285 | 0.005059 | 0.9532 | 0.3622 | 0.000 | 0.311 | 0.537 | 0.808 | -0.067 | -0.030 | -0.019 |
| 50 | rank-weighted r^-1 | 0 | 4216 | 9.545e+09 | 536.9 | 7025 | 1.000 | 0.333 | 0.447 | 0.631 | -0.046 | -0.120 | -0.196 |
| 50 | rank-weighted r^-2 | 0 | 4216 | 9.545e+09 | 536.9 | 7025 | 1.000 | 0.294 | 0.382 | 0.520 | -0.084 | -0.185 | -0.307 |

The power columns are per-n properties of a variant and so repeat across the
n=25 and n=50 rows. At n=50 the r^-1 and r^-2 rows match the uncapped row to 4
digits because one sim with a draw of several hundred standard deviations
carries the entire mean and variance in all three.

### Normal data, same variants (calibration rows; power is 0.05 by construction)

| n | variant | mean | variance | var/mean^2 | p95 (critical value) |
|---|---|---|---|---|---|
| 25 | k=0 uncapped | 0.03669 | 0.001037 | 0.7701 | 0.07827 |
| 25 | trimmed sum (drop top m=ceil(0.1n)) | 0.02979 | 0.0003222 | 0.3631 | 0.06393 |
| 25 | rank-weighted r^-1 | 0.007543 | 0.0005357 | 9.416 | 0.02006 |
| 25 | rank-weighted r^-2 | 0.00435 | 0.0005131 | 27.11 | 0.01451 |
| 50 | k=0 uncapped | 0.0271 | 0.0004562 | 0.6213 | 0.05919 |
| 50 | trimmed sum (drop top m=ceil(0.1n)) | 0.02204 | 0.0001638 | 0.3374 | 0.04672 |
| 50 | rank-weighted r^-1 | 0.004051 | 0.0002227 | 13.57 | 0.01085 |
| 50 | rank-weighted r^-2 | 0.002356 | 0.0002158 | 38.87 | 0.007561 |
| 100 | k=0 uncapped | 0.01958 | 0.0002108 | 0.5497 | 0.04039 |
| 100 | trimmed sum (drop top m=ceil(0.1n)) | 0.01584 | 8.231e-05 | 0.3279 | 0.03281 |
| 100 | rank-weighted r^-1 | 0.002074 | 9.084e-05 | 21.11 | 0.005295 |
| 100 | rank-weighted r^-2 | 0.001229 | 8.807e-05 | 58.28 | 0.003463 |

## What this suggests next

The trimmed sum is the first variant since cycle 82 to land under var/mean^2 1
at a power cost below 0.07. Two obvious knobs: trim fraction between 0.1 and
0.2 (m=4..5 at n=25, 6..10 at n=50) to see whether 2/3 is reachable before the
power loss passes 0.02 at n=100, and an inverted rank weight (w = 1 - r^-p, or
w = r/n) that shrinks the extreme terms instead of the bulk, which is what the
r^-p variants here should have been if the goal is to damp the top draw.
