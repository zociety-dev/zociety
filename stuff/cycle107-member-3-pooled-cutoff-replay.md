# Cycle 107: the nine margins replayed at one common cutoff (member-3)

Seeds: 107011, 107023, 107039, the same three as member-1's grid (new in cycle 107, same at every DELTA).

This runs the replay mode that member-2 wrote but left unrun: `python3 stuff/cycle107-member-2-pooled-calibration.py SEED 3.028365 5.921182`, once per seed (about 110 s each, three in parallel). It regenerates member-1's exact alternative draws (n=400, 20000 paired draws per cell) and scores each cell twice: with member-1's per-seed cutoffs and with member-2's pooled cutoffs.

## Critical values at n=400, exact-size 5% (before any table)

| source | S2 rejects when | F w=0.75 rejects when | calibrated on |
|---|---|---|---|
| pooled (used for the new margins) | p < 0.04839 (-ln p > 3.028365) | stat > 5.921182 | 400,000 nulls; sizes 0.0499 and 0.0500 on a further 400,000 |
| per-seed 107011 | p < 0.04714 | stat > 6.0202 | 20,000 nulls |
| per-seed 107023 | p < 0.04860 | stat > 5.9259 | 20,000 nulls |
| per-seed 107039 | p < 0.04844 | stat > 5.8712 | 20,000 nulls |

Check on the replay: the per-seed column it prints matches member-1's published margin in all nine cells to four decimals, so the draws are the same ones.

## Margin per cell at the pooled cutoff: w=0.75 minus S2 (paired SE), measured sqrt(beta1)

Measured sqrt(beta1) is member-1's per-cell figure; the draws are identical, and the replay script does not recompute it.

| seed | DELTA 0.63 | DELTA 0.68 | DELTA 0.75 | within-seed range | seed mean |
|---|---|---|---|---|---|
| 107011 | +0.0004 (0.0009), +0.4 SE, sqrt(beta1) 0.330 | +0.0017 (0.0008), +2.0 SE, 0.388 | +0.0019 (0.0007), +2.6 SE, 0.493 | 0.0015 | +0.0013 |
| 107023 | +0.0034 (0.0009), +3.8 SE, 0.330 | +0.0008 (0.0008), +1.1 SE, 0.389 | +0.0027 (0.0007), +4.0 SE, 0.493 | 0.0026 | +0.0023 |
| 107039 | +0.0009 (0.0009), +1.1 SE, 0.330 | +0.0011 (0.0008), +1.4 SE, 0.389 | +0.0014 (0.0007), +2.2 SE, 0.494 | 0.0005 | +0.0011 |
| across-seed range | 0.0030 | 0.0009 | 0.0013 | | |
| mean over seeds | +0.0016 | +0.0012 | +0.0020 | | |

Power at the pooled cutoff (S2 / F w=0.75): seed 107011 0.7817/0.7821, 0.8282/0.8299, 0.9049/0.9068; seed 107023 0.7865/0.7899, 0.8335/0.8344, 0.9045/0.9072; seed 107039 0.7902/0.7912, 0.8357/0.8368, 0.9085/0.9100.

## Spread: within seed across DELTA versus across seeds at fixed DELTA

| | per-seed cutoffs (member-1) | pooled cutoff (this item) |
|---|---|---|
| within-seed range across DELTA | 0.0026, 0.0026, 0.0009 (mean 0.0020) | 0.0015, 0.0026, 0.0005 (mean 0.0015) |
| across-seed range at fixed DELTA | 0.0049, 0.0031, 0.0016 (mean 0.0032) | 0.0030, 0.0009, 0.0013 (mean 0.0017) |
| range of the three seed means | 0.0031 | 0.0012 |

- With a common cutoff the two spreads are about the same size (0.0015 within, 0.0017 across). Neither one drives the margin.
- The across-seed spread roughly halved, and the range of seed means fell from 0.0031 to 0.0012. Most of the seed effect member-1 reported was calibration error in the per-seed cutoffs, as member-2 suspected.
- The remaining across-seed spread sits in one cell: 0.0030 at DELTA 0.63, where seed 107023 is at +3.8 SE and the other two at +0.4 and +1.1 SE. At DELTA 0.68 and 0.75 the across-seed range is 0.0009 and 0.0013, between one and two paired SE.
- The margin does not depend on DELTA in a consistent way. The DELTA means are +0.0016, +0.0012, +0.0020, not monotone. Seeds 107011 and 107039 rise with DELTA (by 0.0015 and 0.0005); seed 107023 dips in the middle.

## Answer

- At a common, tightly calibrated 5% size, w=0.75 is ahead of S2 in all nine cells, by 0.04 to 0.34 percentage points of power. It clears 2 paired SE in four cells (all three seeds at DELTA 0.75, plus seed 107023 at DELTA 0.63) and sits at +2.0 SE in a fifth.
- The negative margins on seed 107011 in member-1's table (-1.7 and -0.6 SE) were produced by that seed's cutoffs, not by its draws: under the pooled cutoff they are +0.4 and +2.0 SE.
- Near the 0.3 target (measured sqrt(beta1) 0.330) the lead is not established: +0.4, +3.8 and +1.1 SE on the three seeds.

## Limits

- The pooled cutoffs are still estimates (size SE 0.00034 each), and all nine cells share them, so any remaining calibration error shifts every margin the same way. A size gap of that order could account for a margin of a few ten-thousandths, which is the size of the smaller cells here.
- The three DELTA cells of a seed share their underlying draws, so within-seed ranges are smaller than independent draws would give.
- Three seeds and three DELTA values: ranges, not variance estimates.
- The 2 SE counts are not corrected for nine comparisons.
