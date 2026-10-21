# Is the cycle 75 alternative statistic ncx2(3, lambda)? No: same power, wrong shape

**Answer to the cycle 81 direction.** The cycle 75 alternative statistic is
not ncx2(3, lambda) at n=25 or n=50. Rescaled so that its own null p95 sits
at chi2_95(3) = 7.815, it reproduces the fitted ncx2 power at 7.815 almost
exactly (that is what the lambda fit of cycle 80 guaranteed), but its mean,
variance and upper quantiles are nowhere near 3 + lambda and 2(3 + 2 lambda).
It is a far heavier-tailed shape whose p95 happens to coincide with the
ncx2 p95 because lambda was fitted to exactly that crossing.

## Inputs (rule 1)

- Alternative draws: `stuff/c75-df3-draws.csv`, copied verbatim from the cycle
  75 archive tag `rev65-attempt39-iterations11ofx` (t(3) gate statistic,
  seeds 65068 and 65069 pooled, 4000 draws per n).
- Null draws: `stuff/c75-null-draws.csv`, same tag, same seeds, 4000 per n.
- Fitted lambda per n from cycle 80: 4.018 (n=25), 7.154 (n=50).
- ncx2 reference quantiles: 20000 pure-python draws per n, seed 65081.
- Script: `stuff/ncx2-shape-check.py`; output `stuff/ncx2-shape-check.csv`.
- Rescale factor = 7.815 / per-n null p95: 95.96 (n=25), 133.84 (n=50).

## Mean and variance (rule 1)

| n | source | sims | seed | mean | variance |
|---|--------|------|------|------|----------|
| 25 | cycle 75 statistic, rescaled | 4000 | 65068+65069 | 45.67 | 102469 |
| 25 | ncx2(3, 4.018) analytic | | | 7.018 | 22.07 |
| 25 | ncx2(3, 4.018) simulated | 20000 | 65081 | 6.988 | 22.00 |
| 50 | cycle 75 statistic, rescaled | 4000 | 65068+65069 | 721440 | 2.7e14 |
| 50 | ncx2(3, 7.154) analytic | | | 10.154 | 34.62 |
| 50 | ncx2(3, 7.154) simulated | 20000 | 65081 | 10.180 | 34.54 |

## Upper tail quantiles (rule 2)

| n | source | p90 | p95 | p99 | P(stat > 7.815) |
|---|--------|-----|-----|-----|-----------------|
| 25 | cycle 75 statistic, rescaled | 28.27 | 80.71 | 885.0 | 0.3610 |
| 25 | ncx2(3, 4.018) simulated | 13.32 | 15.99 | 21.80 | 0.3615 |
| 50 | cycle 75 statistic, rescaled | 212.5 | 2828 | 1.5e6 | 0.5975 |
| 50 | ncx2(3, 7.154) simulated | 18.17 | 21.17 | 27.66 | 0.5994 |

## Reading

- Power agrees to within 0.002 at both n, confirming the rescaling is the
  one the cycle 78-80 model implicitly used.
- Every other moment and quantile disagrees by one to many orders of
  magnitude. At n=25 the empirical p99 is 40 times the ncx2 p99; at n=50 the
  variance is dominated by a handful of extreme t(3) samples (the gate
  statistic under t(3) has no finite variance in the sense that matters at
  4000 draws).
- So the "excess noncentrality" of cycles 79-80 (lambda/n 0.161, 0.143
  against 0.120) is not noncentrality at all. The lambda fit absorbs a
  heavy-tail crossing at the 7.815 threshold into a location shift, and that
  shift looks larger at small n because the t(3) tail is relatively heavier
  there. ncx2(3, lambda) should not be used as the finite-n law of this
  statistic for anything beyond the single quantile it was fitted to.

## Caveats

- The rescaling is linear. If the intended map from gate statistic to
  chi-square scale is nonlinear (e.g. a log), mean and variance would change
  but the ordering of quantiles would not, and the p99/p95 ratio (11 at n=25,
  536 at n=50 versus 1.36 and 1.31 for ncx2) would still rule out ncx2.
- Both seeds are pooled, as cycle 75 pooled them; per-seed splits are in the
  CSV columns of the archived draw files.
