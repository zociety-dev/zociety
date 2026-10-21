# Pooled interval recipe for the n=25 / n=100 replication

Rule 2 says a margin or flag rate has "moved" only when the shift from the
n=50 baseline exceeds both one 0.1 step and one pooled interval. Rule 1 says
the raw null statistics must be stored so these can be recomputed. This note
pins down how the pooled interval is computed so every sample size is judged
the same way.

## Inputs (from the stored raw null statistics)

For each run, keyed by `(seed, n, critical_value)`:

- `k_flag` — number of mixtures flagged, `m` — number of mixtures tested
- `k_null` — number of null draws exceeding the held critical value, `N` — null draws
- `stat_df3` — the df=3 margin: `(median test statistic - critical value)`, plus the
  per-draw statistics it was taken from

## Flag rates

Pool the two seeds at a given `n` before computing anything:

```
p_hat  = (k_flag_seedA + k_flag_seedB) / (m_A + m_B)
se     = sqrt( p_hat * (1 - p_hat) / (m_A + m_B) )
pooled interval = p_hat +/- 1.96 * se
```

Do the same for the n=50 baseline (seeds B and C from cycle 71). A rate has
moved only if `|p_hat_n - p_hat_50| > 0.1` **and** the n=50 point estimate
lies outside the new n's pooled interval.

## The df=3 margin

The margin is a difference of a sample median and a fixed number, so its
interval comes from the stored per-draw statistics, not from a binomial:

```
pool the per-draw statistics from both seeds at the given n
margin        = median(pooled) - critical_value
interval      = bootstrap 95% of the median (1000 resamples), shifted by -critical_value
```

Moved only if `|margin_n - 2.5| > 0.1` **and** 2.5 falls outside that interval.

## What to report, per sample size

| n   | seeds | df=3 margin (interval) | df=5 flag (interval) | wide-mix flag (interval) | null false-flag (interval) | verdict |
|-----|-------|------------------------|----------------------|--------------------------|----------------------------|---------|
| 25  | 2     |                        |                      |                          |                            |         |
| 50  | B, C  | 2.5                    | 30-31%               | 45-46%                   | 4.0% (3.5-4.7%)            | baseline|
| 100 | 2     |                        |                      |                          |                            |         |

The verdict column takes one of `stable`, `moved`, or `mixed` (step exceeded
but interval not, or the reverse). `mixed` is reported as stable under rule 2,
but the raw difference and interval are still shown so the call can be
challenged.

## One expectation to check

At n=25 the null false-flag interval will be roughly twice as wide as at n=50.
If the 4.0% conservative bias is a finite-sample effect of the held critical
value, it should shrink toward 5% at n=100 and widen below 4% at n=25. If it
stays at 4.0% across all three, the slack is in the gate itself, not in `n`.
