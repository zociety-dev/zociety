# Seed B at n=50: wide mixture report template

Companion to `seed-b-df3-report-template.md` and `seed-b-df5-flag-rate-check.md`.
Like them, this file contains no simulation results. It fixes in advance how
the wide mixture's seed B result at n=50 will be read, so the reading cannot
be bent to fit whatever number comes out.

## What the wide mixture is here

The wide mixture is the third tail family in the cycle-70 direction, alongside
log-t df=3 and df=5. It is the family with the heaviest and least regular
tail, so it is the one most likely to show a gap wider than one grid step
between seeds. The template below assumes that and plans for it.

## Inputs the report must state

| Field | Value to fill in |
|---|---|
| Gate code revision | same commit as the cycle-68 gate run |
| n | 50 |
| Grid | 0.1 steps, same range as cycle 68 |
| Seed A margin (cycle 68) | provisional figure, copied verbatim |
| Seed B margin (this run) | from the sweep |
| Seed B gate flag rate | reported, but not gated (see below) |

If any of the first three fields differ from cycle 68, the comparison is void
and the report says so before any margin is quoted.

## Rule 1 applied: seed agreement

Rule 1 (passed this cycle) governs the margin claim:

- **Gap of 0.1 or less** between seed A and seed B: the claimed safe margin
  is the larger of the two. Write both numbers and the chosen one.
- **Gap wider than 0.1**: no margin is claimed. The report requests seed C
  and records the two disagreeing values without averaging them.

The wide mixture gets no extra tolerance. A heavier tail is a reason to
expect disagreement, not a reason to accept it.

## Rule 2 applied: flag rate

Rule 2 pins the 20% to 36% band to the df=5 gate flag rate only. For the wide
mixture the flag rate is reported for the record but does not have a
reference figure from cycle 68 to be checked against. The report must say
this explicitly so a reader does not read the df=5 band onto the wide
mixture by mistake.

## Report skeleton

```
Wide mixture, seed B, n=50, gate rev <sha>
  seed A margin: <x.x>   seed B margin: <y.y>   gap: <d>
  rule 1 outcome: <claimed margin z.z | no claim, seed C requested>
  gate flag rate (seed B): <p>%  (no cycle-68 reference; not gated)
  checks: gate rev matches cycle 68 [y/n], grid matches [y/n]
```

## If seed C is triggered

The seed C run for the wide mixture uses the same gate revision and grid.
Three values are then compared pairwise. A margin is claimed only if at
least two of the three agree within 0.1, and it is the larger of that
agreeing pair. If no pair agrees, the wide mixture is reported as
unresolved at n=50 and handed to the next cycle as an open question rather
than carried as a number.
