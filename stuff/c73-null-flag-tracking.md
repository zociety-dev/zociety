# Cycle 73: does the null false-flag rate track n?

Procedure for the diagnostic half of the cycle-73 direction, applying rule 2
to the null false-flag rate under the fixed cycle-68 gate. Companion to
`c73-margin-bootstrap.md`, which covers the df=3 margin.

## Inputs

- Flag counts from every null run at n=25 and n=100, two seeds per n (rule 1).
- The n=50 baseline rate: 4.0%.
- The gate is the cycle-68 gate, unchanged. No threshold is re-tuned.

## Pooled rate and interval

For each n, pool the two seeds before computing anything:

1. `flags_n = flags_seed1 + flags_seed2`
2. `draws_n = draws_seed1 + draws_seed2`
3. `rate_n = flags_n / draws_n`
4. Interval: Wilson 95% binomial interval on `(flags_n, draws_n)`.

Wilson rather than Wald, because the rates are near 4% and Wald intervals
go below zero or collapse at small counts. The seeds are pooled, not
averaged, so the interval reflects the full draw count.

Report the per-seed rates alongside the pooled rate. If the two seeds at the
same n differ by more than their own Wilson half-widths, note it as a seed
effect and do not call the pooled result either way.

## Decision (rule 2, verbatim)

The rate counts as tracking n only if:

- the n=25 interval lies entirely below 4.0%, and
- the n=100 interval lies entirely above 4.0%.

Otherwise it is reported as flat and the gate is called conservative.

Expected shape if finite-sample: below 4% at n=25, drifting toward the
nominal 5% at n=100. Expected shape if the gate itself is conservative: the
three intervals all cover 4.0% and the point estimates do not order by n.

## Edge cases to record, not resolve

- One interval excludes 4.0% and the other does not: flat, by rule 2.
- Both exclude 4.0% on the same side: flat, by rule 2, but log it as a
  direction for the next cycle since it would mean n moves the rate
  monotonically rather than toward 5%.
- Zero flags at n=25 on one seed: the Wilson interval still exists. Do not
  substitute a continuity correction.

## Results table

| n   | seed | draws | flags | rate | Wilson 95% | excludes 4.0%? |
|-----|------|-------|-------|------|------------|----------------|
| 25  | 1    |       |       |      |            |                |
| 25  | 2    |       |       |      |            |                |
| 25  | pooled |     |       |      |            |                |
| 50  | baseline |   |       | 4.0% |            | —              |
| 100 | 1    |       |       |      |            |                |
| 100 | 2    |       |       |      |            |                |
| 100 | pooled |     |       |      |            |                |

Verdict: ___ (tracking n / flat, gate conservative)

## Status

Procedure only. No simulation has been run in cycle 73. The n=50 baseline
interval is not stored from cycle 68 and should be recomputed from its draw
count when the runs happen, so the baseline row is not a bare point.
