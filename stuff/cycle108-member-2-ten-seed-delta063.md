# Cycle 108: ten-seed DELTA 0.63 margin, w=0.75 Fisher minus S2, n=400 (member-2)

Script: `stuff/cycle108-member-2-ten-seed-delta063.py`, run as `uv run --no-project --with numpy python3 stuff/cycle108-member-2-ten-seed-delta063.py` (about 18 s). The statistics are the numpy forms from cycle 107's pooled-calibration script, unchanged.

## Critical values at n=400, exact-size 5% (before any table)

- Null seed: numpy `default_rng(108999)`, disjoint from the ten power seeds.
- Null calibration sample: 400,000 N(0,1) samples of size 400; cutoffs are its 95th percentiles.
- Plain S2 rejects when its statistic exceeds 3.033908 (p < 0.04813).
- w=0.75 Fisher rejects when its statistic exceeds 5.926776.
- Size on a further 400,000 nulls from the same stream: S2 0.0502, Fisher 0.0503 (binomial SE 0.00034 each). The size gap is +0.0001 in Fisher's favour.

## Seeds

Ten new numpy seeds, not used in cycles 100 to 107: 108011, 108023, 108037, 108041, 108053, 108067, 108079, 108083, 108097, 108103. Each gives 20,000 samples of size 400 from skew-normal (DELTA 0.63) divided by sqrt(chi-square(10)/10); both tests see the same samples.

## Per-seed results

| seed | measured sqrt(beta1) | S2 power | Fisher power | margin (Fisher minus S2) | paired SE | margin / SE |
|---|---|---|---|---|---|---|
| 108011 | 0.330 | 0.7813 | 0.7832 | +0.0019 | 0.0009 | +2.0 |
| 108023 | 0.326 | 0.7843 | 0.7847 | +0.0003 | 0.0009 | +0.4 |
| 108037 | 0.328 | 0.7809 | 0.7826 | +0.0017 | 0.0009 | +1.9 |
| 108041 | 0.331 | 0.7843 | 0.7839 | -0.0004 | 0.0009 | -0.5 |
| 108053 | 0.326 | 0.7827 | 0.7830 | +0.0002 | 0.0009 | +0.2 |
| 108067 | 0.331 | 0.7881 | 0.7900 | +0.0019 | 0.0009 | +2.1 |
| 108079 | 0.330 | 0.7908 | 0.7907 | -0.0001 | 0.0009 | -0.1 |
| 108083 | 0.329 | 0.7831 | 0.7856 | +0.0026 | 0.0009 | +2.9 |
| 108097 | 0.329 | 0.7839 | 0.7856 | +0.0017 | 0.0009 | +1.8 |
| 108103 | 0.329 | 0.7882 | 0.7893 | +0.0011 | 0.0009 | +1.3 |

sqrt(beta1) is the sample skewness of all 8,000,000 values in a seed's draws.

## Mean

- Mean of the ten margins: +0.00109.
- Across-seed SD 0.00099, across-seed SE 0.00031.
- Does the mean exceed two across-seed SE? **Yes**: it is 3.5 across-seed SE.
- Positive margins: 8 of 10.

## What this shows

- The w=0.75 Fisher lead over S2 at DELTA 0.63 is real but small: about 0.11 percentage points of power at about 78% power.
- The across-seed SD (0.00099) is about the paired SE of one seed (0.0009). With cutoffs fixed from one large null sample, seeds add no spread beyond ordinary draw noise. This fits cycle 107's finding that the earlier seed-to-seed swings were partly per-seed calibration error.

## Limit

All ten seeds share one cutoff pair, so calibration error is common to them and is not in the across-seed SE. The check sample puts Fisher's size 0.0001 above S2's, with an SE of that order. A size gap is not a power gap, so this item does not say how much of the +0.0011 it could account for. A second independent null sample would settle it.
