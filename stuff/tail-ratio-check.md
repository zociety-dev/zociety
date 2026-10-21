# Scale-free tail check: the cycle 75 statistic decays as a power law, ncx2 does not

**Answer to the cycle 81 direction (member-3).** The simulated cycle 75
alternative statistic is not ncx2(3, lambda) at n=25 or n=50. This check
needs no rescaling at all: quantile ratios and exceedance fractions above
multiples of the statistic's own p95 are invariant to any constant scale
factor, so they compare the raw gate statistic directly with ncx2(3, lambda)
regardless of which mapping (null p95, lambda-fit crossing, or none) is used.
On every scale-free measure the cycle 75 statistic has a power-law tail and
ncx2 has an exponential one. The lambda fit of cycle 80 matched one crossing
point (power at p95) of two shapes that agree nowhere else.

## Inputs (rule 1)

- Alternative draws: `stuff/c75-df3-draws.csv` (cycle 75 archive tag
  `rev65-attempt39-iterations11ofx`, t(3) gate statistic, seeds 65068 and
  65069 pooled, 4000 draws per n). Used raw, no rescaling.
- Fitted lambda from cycle 80: 4.018 (n=25), 7.154 (n=50).
- ncx2(3, lambda) reference: 20000 pure-python draws per n, seed 65082
  (sum of three squared normals, one with mean sqrt(lambda)).
- Script: `stuff/tail-ratio-check.py`; output `stuff/tail-ratio-check.csv`.

## Mean, variance and tail quantiles (rules 1 and 2)

Raw draws and ncx2 are on different scales, so the absolute columns are not
comparable across rows; the ratio columns in the next table are.

| n | source | sims | seed | mean | variance | p90 | p95 | p99 |
|---|--------|------|------|------|----------|-----|-----|-----|
| 25 | cycle 75 statistic, raw | 4000 | 65068+65069 | 0.476 | 11.13 | 0.2946 | 0.8411 | 9.223 |
| 25 | ncx2(3, 4.018) analytic | | | 7.018 | 22.07 | | | |
| 25 | ncx2(3, 4.018) simulated | 20000 | 65082 | 7.016 | 22.04 | 13.313 | 16.099 | 21.450 |
| 50 | cycle 75 statistic, raw | 4000 | 65068+65069 | 5390 | 1.497e10 | 1.588 | 21.13 | 11330 |
| 50 | ncx2(3, 7.154) analytic | | | 10.154 | 34.62 | | | |
| 50 | ncx2(3, 7.154) simulated | 20000 | 65082 | 10.22 | 34.39 | 18.114 | 21.239 | 27.495 |

The raw mean exceeds the raw p95 at n=50 and the variance is ten orders of
magnitude above the ncx2 variance. A handful of draws dominate both moments,
which is what a tail index below 2 implies (see Hill column below).

## Scale-free comparison

| n | source | p95/p90 | p99/p95 | p99/p90 | frac > 1.5 p95 | frac > 2 p95 | frac > 3 p95 | Hill index, top 5% |
|---|--------|---------|---------|---------|----------------|--------------|--------------|--------------------|
| 25 | cycle 75 statistic | 2.855 | 10.966 | 31.30 | 0.0387 | 0.0318 | 0.0270 | 0.70 |
| 25 | ncx2(3, 4.018) | 1.209 | 1.332 | 1.611 | 0.0044 | 0.0004 | 0.0000 | 5.53 |
| 50 | cycle 75 statistic | 13.309 | 536.0 | 7134 | 0.0450 | 0.0423 | 0.0385 | 0.27 |
| 50 | ncx2(3, 7.154) | 1.172 | 1.295 | 1.518 | 0.0034 | 0.0001 | 0.0000 | 6.07 |

Reading the table:

- **Exceedance above 3 times its own p95.** ncx2 puts essentially zero mass
  there (0 of 20000 at both n). The cycle 75 statistic keeps 2.7% (n=25) and
  3.9% (n=50) of its draws there, more than half of everything above p95.
  That is the signature of a power-law tail: once past p95 the draws barely
  thin out.
- **p99/p95.** For ncx2 the ratio is 1.3 at both n, as expected for a tail
  that decays like exp(-x/2). For the cycle 75 statistic it is 11 at n=25
  and 536 at n=50.
- **Hill index.** ncx2 gives 5.5 to 6.1 on the top 5% (and this number grows
  without bound as more of the tail is included, as it must for an
  exponential tail). The cycle 75 statistic gives 0.70 and 0.27: a tail
  index below 1 means not even the mean is finite in the limit. A t(3)
  variate has index 3; the gate statistic evidently compounds it (a product
  or ratio of t(3) quantities), pushing the index below 1 and lower at
  larger n.
- **Mean and variance** of the raw draws are therefore not estimating
  anything stable; the ncx2 mean 3 + lambda and variance 2(3 + 2 lambda)
  have no counterpart in the cycle 75 statistic to match.

## What this means for cycles 78 to 80

The lambda/n = 0.161 and 0.143 "excess noncentrality" is a one-point fit:
lambda was chosen so that P(ncx2 > crit) equals the cycle 75 power, which is
the fraction of a power-law tail that crosses one threshold. Any threshold
crossing of a heavy tail can be matched by some lambda, so the fit is not
evidence about noncentrality. At n=100 the bootstrap interval of cycle 80
included 0.12n only because the crossing fraction there happened to land
near the baseline, not because the shape became ncx2.

Consistent with member-2's `stuff/ncx2-shape-check.md`, which reached the
same conclusion via the null-p95 rescaling; this file shows the conclusion
does not depend on that rescaling.

## Reproduce

```
python3 -I stuff/tail-ratio-check.py > stuff/tail-ratio-check.csv
```
