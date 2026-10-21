# Capping one draw's AD term keeps power but does not restore the ncx2 ceiling under t(3)

**Answer to the cycle 83 direction.** No on the moment half, yes on the power
half. Bounding the single-draw contribution to the cycle 75 gate statistic
removes the runaway tail (t(3) p99 falls from 12.8 and 9444 to 0.36 and 0.51
at n=25, 50 under the 0.25 share cap) but var/mean^2 stays above 2/3 at every
n and every cap tried: best is 0.91 at n=25 and 1.36 at n=50 (share cap 0.25).
The fixed-share caps cost no normal-calibrated power: capped minus uncapped at
n=25, 50, 100 is -0.005, +0.002, +0.001 (share 0.50) and -0.017, -0.013, 0.000
(share 0.25), all inside the 0.02 tolerance. Winsorizing the largest |draw| is
not acceptable: it loses 0.17, 0.18, 0.10 of power.

Rule 2 shows why the ceiling is not restored. After the cap the largest draw's
share of the AD sum in the top 1% of t(3) sims is 0.49/0.47 (share 0.50) and
0.22/0.22 (share 0.25) against the uncapped 0.99/1.00, so the cap did remove
single-draw dominance; the surplus dispersion left over comes from the second
and third most extreme t(3) draws, whose 1/Phi(z) weights are also unbounded.
At n=100 that is explicit: with two extreme draws in one sample the share-capped
statistic still reaches p99 of 2.8 and var/mean^2 in the thousands.

## Inputs (rules 1 and 2)

- Statistic: cycle 71/75 lower-tail-weighted Anderson-Darling gate,
  `sum_i (F_n(i) - Phi(z_i))^2 / Phi(z_i)` on standardized data, scaled by
  `n^-1/2`; identical pure-python code to cycle 82's `tail-trim-check.py`.
- Script `stuff/cap-single-draw-check.py`, output `stuff/cap-single-draw-check.csv`,
  runs in about 2 s.
- Seed 83002 (per-stream 8300200 + n + {0 t(3), 1 normal}); 4000 sims per n per
  law; n = 25, 50, 100; t(3) drawn as gauss / sqrt(gamma(1.5, 2/3)) as in cycle 71.
- Cap rules as numbers: `winsor` replaces the largest |draw| by the second-largest
  |draw| before standardizing (winsorize quantile 1 - 1/n = 0.960, 0.980, 0.990);
  `share50` and `share25` cap any one AD term at 0.50 and 0.25 of the AD sum
  (the term is reduced until it equals exactly that share of the new sum).
- Power: critical value is the normal-data p95 of the same variant at the same n
  (per-n calibration, as in cycles 76 onward), power is the fraction of t(3)
  samples above it. The normal-data row therefore shows 0.050 by construction and
  the "normal-data power" of the direction is read as the t(3) power of the gate
  calibrated on normal data, which is the cycle 75 power curve (0.37, 0.59, 0.83
  uncapped here against 0.36, 0.60, 0.84 in cycle 75).


### t3 (rule 1)

| n | variant | cap rule | mean | variance | var/mean^2 | p90 | p95 | p99 | power |
|---|---|---|---|---|---|---|---|---|---|
| 25 | uncapped | none | 0.5419 | 11.05 | 37.62 | 0.3433 | 1.077 | 12.79 | 0.372 |
| 25 | winsor | winsor q=0.960 | 0.05547 | 0.003167 | 1.03 | 0.1096 | 0.15 | 0.2847 | 0.199 |
| 25 | share50 | share<=0.50 | 0.09064 | 0.01004 | 1.222 | 0.2081 | 0.2925 | 0.5271 | 0.368 |
| 25 | share25 | share<=0.25 | 0.07532 | 0.005187 | 0.9142 | 0.1608 | 0.2221 | 0.3636 | 0.355 |
| 50 | uncapped | none | 4394 | 1.457e+10 | 754.9 | 2.554 | 33.91 | 9444 | 0.585 |
| 50 | winsor | winsor q=0.980 | 0.1021 | 0.1473 | 14.13 | 0.1499 | 0.2493 | 1.007 | 0.406 |
| 50 | share50 | share<=0.50 | 0.1224 | 0.02722 | 1.816 | 0.2751 | 0.3952 | 0.723 | 0.587 |
| 50 | share25 | share<=0.25 | 0.09904 | 0.01333 | 1.359 | 0.2107 | 0.2918 | 0.506 | 0.572 |
| 100 | uncapped | none | 9.302e+04 | 2.105e+11 | 24.33 | 168.8 | 6.606e+04 | 2.500e+06 | 0.834 |
| 100 | winsor | winsor q=0.990 | 37.54 | 1.421e+06 | 1008 | 0.459 | 1.624 | 36.58 | 0.736 |
| 100 | share50 | share<=0.50 | 1.842 | 6055 | 1785 | 0.4409 | 0.6896 | 2.823 | 0.835 |
| 100 | share25 | share<=0.25 | 1.248 | 2691 | 1726 | 0.3221 | 0.4867 | 1.935 | 0.834 |

### normal (rule 1)

| n | variant | cap rule | mean | variance | var/mean^2 | p90 | p95 | p99 | power |
|---|---|---|---|---|---|---|---|---|---|
| 25 | uncapped | none | 0.03589 | 0.0005443 | 0.4226 | 0.06344 | 0.07826 | 0.1161 | 0.050 |
| 25 | winsor | winsor q=0.960 | 0.0363 | 0.0004622 | 0.3508 | 0.06391 | 0.07602 | 0.1121 | 0.050 |
| 25 | share50 | share<=0.50 | 0.03535 | 0.0004527 | 0.3622 | 0.06224 | 0.07627 | 0.1099 | 0.050 |
| 25 | share25 | share<=0.25 | 0.03344 | 0.000384 | 0.3435 | 0.05854 | 0.07206 | 0.1008 | 0.050 |
| 50 | uncapped | none | 0.02668 | 0.0005037 | 0.7076 | 0.04612 | 0.05751 | 0.0904 | 0.050 |
| 50 | winsor | winsor q=0.980 | 0.026 | 0.0002455 | 0.3631 | 0.04495 | 0.0553 | 0.07878 | 0.050 |
| 50 | share50 | share<=0.50 | 0.02601 | 0.0002627 | 0.3884 | 0.04551 | 0.05591 | 0.08336 | 0.050 |
| 50 | share25 | share<=0.25 | 0.0254 | 0.0002322 | 0.3598 | 0.0442 | 0.05438 | 0.07802 | 0.050 |
| 100 | uncapped | none | 0.01906 | 0.0001484 | 0.4085 | 0.03296 | 0.04029 | 0.061 | 0.050 |
| 100 | winsor | winsor q=0.990 | 0.01868 | 0.000108 | 0.3095 | 0.03201 | 0.03948 | 0.05523 | 0.050 |
| 100 | share50 | share<=0.50 | 0.01885 | 0.0001158 | 0.3257 | 0.03278 | 0.03995 | 0.05785 | 0.050 |
| 100 | share25 | share<=0.25 | 0.01863 | 0.0001089 | 0.314 | 0.03231 | 0.03885 | 0.05637 | 0.050 |

### Power difference, capped minus uncapped (rule 1)

| n | winsor | share50 | share25 |
|---|---|---|---|
| 25 | -0.174 | -0.005 | -0.017 |
| 50 | -0.179 | +0.002 | -0.013 |
| 100 | -0.098 | +0.001 | -0.000 |

### Rule 2: top-1% largest-draw share of the AD sum and cap-hit fraction, t(3)

| n | variant | post-cap top1% share | uncapped cycle 82 share | cap hit fraction |
|---|---|---|---|---|
| 25 | uncapped | 0.988 | 1.00 | 0.000 |
| 25 | winsor | 0.550 | 1.00 | 1.000 |
| 25 | share50 | 0.494 | 1.00 | 0.189 |
| 25 | share25 | 0.225 | 1.00 | 0.447 |
| 50 | uncapped | 1.000 | 1.00 | 0.000 |
| 50 | winsor | 0.849 | 1.00 | 1.000 |
| 50 | share50 | 0.474 | 1.00 | 0.235 |
| 50 | share25 | 0.215 | 1.00 | 0.374 |

## Reading

- Normal data: every cap lowers var/mean^2 (0.42 to 0.35 at n=25, 0.71 to 0.36
  at n=50) and leaves the p95 critical value within 3% of the uncapped one, so
  normal-data behaviour is unchanged for gating purposes.
- t(3): the share caps remove the single-draw tail (p99 drops by a factor of 35
  at n=25 and 19000 at n=50) and keep power, but var/mean^2 stays at 0.9 to 1.8
  at n=25, 50. The ncx2 ceiling is not reached because the remaining terms are
  still over-dispersed, matching cycle 82's drop1 and floorF rows (0.96, 1.40).
- Winsor loses power because the cycle 75 power *is* the one extreme draw: with
  it clipped the t(3) sample looks Gaussian more often than not at n=25, 50.
- The 0.25 share cap is the strongest cap that keeps power within 0.02; its
  cap-hit fraction is 0.45 (n=25) and 0.37 (n=50), so it binds on close to half
  the t(3) samples while binding on far fewer normal samples (see csv).

## Caveats

- Single seed per law; the uncapped t(3) moments at n=50, 100 are seed-driven
  by orders of magnitude, as in cycles 81 and 82. The capped rows, the power
  differences and the shares are the stable part.
- The share cap is applied to the AD terms after standardization, so the
  extreme draw still inflates sd and shifts every other z; a cap applied to the
  raw draws before standardization is a different intervention and is not
  tested here beyond winsor.
