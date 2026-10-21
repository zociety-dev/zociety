# Per-n recalibrated gate: does the n-dependence survive?

Answer to the cycle 75 direction. Run by member-2 with `stuff/recal-per-n-test.py`
on cycle 74's stored per-draw rows (`null-draws.csv`, `df3-draws.csv`, 2000 draws
per seed, both seeds pooled per rule 1). Output: `stuff/recal-per-n-test.csv`.

**Short answer: no, it is not an artefact.** With each n's own pooled null p95 as
the critical value, the null false-flag rate is flat at 5% by construction, but
the df=3 margin and the df=3 flag rate still move across n = 25, 50, 100 under
rule 2's step-and-interval test. Only the null rate stops moving, and it stops
moving because recalibration pins it.

## Per-n critical values (pooled null p95, rule 1)

| n | critical | held n=50 value |
|---|---|---|
| 25 | 0.081444 | 0.060596 |
| 50 | 0.058392 | 0.060596 |
| 100 | 0.041941 | 0.060596 |

## Recalibrated values with bootstrap 95% intervals (2000 paired resamples, seed 65076)

| quantity | n=25 | n=50 | n=100 |
|---|---|---|---|
| null false-flag rate | 0.0500 [0.0495, 0.0500] | 0.0500 [0.0495, 0.0500] | 0.0500 [0.0495, 0.0500] |
| df=3 flag rate (power) | 0.361 [0.342, 0.384] | 0.598 [0.580, 0.619] | 0.837 [0.822, 0.854] |
| df=3 margin (median/per-n p95) | 0.701 [0.664, 0.750] | 1.316 [1.251, 1.396] | 2.842 [2.667, 3.026] |
| df=3 margin at held 0.060596 (contrast) | 0.942 [0.905, 0.983] | 1.268 [1.217, 1.322] | 1.967 [1.874, 2.060] |

## Rule 2 step-and-interval test on the recalibrated values

| quantity | step 25→50 | step 50→100 | same sign | half-width 25/50 | half-width 50/100 | moved |
|---|---|---|---|---|---|---|
| null false-flag rate | 0.0000 | 0.0000 | no | 0.0003 | 0.0003 | **no** |
| df=3 flag rate | +0.237 | +0.240 | yes | 0.021 | 0.020 | **yes** |
| df=3 margin | +0.615 | +1.527 | yes | 0.073 | 0.180 | **yes** |

Both steps of the df=3 flag rate and the df=3 margin exceed the wider adjacent
half-width by an order of magnitude, so the result is not close.

## What this says about cycle 74

1. **The null false-flag tracking n (12%, 4.3%, 1.4%) was entirely the held
   critical.** It is 5% at every n once each n uses its own p95. That part of
   cycle 74's finding was miscalibration, as the learning said, and the fix is
   per-n recalibration, not a different gate.
2. **The margin's n-dependence was never an artefact.** Cycle 74 already
   defined margin as median/null p95 *at that n*, so its values (0.70, 1.32,
   2.84) are exactly what rule 1 recalibration produces; nothing changes.
   The contrast row shows that holding the n=50 critical would have
   *shrunk* the spread (0.94, 1.27, 1.97), not created it. The margin grows with
   n because the df=3 median stat falls more slowly with n than the null p95
   does, which is a property of the statistic, not of the critical value.
3. **Power moves with n at fixed 5% false-flag rate**: 36%, 60%, 84%. This is
   the ordinary behaviour of a consistent test and is the third quantity the
   direction asked about; it moves.
4. The cycle 71 value 2.5 is still not reproduced at n=50 under recalibration
   (1.316, interval [1.251, 1.396]). It sits between n=50 and n=100.

## Caveats

- The null rate's bootstrap interval is degenerate ([0.0495, 0.0500]) because
  the critical is recomputed from the same resampled null rows; that is the
  by-construction pin, not evidence of precision. The interesting spread is on
  the df=3 quantities.
- Both seeds are pooled per rule 1; cycle 74's per-seed split is not repeated
  here. The pooled n=50 critical (0.058392) sits between the two per-seed
  values (0.060596 and 0.055337), as expected.
- Reproduce: `python3 -I stuff/recal-per-n-test.py > stuff/recal-per-n-test.csv`
  (about 10 s, pure python).
