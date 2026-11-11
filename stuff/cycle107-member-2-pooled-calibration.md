# Cycle 107: how far member-1's per-seed cutoffs are from exact 5% (member-2)

Seeds: 107011, 107023, 107039, the same three as member-1's grid (new in cycle 107, same at every DELTA). No new alternative draws were made here; the nine-cell rerun is not done (see "Not done").

Script: `stuff/cycle107-member-2-pooled-calibration.py`, run as `uv run --no-project --with numpy python3 stuff/cycle107-member-2-pooled-calibration.py cal` (about 20 s). Same statistics as member-1's script; the numpy version agrees with the pure-Python one to 7.5e-13 on 50 samples.

## Critical values at n=400, exact-size 5% (before any table)

Pooled calibration, numpy stream `default_rng(107107)`: 95th percentile of 400,000 N(0,1) samples, checked on a further 400,000.

| source | S2 rejects when | S2 size on 400,000 check | F w=0.75 rejects when | F size on 400,000 check | F size minus S2 size |
|---|---|---|---|---|---|
| pooled (this item) | p < 0.04839 | 0.0499 | stat > 5.9212 | 0.0500 | +0.0001 |
| member-1, seed 107011 | p < 0.04714 | 0.0488 | stat > 6.0202 | 0.0476 | -0.0012 |
| member-1, seed 107023 | p < 0.04860 | 0.0501 | stat > 5.9259 | 0.0498 | -0.0003 |
| member-1, seed 107039 | p < 0.04844 | 0.0500 | stat > 5.8712 | 0.0511 | +0.0011 |

Binomial SE of each size is 0.00034. Member-1's own check (20,000 nulls, SE 0.0015) could not see these gaps.

## Margin per cell (member-1's numbers, unchanged) beside the size gap

w=0.75 minus S2 (paired SE), measured sqrt(beta1), from `stuff/cycle107-member-1-delta-by-seed-grid.md`:

| seed | F size minus S2 size | DELTA 0.63 | DELTA 0.68 | DELTA 0.75 | seed mean |
|---|---|---|---|---|---|
| 107011 | -0.0012 | -0.0015 (0.0009), 0.330 | -0.0005 (0.0008), 0.388 | +0.0011 (0.0007), 0.493 | -0.0003 |
| 107023 | -0.0003 | +0.0030 (0.0009), 0.330 | +0.0004 (0.0008), 0.389 | +0.0027 (0.0007), 0.493 | +0.0020 |
| 107039 | +0.0011 | +0.0034 (0.0009), 0.330 | +0.0026 (0.0008), 0.389 | +0.0025 (0.0006), 0.494 | +0.0028 |

Spread (member-1's): within-seed range across DELTA 0.0026, 0.0026, 0.0009; across-seed range at fixed DELTA 0.0049, 0.0031, 0.0016.

## What this shows

- The two tests were not held to the same size within a seed. On seed 107011 the Fisher cutoff is stricter than the S2 cutoff by 0.0012 of size; on seed 107039 it is looser by 0.0011.
- The seed order of the size gap (-0.0012, -0.0003, +0.0011) is the same as the seed order of the mean margin (-0.0003, +0.0020, +0.0028). The seed where w=0.75 fails to lead is the seed where Fisher was handicapped.
- So the across-seed spread that member-1 found to dominate is at least partly calibration error, not a property of the alternative draws. This item does not measure how much: a size gap is not a power gap, and converting one to the other needs the rerun below.
- It does not change the DELTA result. Calibration error is shared by a seed's three DELTA cells, so the within-seed ranges stand.

## Not done

The script's second mode (`python3 ... SEED 3.028365 5.921182`) replays member-1's exact alternative draws for one seed and reports each cell's margin under both the per-seed and the pooled cutoffs. It takes about 110 s per seed, did not fit this turn, and has not been run or tested. Running it for the three seeds would give the nine margins at a common, tighter-calibrated size and the across-seed spread with calibration noise removed.
