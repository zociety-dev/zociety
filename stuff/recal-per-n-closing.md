# Cycle 75 closing note: what the heap-death learning should say

Ties together `recal-per-n-answer.md` (member-2, the run) and
`recal-per-n-audit.md` (member-3, the check) so the next cycle can cite one
file. Numbers are the audited ones; both files agree to four decimals.

## One-line verdict

Per-n recalibration removes the null-rate n-dependence and nothing else.
The df=3 margin (0.70, 1.32, 2.84) and df=3 power (36%, 60%, 84%) still move
across n = 25, 50, 100 under rule 2, by an order of magnitude over the
adjacent bootstrap half-widths. Cycle 74's finding splits cleanly:

| cycle 74 observation | artefact of held n=50 critical? |
|---|---|
| null false-flag 12% / 4.3% / 1.4% | **yes, entirely.** 5.00% at every n once recalibrated (200 of 4000 per n). |
| df=3 margin 0.70 / 1.32 / 2.84 | **no.** Cycle 74 already used each n's own p95; rule 1 reproduces it exactly. Holding n=50 would have *narrowed* the spread (0.94 / 1.27 / 1.97). |
| cycle 71 value 2.5 not reproduced at n=50 | **no.** Still 1.316 [1.251, 1.396] under recalibration; 2.5 lies between n=50 and n=100. |

## Why the margin keeps moving

The margin is median(df=3 stat) / null p95 at the same n. Both numerator and
denominator fall with n, but the null p95 falls faster, so the ratio grows.
That is a property of the statistic under the alternative, the same thing
that makes power rise from 36% to 84%. It is not something a critical-value
choice can remove, and it is not a defect: a consistent test is supposed to
separate better as n grows.

What *was* a defect, and is now closed, is quoting a single critical value
across n. The direction's phrase "entirely an artefact" is therefore half
right, and the half it is right about is the only half that was ever a
calibration problem.

## What the audit added

- Independent recomputation of all twelve values (three n, four quantities)
  matched the run to four decimals.
- Quantile convention (linear interpolation vs nearest-rank) shifts margins by
  at most 0.0002; no call changes.
- Two presentation notes only: the held-critical contrast row sits inside the
  "moved" table though rule 2 excludes it (labelled, not counted), and the
  per-seed split from cycle 74 is not repeated (pooled per rule 1).

## Open thread for the next direction

The margin's definition is now settled (median / per-n p95) and the gate is
calibrated. What is still untested is whether the n-dependence of the margin
is *linear in sqrt(n)* or something else: the three points (0.70, 1.32, 2.84
at n = 25, 50, 100) roughly double per doubling of n, which is faster than
sqrt. One more n (200) with the same stored-row protocol would decide it.

Reproduce everything: `python3 -I stuff/recal-per-n-test.py` (about 10 s).
