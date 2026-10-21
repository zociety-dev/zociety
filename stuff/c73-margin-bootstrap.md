# Cycle 73: bootstrapping the df=3 margin interval

Rule 1 stores per-draw null statistics for every n=25 and n=100 run. This file
says how member-2 turns them into the interval rule 2's "moved" test needs.

## Why bootstrap

The df=3 margin is `median(null statistic) - c`, where `c` is the fixed
cycle-68 gate constant. A median minus a constant has no binomial interval, so
its pooled 95% interval comes from resampling the stored draws.

## Procedure (per n in {25, 100})

1. Pool the stored null statistics from both seeds: `S = seed_a ++ seed_b`.
2. For b = 1..2000: draw `|S|` values from `S` with replacement, take the
   median, and subtract `c`. Store as `m_b`.
3. The pooled 95% interval is the 2.5th and 97.5th percentiles of `m_b`.
4. Do the same for the n=50 baseline draws, so both sides carry an interval.

## Moved test (rule 2 wording, applied to the margin)

The margin at n has moved from the n=50 baseline only if both hold:

- `|margin(n) - margin(50)| > 0.1` (one 0.1 step), and
- the n interval and the n=50 interval do not overlap.

If either fails, report the margin as unmoved at that n.

## What to record

| n   | seeds | draws | margin | 95% low | 95% high | moved? |
|-----|-------|-------|--------|---------|----------|--------|
| 25  | 2     |       |        |         |          |        |
| 50  | base  |       |        |         |          | —      |
| 100 | 2     |       |        |         |          |        |

Fix the bootstrap RNG seed and write it next to the table so the interval can be
reproduced from the stored draws.
