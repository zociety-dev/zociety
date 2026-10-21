# Recovery trace: one in-order pass, no retroactive change

A worked example of rules 1 and 2. It checks that a later log event restores
a pulled cutoff without editing any earlier verdict.

## Setup

- Honest key **H** makes cuts at log positions 2, 4, 6, 8, 10.
- Countersigner **C** is stolen at position **t = 3**.
- The forger signs a revocation of H as C at position 3.
- C's real owner notices and revokes C at position **p = 7**.

## Pass, in log order

| pos | event               | verdict for H's cut | why (events before pos only)          |
|-----|---------------------|---------------------|---------------------------------------|
| 2   | H cut               | counts              | no revocation yet                     |
| 3   | forged C-revokes-H  | (none)              | C has not been revoked, so it counts  |
| 4   | H cut               | denied              | the forged revocation is in force     |
| 6   | H cut               | denied              | still inside (t, p]                   |
| 7   | C revoked by owner  | (none)              | from here on, C's revocations stop counting (rule 1) |
| 8   | H cut               | counts              | the forged revocation no longer counts |
| 10  | H cut               | counts              | same                                  |

## Checks

- **Fixedness (rule 2):** the verdicts at 4 and 6 were decided before
  position 7 and stay denied. Position 7 changes only verdicts after it.
- **Loss:** 2 denied cuts. Both fall in (t, p] = (3, 7], which has 4
  positions. That matches the worst-case bound p − t.
- **Recovery:** H gets its cutoff back at p without any recomputation. One
  in-order pass gives the final answer.

## Open edge

What happens if a cut and C's revocation land at the same position p? Then
the inclusion at the closed end of (t, p] decides the outcome. Rule 2 says
"events before q," so a cut at q = p does not see the revocation and is still
denied. The bound p − t therefore includes p.
