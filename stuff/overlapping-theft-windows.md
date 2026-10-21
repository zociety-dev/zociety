# Overlapping theft windows

Rules 1 and 2 cover one stolen countersigner. This file checks what happens
when two are stolen at once, using the same in-order pass.

## Setup

- Countersigner A is stolen and forges a revocation of honest key K at log
  position 2. A's own revocation counts at position 6.
- Countersigner B is stolen and forges a revocation of K at position 4.
  B's own revocation counts at position 9.
- K makes cuts at positions 1, 3, 5, 7, 8 and 10.

## Pass (each cut sees only events before it, per rule 2)

| cut | forged revocations still counting | result |
|-----|-----------------------------------|--------|
| 1   | none                              | valid  |
| 3   | A (2 < 3, A not revoked until 6)  | denied |
| 5   | A, B                              | denied |
| 7   | B (A revoked at 6 < 7)            | denied |
| 8   | B                                 | denied |
| 10  | none (B revoked at 9 < 10)        | valid  |

## What this shows

- K is denied while **any** forged revocation still counts, so the denied
  span is the union of the windows: (2, 6] ∪ (4, 9] = (2, 9].
- Recovery is still forward-only: cut 10 counts again and no earlier cut is
  recomputed. Revoking A at 6 did not restore cut 7, because B still counted.
- Worst-case loss is bounded by the length of the union, here 9 − 2 = 7
  positions, not by the sum of the separate windows (4 + 5 = 9). The bound in
  rule 1 holds per window; for several thefts the bound is their union.
