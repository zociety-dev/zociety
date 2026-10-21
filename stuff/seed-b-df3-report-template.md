# Seed B at n=50: log-t df=3 report template (member-3)

Cycle 70 direction: under the cycle-68 gate at n=50, what safe margins does
seed B give for log-t df=3, df=5 and the wide mixture, and does the df=5 gate
flag rate stay near 28%?

This file fixes the shape of the df=3 report before any numbers exist, so the
result cannot be fitted to the rules after the fact. No simulation has been run
for it yet. Every value below marked `TBD` must be filled from an actual seed B
run, not estimated.

## Inputs

| Field            | Value                                  |
|------------------|----------------------------------------|
| Distribution     | log-t, df=3                            |
| n                | 50                                     |
| Gate             | cycle-68 gate, unchanged               |
| Margin grid      | 0.1 steps                              |
| Seed A margin    | 2.5 (cycle 68, provisional)            |
| Seed B margin    | TBD                                    |

## Rule 1 check (seed agreement)

- |seed B − 2.5| ≤ 0.1 → seeds agree. Claimed safe margin = max(2.5, seed B).
- |seed B − 2.5| > 0.1 → seeds disagree. Do NOT average. Run seed C at n=50
  and report all three margins; the claim waits for seed C.

Result: TBD (agree / disagree), claimed margin: TBD.

## Rule 2 check (df=5 flag rate)

Rule 2 is about df=5, not df=3. The df=3 report still states it so the three
reports read side by side:

- df=5 gate flag rate under seed B: TBD (from the df=5 report)
- Cycle 68 figure: 28%
- Inside the 20%–36% band? TBD. If not, the report must say explicitly that
  the 28% figure is a seed artefact.

## What would make df=3 interesting

df=3 is the heaviest tail of the three. If seed B's margin comes in above 2.6,
the provisional 2.5 was too tight and the larger value becomes the claim under
rule 1, but only after seed C confirms it. If it comes in at 2.4–2.6, cycle 68's
number stands and df=3 stops being provisional.
