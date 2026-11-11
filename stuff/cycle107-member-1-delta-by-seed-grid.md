# Cycle 107: w=0.75 Fisher minus S2 on a DELTA-by-seed grid (member-1)

Seeds: 107011, 107023, 107039 (new; not used in cycles 100 to 106). The same three seeds are used at every DELTA.

Script: `stuff/cycle107-member-1-delta-by-seed-grid.py`, run once per seed as `python3 stuff/cycle107-member-1-delta-by-seed-grid.py SEED` (about 100 s each). n=400, 20000 paired draws per cell, nine cells.

- Statistic: F_0.75 = -2[0.75 ln p_S2 + 0.25 ln p_SW], with p_SW from Royston's log(1-W) normal approximation and p_S2 = exp(-(Z1^2+Z2^2)/2) from D'Agostino-Pearson K^2. Same code as cycle 106.
- Alternative: x = (DELTA |g1| + sqrt(1-DELTA^2) g2) / sqrt(chi2_10 / 10).
- Within a seed, each DELTA restarts `random.Random(SEED)`, so the three DELTA cells of a seed share the same underlying normal and chi-square draws. Only DELTA changes.
- Critical values come from a separate stream, `random.Random(SEED + 5000000)`: 95th percentile of 20000 N(0,1) samples, then checked on a further 20000.
- Measured sqrt(beta1) is the pooled sample skewness of all 8,000,000 values drawn in that cell, not a nominal figure.

## Critical values at n=400, exact-size 5% (before any table)

| seed | S2 rejects when | S2 null rate | F w=0.75 rejects when | F w=0.75 null rate |
|---|---|---|---|---|
| 107011 | p < 0.04714 | 0.0491 | stat > 6.0202 | 0.0490 |
| 107023 | p < 0.04860 | 0.0513 | stat > 5.9259 | 0.0500 |
| 107039 | p < 0.04844 | 0.0506 | stat > 5.8712 | 0.0517 |

Binomial SE of each null rate is 0.0015; all six are within 1.2 SE of 0.05.

## Margin per cell: w=0.75 minus S2 (paired SE), measured sqrt(beta1)

| seed | DELTA 0.63 | DELTA 0.68 | DELTA 0.75 | within-seed range |
|---|---|---|---|---|
| 107011 | -0.0015 (0.0009), -1.7 SE, sqrt(beta1) 0.330 | -0.0005 (0.0008), -0.6 SE, 0.388 | +0.0011 (0.0007), +1.6 SE, 0.493 | 0.0026 |
| 107023 | +0.0030 (0.0009), +3.3 SE, 0.330 | +0.0004 (0.0008), +0.5 SE, 0.389 | +0.0027 (0.0007), +3.9 SE, 0.493 | 0.0026 |
| 107039 | +0.0034 (0.0009), +3.9 SE, 0.330 | +0.0026 (0.0008), +3.2 SE, 0.389 | +0.0025 (0.0006), +3.9 SE, 0.494 | 0.0009 |
| across-seed range | 0.0049 | 0.0031 | 0.0016 | |
| mean over seeds | +0.0016 | +0.0008 | +0.0021 | |

Power (S2 / F w=0.75): seed 107011 0.7793/0.7779, 0.8267/0.8262, 0.9032/0.9043; seed 107023 0.7868/0.7898, 0.8338/0.8342, 0.9045/0.9072; seed 107039 0.7903/0.7937, 0.8357/0.8383, 0.9085/0.9110. No cell is at the power ceiling.

## Spread: within seed across DELTA versus across seeds at fixed DELTA

- Within-seed range across DELTA: 0.0026, 0.0026, 0.0009 (mean 0.0020).
- Across-seed range at fixed DELTA: 0.0049, 0.0031, 0.0016 (mean 0.0032).
- Seed means: -0.0003, +0.0020, +0.0028. DELTA means: +0.0016, +0.0008, +0.0021.

The seed drives the margin more than DELTA does. The across-seed spread is larger at two of the three DELTA values, and it is largest (0.0049, about 5 paired SE) at DELTA 0.63, the cell nearest the 0.3 target. The DELTA means are not monotone: the middle value 0.68 is lowest, and the three seeds disagree on direction (107011 rises with DELTA, 107039 falls slightly, 107023 dips in the middle).

## Answer

- w=0.75 does not reliably beat S2 here. It leads by more than 2 paired SE in 5 of 9 cells, all on seeds 107023 and 107039; on seed 107011 it is within 2 SE of S2 at every DELTA, and behind at two.
- The cycle 106 "fade toward sqrt(beta1) 0.3" is not a skewness effect: at measured sqrt(beta1) 0.330 the margin is -1.7, +3.3 and +3.9 SE depending on the seed alone.
- Every margin is at most 0.34 percentage points of power.

## Limits

- The paired SE covers only the alternative draws. Each seed's critical values are themselves estimated from 20000 null draws and are shared by its three DELTA cells, so calibration error shifts a whole row together and is not in the paired SE. The S2 cutoff ranges from p < 0.04714 to p < 0.04860 across seeds, and the seed with the strictest cutoffs (107011) is the one where w=0.75 does not lead. The across-seed spread therefore mixes alternative-draw noise with calibration noise, and this run cannot separate them.
- Because the DELTA cells of a seed share draws, the within-seed range is smaller than it would be with independent draws; that favours finding a DELTA effect, and none consistent across seeds showed up.
- Three seeds and three DELTA values; ranges, not variance estimates.
