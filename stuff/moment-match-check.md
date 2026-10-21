# Moment-match check: no ncx2(3, lambda) at any scale has the cycle 75 moments

**Answer to the cycle 81 direction (member-1).** The simulated cycle 75
alternative statistic is not ncx2(3, lambda) at n=25 or n=50, and the
mismatch is not a matter of which lambda or which rescaling is used. For
c * ncx2(3, lambda) the scale-free ratio var/mean^2 equals
2(3+2 lambda)/(3+lambda)^2, which is at most 2/3 (at lambda=0) and falls
toward 0 as lambda grows. The cycle 75 draws have var/mean^2 of 49 at n=25
and 515 at n=50, with bootstrap 2.5% bounds of 38 and 276. So there is no
lambda >= 0 and no scale factor c for which a three-degree-of-freedom
noncentral chi-square reproduces both the mean and the variance. Cycle 80's
lambda of 4.018 and 7.154 can therefore only have matched one quantile (the
p95 crossing), and the shape is heavier-tailed than any ncx2(3, lambda).

This is a third, independent route to the same conclusion as member-2
(null-p95 rescaling: variance 7 to 30 times too large) and member-3
(scale-free quantile ratios and Hill index below 1).

## Inputs (rule 1)

- Alternative draws: `stuff/c75-df3-draws.csv` (cycle 75 archive tag
  `rev65-attempt39-iterations11ofx`, t(3) gate statistic, seeds 65068 and
  65069, 2000 draws per seed per n, 4000 pooled). Used raw, no rescaling.
- Fitted lambda from cycle 80: 4.018 (n=25), 7.154 (n=50).
- Bootstrap of the pooled variance and var/mean^2: 400 resamples, seed 65083.
- ncx2(3, lambda_80) reference scaled to the empirical mean: 20000
  pure-python draws per n, seed 65084.
- Script: `stuff/moment-match-check.py`; output `stuff/moment-match-check.csv`.

## Mean, variance, and the scale-free moment ratio

| n | source | sims | seed | mean | variance | var/mean^2 | ncx2 max | implied lambda |
|---|---|---|---|---|---|---|---|---|
| 25 | cycle 75 raw | 2000 | 65068 | 0.4973 | 14.01 | 56.6 | 0.667 | none |
| 25 | cycle 75 raw | 2000 | 65069 | 0.4546 | 8.25 | 39.9 | 0.667 | none |
| 25 | cycle 75 raw | 4000 | pooled | 0.4760 | 11.13 | 49.1 | 0.667 | none |
| 25 | bootstrap 2.5% / 97.5% | 400 | 65083 | | 6.81 / 16.96 | 38.4 / 60.1 | 0.667 | none |
| 25 | ncx2(3, 4.018), c=0.0678 | 20000 | 65084 | 0.4764 | 0.1035 | 0.456 | 0.667 | 4.018 |
| 50 | cycle 75 raw | 2000 | 65068 | 6725 | 2.41e10 | 533 | 0.667 | none |
| 50 | cycle 75 raw | 2000 | 65069 | 4056 | 5.83e9 | 355 | 0.667 | none |
| 50 | cycle 75 raw | 4000 | pooled | 5390 | 1.50e10 | 515 | 0.667 | none |
| 50 | bootstrap 2.5% / 97.5% | 400 | 65083 | | 1.72e9 / 3.32e10 | 276 / 811 | 0.667 | none |
| 50 | ncx2(3, 7.154), c=530.9 | 20000 | 65084 | 5379 | 9.72e6 | 0.336 | 0.667 | 7.154 |

"Implied lambda" is the lambda that would give the observed var/mean^2;
it is "none" wherever that ratio exceeds 2/3, which is every cycle 75 row
and every bootstrap bound. At the matched mean, the cycle 80 ncx2 has a
variance 108 times too small at n=25 and 1540 times too small at n=50.

## Upper tail quantiles (rule 2)

Both rows per n share the same mean, so the quantiles are directly
comparable on the raw scale.

| n | source | p90 | p95 | p99 |
|---|---|---|---|---|
| 25 | cycle 75 raw, pooled | 0.295 | 0.841 | 9.22 |
| 25 | ncx2(3, 4.018) scaled to same mean | 0.912 | 1.094 | 1.485 |
| 50 | cycle 75 raw, pooled | 1.59 | 21.1 | 11327 |
| 50 | ncx2(3, 7.154) scaled to same mean | 9593 | 11137 | 14512 |

With the mean pinned, the cycle 75 statistic sits far below the ncx2 at p90
and p95 and far above it at p99 (6 times at n=25). Its mean is carried by
a handful of extreme draws: at n=50 the pooled mean of 5390 exceeds the
p95 of 21 by a factor of 255. No noncentral chi-square can have its mean
above its own p95; that alone rules out ncx2(3, lambda) at n=50.

## Reading

- The direction's "do its mean and variance match the fitted ncx2" has a
  stronger negative answer than a mismatch at the fitted lambda: the
  second moment is incompatible with the ncx2(3, .) family entirely.
- The per-seed moments differ by a factor of 1.7 (n=25) and 4 (n=50)
  across two seeds of 2000 draws each, and the bootstrap variance interval
  spans a factor of 2.5 and 19. Consistent with member-3's Hill index below
  1, the sample variance is not estimating a finite quantity.
- Any future lambda fit should be stated as "the lambda whose p95 power
  matches", not as a distributional fit, and reported with the mean and
  var/mean^2 of the draws so this check can be repeated.
