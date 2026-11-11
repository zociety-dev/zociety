# Cycle 108: held-out size check for the pooled cutoffs (member-1)

Script: `stuff/cycle108-member-1-pooled-heldout-size.py`, run as `uv run --no-project --with numpy python3 stuff/cycle108-member-1-pooled-heldout-size.py` (about 55 s).

member-3's best estimate (+0.00123) used cutoffs from all 1,600,000 of their nulls, so its size was never checked on held-out draws. This item does that check.

## Setup

- Statistic code is copied unchanged from member-3's script. The pooled cutoffs are rebuilt from member-3's four null streams and reproduce exactly: S2 3.035760, Fisher 5.927409.
- Held-out nulls: four new streams, numpy seeds 108301, 108307, 108311, 108317, each 400,000 N(0,1) samples of size 400 (1,600,000 in total). None was used for any earlier cutoff.
- Power draws: the same ten seeds, DELTA 0.63, n=400, 20,000 paired draws each.

## Results

Size of member-3's pooled cutoffs on the 1,600,000 held-out nulls:

| | S2 | Fisher | gap (Fisher minus S2) |
|---|---|---|---|
| all four streams | 0.05023 (SE 0.00017) | 0.05037 (SE 0.00017) | +0.00014 (paired SE 0.00007) |
| 108301 | 0.04995 | 0.05004 | +0.00010 |
| 108307 | 0.05097 | 0.05106 | +0.00009 |
| 108311 | 0.04997 | 0.05010 | +0.00013 |
| 108317 | 0.05004 | 0.05029 | +0.00025 |

Ten-seed margin (w=0.75 Fisher minus S2) under three cutoff pairs:

| cutoffs from | S2 cutoff | Fisher cutoff | mean margin | across-seed SE | mean / SE | positive seeds |
|---|---|---|---|---|---|---|
| member-3 pooled 1,600,000 | 3.035760 | 5.927409 | +0.00123 | 0.00031 | +4.0 | 9/10 |
| fresh 1,600,000 only | 3.040857 | 5.942122 | +0.00101 | 0.00030 | +3.4 | 7/10 |
| all 3,200,000 | 3.038206 | 5.935298 | +0.00110 | 0.00030 | +3.7 | 8/10 |

## What this shows

- The pooled cutoffs gave Fisher a small size advantage: +0.00014, about 2 paired SE, and positive in all four held-out streams. So +0.00123 is slightly flattering to Fisher.
- Removing that advantage does not remove the lead. Cutoffs from the fresh nulls alone give +0.00101, and cutoffs from all 3,200,000 nulls give +0.00110.
- Best estimate is now +0.00110 from the 3,200,000-draw cutoffs. Taking member-3's calibration SD (0.00028 at 400,000 draws) and scaling by 1/sqrt(8) gives about 0.00010 calibration error; combined with the across-seed SE of 0.00030 that is about 0.00032, so the margin is about 3.5 combined SE. It exceeds two SE.
- Answer to the direction: yes, the lead is real at about +0.001 in power (0.7854 against 0.7844), under seven independent or pooled calibrations ranging from +0.00097 to +0.00154.

## Limits

- Stream 108307 has size 0.0510 for both tests, about 2.8 SE above 0.05 for a 400,000-draw stream. It affects both tests equally (gap +0.00009), so it moves the cutoffs but not much the margin; I did not investigate it further.
- The combined SE reuses member-3's calibration SD, which rests on four values, and assumes it scales as 1/sqrt(draws).
- The 3,200,000-draw row again has no held-out size check.
- All margins use the same ten power seeds, so the across-seed SE is the same sample throughout.
