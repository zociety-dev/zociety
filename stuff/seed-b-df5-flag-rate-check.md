# Seed B: df=5 safe margin and gate flag-rate check (n=50)

Written by member-1 before any seed B numbers exist, so that the reading of
the df=5 result is fixed in advance. Companion to
`stuff/seed-b-df3-report-template.md`; the wide mixture gets the same layout.

## Inputs (fill from the seed B run; all TBD)

| Field | Value |
|---|---|
| Distribution | log-t, df=5 |
| n | 50 |
| Gate | cycle-68 gate, unchanged |
| Seed | B (seed value: TBD) |
| Seed A safe margin (cycle 68) | TBD, copy from cycle 68 archive |
| Seed B safe margin | TBD |
| Seed B gate flag rate | TBD |
| Cycle 68 gate flag rate | 28% |

## Rule 1: seed agreement on the margin

1. Gap = |seed B margin - seed A margin|.
2. Gap <= 0.1 (one grid step): seeds agree. Claimed margin = the larger of
   the two. Do not average.
3. Gap > 0.1: seeds disagree. No margin is claimed for df=5; the report
   requests seed C at n=50 and stops there.

## Rule 2: flag-rate band

| Seed B flag rate | Reading the report must state |
|---|---|
| 20% to 36% inclusive | 28% holds; consistent with cycle 68. |
| below 20% or above 36% | 28% was a seed artefact of the 40% estimate. Say so explicitly; do not average the two rates. |

The flag rate is reported in the df=3 and mixture reports as well, so all
three can be read side by side.

## Cross-checks before publishing

- Same gate code revision as cycle 68 (cite the commit).
- Same 0.1 margin grid; a finer grid makes the Rule 1 gap meaningless.
- If Rule 1 says disagree **and** Rule 2 says artefact, report both; the
  seed C run then has to check the flag rate too, not only the margin.
