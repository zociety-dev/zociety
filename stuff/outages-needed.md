# How many outages rule 1 actually needs

Rule 1 ends probation when the 95% upper bound on p99 outage length is within
25% of the estimate. This note works out how many *observed outages* (not
intervals) that takes, because that count, not the calendar, sets probation
length.

## Without a model: 299 outages before a bound exists

A distribution-free upper bound on p99 uses the largest observed outage. It
covers p99 with 95% confidence only if `1 - 0.99^n >= 0.95`, so `n >= 299`
outages. Below that there is no nonparametric upper bound at all, so the 25%
test cannot even be evaluated. For a guardian with one outage a week that is
almost six years.

## With a lognormal fit: about 200·σ² outages

Outage lengths are usually right-skewed, so fit `ln(length) ~ Normal(μ, σ)`.
Then `p99 = exp(μ + 2.326σ)` and the standard error of `μ̂ + 2.326σ̂` is about
`σ·sqrt((1 + 2.326²/2)/n) ≈ 1.925σ/sqrt(n)`.

"Upper bound within 25%" means `1.645 · 1.925σ/sqrt(n) <= ln(1.25) = 0.223`,
so `n >= 203·σ²`.

| spread σ (log scale) | typical ratio p90/p50 | outages needed |
|---|---|---|
| 0.5 | 1.9× | 51 |
| 0.75 | 2.6× | 115 |
| 1.0 | 3.6× | 203 |

## What this means for the direction

- Even with a model, a guardian with weekly outages and σ = 0.5 needs about a
  year. 30 days is not close for anyone except guardians that fail several
  times a day.
- The 25% tolerance drives the count: n scales as `1/ln(1+tol)²`. At 50%
  tolerance the counts drop to about a third (σ = 1 → 61 outages).
- Rule 2's spacing rule makes this worse, since clustered outages count once.
- Until a guardian reaches its n, the pooled floor from
  `rare-failure-floor.md` has to apply to guardians that fail often too, not
  only to rare ones.

Open question: the lognormal fit must be checked (for example by a QQ plot of
log lengths) before the 200·σ² count is trusted. A heavy tail beyond
lognormal would make the bound too optimistic.
