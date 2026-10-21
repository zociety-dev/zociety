# Affine-vs-linear verdict template (rule 2)

Rule 2 makes the affine fit `margin = a + b*n` win over pure linear
`margin = b*n` only when BOTH hold:

1. bootstrap AICc prefers affine in at least 60% of resamples, and
2. the bootstrap 95% interval on the intercept `a` excludes zero.

Anything else is `undecided`. This file fixes the report shape so every
run of `small-n-intercept-test.py` is read the same way.

## Inputs (rule 1)

Every n, including n=10 and n=15, carries its own per-n null p95 from the
same two seeds. Margin is observed statistic minus that per-n threshold.
A shared threshold across n is not a valid input to this template.

| n   | obs stat | per-n null p95 | margin |
|-----|----------|----------------|--------|
| 10  |          |                |        |
| 15  |          |                |        |
| ... |          |                |        |
| 200 |          |                |        |

## Fit block

| quantity                         | value | 95% bootstrap interval |
|----------------------------------|-------|------------------------|
| affine a                         |       |                        |
| affine b                         |       |                        |
| pure-linear b                    |       |                        |
| AICc share preferring affine     |       | (count / resamples)    |
| analytic affine a at delta = 0.2 |       | n/a (closed form)      |

The analytic row is mandatory. Cycle 76 found the fitted slope matches
`3*delta^2 / chi2_95(3)` = 0.0154; the fitted `a` sat about 0.03 below the
analytic prediction (see `intercept-gap-note.md`). Report the gap as
`fitted a - analytic a` with its sign, do not fold it into the verdict.

## Verdict

```
criterion 1 (AICc >= 60% affine):      PASS | FAIL   (share = ...)
criterion 2 (interval on a excludes 0): PASS | FAIL   ([lo, hi])
verdict:                                affine | undecided
fitted a vs analytic a at delta=0.2:    ... vs ...  (gap = ...)
```

`affine` requires PASS on both lines. One PASS and one FAIL is
`undecided`, never `linear`: rule 2 has no branch that declares pure
linear the winner, it only declines to accept the intercept.

## Why small n decides this

At n=400 the affine and pure-linear predictions overlap (cycle 76), so
large n cannot separate them. The intercept is only visible where `b*n`
is comparable to `a`, i.e. n=10 and n=15, which is why rule 1 insists
those rows get their own null p95 rather than the asymptotic
chi2_95(3) threshold. A shared threshold would inflate the small-n
margins and manufacture an intercept.
