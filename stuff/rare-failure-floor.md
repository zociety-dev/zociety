# Grace floor for guardians that rarely fail

Rule 1 ends probation when the 95% upper bound on p99 outage is within 25% of
the estimate. A guardian with almost no outages never gets there: you can't
estimate the size of outages you haven't seen.

## What zero outages does tell you

If there are 0 outages in N independent counted intervals (spaced per rule 2),
the 95% upper bound on the per-interval outage *rate* is about 3/N (the rule of
three). For example:

| counted intervals N | rate bound (95%) |
|---|---|
| 30  | 10% |
| 100 | 3%  |
| 299 | 1%  |

At N = 299 the rate bound reaches 1%. That means p99 outage is 0 at 95%
confidence: in 99% of intervals there is no outage.

## Proposed floor before that point

Before N = 299, set the grace floor to the **fleet-pooled p99 outage length**,
which is the p99 over all graduated guardians' counted outages. Don't use the
guardian's own data. The guardian graduates early only if both of these hold:

- it reaches the 299-interval bound, so its floor can be its own measured
  value, or
- it records enough outages to meet rule 1's 25% test on its own data.

## Why not just keep 30 days

With daily intervals, 30 days gives a rate bound of 10%, which says nothing
about p99. A reliable guardian on a hand-picked 30 days gets a floor that has no
evidence behind it. The pooled floor at least uses real outages from similar
guardians.

## Open question

Pooling assumes the fleet is homogeneous. If a few guardians fail often and
with long outages, they push the pooled p99 up, and reliable guardians end up
with floors that are too long. A pooled value cut down to guardians of the same
type or provider would fix that, but each type then needs enough guardians to
pool from.
