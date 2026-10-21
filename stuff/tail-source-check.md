# The heavy tail is the t(3) data, and it lives in the AD denominator, not the variance

**Answer to the cycle 82 direction.** Yes, the heavy upper tail of the cycle
75 gate statistic is driven by the t(3) data, and replacing t(3) with N(0,1)
at the same n restores ncx2-compatible moments: var/mean^2 drops from 39 and
739 (t(3)) to 0.53 and 0.71 (normal) at n=25 and 50, both at or below the
ncx2 family ceiling of 2/3 within sampling error. The dominating term is the
denominator F = Phi(z_min) of the single most negative standardized draw,
not the pooled variance: in the top 1% of t(3) statistics that one AD term
carries 98.7% (n=25) and 100% (n=50) of the statistic, while the same draw
carries only 84% and 79% of the sum of squares.

## Inputs (rule 1)

- Statistic: the cycle 71/75 lower-tail-weighted Anderson-Darling gate,
  `sum_i (F_n(i) - Phi(z_i))^2 / Phi(z_i)` on standardized data, scaled by
  `n^-1/2`, regenerated from the identical pure-python code.
- Script `stuff/tail-source-check.py`, output `stuff/tail-source-check.csv`.
- Seed 65082 (per-stream: 6508200 + n + {0 t(3), 1 normal}); 4000 sims per n
  per law; t(3) drawn as gauss / sqrt(gamma(1.5, 2/3)) as in cycle 71.

## t(3) data (rule 1)

| n | seed | sims | mean | variance | var/mean^2 | p90 | p95 | p99 |
|---|------|------|------|----------|------------|-----|-----|-----|
| 25 | 65082 | 4000 | 0.4887 | 9.32 | 39.0 | 0.306 | 0.981 | 11.6 |
| 50 | 65082 | 4000 | 3496 | 9.03e9 | 739 | 1.47 | 29.8 | 4410 |

## Normal data (rule 1)

| n | seed | sims | mean | variance | var/mean^2 | p90 | p95 | p99 |
|---|------|------|------|----------|------------|-----|-----|-----|
| 25 | 65082 | 4000 | 0.03645 | 7.09e-4 | 0.534 | 0.0636 | 0.0780 | 0.131 |
| 50 | 65082 | 4000 | 0.02751 | 5.37e-4 | 0.710 | 0.0472 | 0.0588 | 0.0913 |

## Per-draw dominance (rule 2)

Share owed to the single largest |draw| in each sample, averaged over the
top 1% of statistics (40 samples) and over all 4000.

| law | n | top1% share of variance term | top1% share of AD sum (largest term) | all-sample share of variance | all-sample share of AD sum |
|-----|---|------|------|------|------|
| t(3) | 25 | 0.840 | 0.987 | 0.343 | 0.321 |
| t(3) | 50 | 0.788 | 1.000 | 0.280 | 0.316 |
| normal | 25 | 0.378 | 0.611 | 0.210 | 0.251 |
| normal | 50 | 0.218 | 0.481 | 0.131 | 0.169 |

## Reading

- Under normal data var/mean^2 is 0.53 and 0.71 against the ncx2 ceiling
  2/3; the 0.71 at n=50 is within the Monte Carlo spread of 4000 sims. The
  statistic is well behaved there. The 49 and 515 of cycle 81 (39 and 739
  here, same order, different seed) are entirely a t(3) effect.
- The mechanism is the weight 1/Phi(z_min). One extreme negative t(3) draw
  standardizes to z of order -4 to -6 once it inflates the sd less than it
  inflates itself, Phi(z) is 1e-5 or smaller, and that single term is the
  whole statistic (share 0.987 and 1.000 in the top 1%). The variance term
  is also dominated (0.84, 0.79) but less completely, so the heavy tail is
  a denominator effect, consistent with the member-3 join question.
- Normal top-1% shares (0.61, 0.48) show the same term is the largest even
  for Gaussian samples, but it never runs away because z_min is bounded by
  roughly -3 at these n.
- So cycle 80's lambda/n excess was the 1/Phi(z_min) tail of t(3) reaching
  the 7.815 crossing, not noncentrality; no ncx2 fit should be expected to
  hold for t(3) data beyond the fitted quantile.

## Caveats

- Single seed per law; the t(3) n=50 variance (9e9) is driven by a handful
  of draws and would move by orders of magnitude under another seed, as
  cycle 81's bootstrap bounds already showed. The share figures are far
  more stable than the moments.
- Pure-python t(3) uses gammavariate, same as cycle 71; no comparison to a
  stored cycle 75 row was made here, only regeneration from the same code.
