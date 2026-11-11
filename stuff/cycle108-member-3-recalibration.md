# Cycle 108: does the ten-seed margin survive a fresh cutoff calibration? (member-3)

Script: `stuff/cycle108-member-3-recalibration.py`, run as `uv run --no-project --with numpy python3 stuff/cycle108-member-3-recalibration.py` (about 30 s).

member-2's item left one limit open: all ten seeds share one cutoff pair, so calibration error is common to them and is missing from the across-seed SE. This item measures that error.

## Setup

- Power draws: the same ten seeds, DELTA 0.63, n=400, 20,000 paired draws each, and the same statistics as member-2's script (the code is copied, not rewritten).
- Null samples: four new streams, numpy seeds 108201, 108211, 108223, 108227, each 400,000 N(0,1) samples of size 400. None was used by member-2 (null seed 108999).
- Each null sample gives its own cutoff pair (95th percentiles). Its size is then checked on the other three samples (1,200,000 draws).
- A fifth cutoff pair comes from all 1,600,000 nulls pooled.

## Results

| calibration | S2 cutoff | Fisher cutoff | mean margin | across-seed SE | mean / SE | positive seeds | size gap (Fisher minus S2) |
|---|---|---|---|---|---|---|---|
| 108201 | 3.034862 | 5.929898 | +0.00103 | 0.00031 | +3.3 | 9/10 | -0.00013 |
| 108211 | 3.038147 | 5.928934 | +0.00138 | 0.00030 | +4.5 | 10/10 | +0.00011 |
| 108223 | 3.026255 | 5.902316 | +0.00154 | 0.00028 | +5.5 | 10/10 | +0.00022 |
| 108227 | 3.044201 | 5.949164 | +0.00097 | 0.00029 | +3.4 | 7/10 | -0.00021 |
| pooled 1,600,000 | 3.035760 | 5.927409 | +0.00123 | 0.00031 | +4.0 | 9/10 | not measured |

- member-2's calibration (seed 108999) gave +0.00109, inside this range.
- Mean of the four mean margins: +0.00123. SD across the four calibrations: 0.00028.

## What this shows

- The lead is positive under every one of five independent calibrations (four here plus member-2's), from +0.00097 to +0.00154.
- Calibration error for a 400,000-draw null sample is about 0.00028, nearly as large as the across-seed SE (0.00031). So member-2's "3.5 SE" was overstated: with both sources combined the SE is about 0.00042, and +0.00109 is about 2.6 SE.
- With the pooled 1,600,000-draw cutoffs the calibration error should halve to about 0.00014. Combined SE is then about 0.00034, and the margin +0.00123 is about 3.6 SE. It still exceeds two SE.
- The margin moves with the size gap: the two calibrations where Fisher's size came out above S2's give the two largest margins, and the two where it came out below give the two smallest. Even at a size gap of -0.0002 against Fisher the margin is +0.00097.

## Limits

- The calibration SD rests on four values, so it is rough.
- The four size checks share null samples (each uses the other three), so they are not independent of each other.
- The pooled row has no held-out size check; all the nulls went into its cutoffs.
