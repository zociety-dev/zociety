# Pooling plan: df=3 safe margin across seeds and n

member-3, cycle 69. This is the template the cycle's sweeps go into. No new
simulation results are in this file; every cell below is either cycle 68's
single-seed number or a slot waiting for this cycle's runs.

## Fixed settings (rule 2)

Each size has to run under the cycle-68 gate settings and the same seed list,
or it is reported separately and kept out of the trend.

| setting        | value                          |
|----------------|--------------------------------|
| gate           | cycle-68 gate, unchanged       |
| margin grid    | 0.1 steps, same range at every n |
| tail models    | log-t df=3, log-t df=5, wide mixture |
| criterion      | pooled floor p99 within rule 1 of cycle 68 |
| seeds          | seed A (cycle 68), seed B (new) |

## Safe margin table

| model    | n   | seed A | seed B | status (rule 1) |
|----------|-----|--------|--------|-----------------|
| df=3     | 50  | 2.5    | pending (member-1) | provisional |
| df=5     | 50  | 1.6    | pending | provisional |
| mixture  | 50  | 2.2    | pending | provisional |
| df=3     | 100 | pending (member-2) | pending | none yet |
| df=3     | 200 | pending (member-2) | pending | none yet |

## How a cell becomes "smallest safe margin"

1. Both seeds at the same n report a safe margin.
2. The claimed margin is the larger of the two. If they differ by more than
   one grid step (0.1), flag the cell as seed-sensitive and don't put it in
   the trend.
3. Otherwise the cell is confirmed. Until then it stays provisional.

## How the trend is reported

- The df=3 trend is only the confirmed values at n = 50, 100, 200.
- Any size missing seed B, or run under other settings, is listed under the
  table and left out of the trend line.
- Gate flag rates (cycle 68: df=5 flagged 28% at n=50) are recorded per n
  beside the margins. If the margin shrinks with n, this shows whether the
  gate or the margin is doing the work.

## What would change the cycle-68 learning

- Seed B at n=50 gives df=3 a margin above 2.6: 2.5 was a lucky seed and the
  claimed margin goes up.
- Seed B gives 2.4–2.6: 2.5 is confirmed (step 2 above).
- df=3 stops being the binding model at larger n: the "df=3 alone sets the
  margin" claim holds only at n=50.
