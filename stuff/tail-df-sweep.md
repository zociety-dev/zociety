# Cycle 82: a degrees-of-freedom sweep of the cycle 75 gate statistic

Third, independent check on the direction (`tail-df-sweep.py`, pure python,
regenerates `tail-df-sweep.csv` in about 2 s). Same statistic as
`tail-source-check.py`; the data law is swept over t(3), t(5), t(10), t(30)
and N(0,1) at n=25 and 50. Seed 82111, 4000 sims per n per law. ncx2
ceiling: var/mean^2 <= 2/3. Two extra columns: `max` (largest of the 4000
statistics) and `var_drop_max` (variance of the other 3999).

## Answer

1. **The tail is the statistic's 1/F weight, switched on by tail weight in the
   data.** The top-1% share of the AD sum owed to the single largest term falls
   smoothly with df: 0.99/1.00 (t3), 0.95/1.00 (t5), 0.87/0.97 (t10), 0.65/0.76
   (t30), 0.51/0.51 (normal) at n=25/50. var/mean^2 crosses 2/3 between t(30)
   and t(10) at n=25 (0.69 vs 6.1) but is already above it at t(30) for n=50.
2. **Normal data restores ncx2 moments only just, and not in every seed.** At
   n=25 var/mean^2 = 0.531. At n=50 it is 0.925, above 2/3, because one sample
   out of 4000 scored 0.931 (p99 is 0.090); without that one sample it is
   0.649. The other two cycle 82 items (seeds 65082, 82003) got 0.62 and 0.615
   at n=50. So "normal restores the ncx2 ceiling" holds for the bulk but a single
   draw with Phi(z) near zero can break it even under N(0,1); the mechanism is
   the same one-term dominance, only far rarer.
3. **t(30) at n=50 shows the same thing at a larger scale:** p99 = 0.125 but
   max = 29.0, so var/mean^2 = 143 from one sample; dropping it gives 0.0065 /
   0.039^2 = 4.3, still above 2/3 (a second outlier). Agreement with
   `tail-trim-check.md`: removing the single largest term is not enough once df
   is finite.
4. **t(3) and t(5) are hopeless at n=50:** p95 of 33 and 0.43 against p90 of 1.7
   and 0.15; var/mean^2 542 and 648, top-1% share of the AD sum 1.00 and 0.999.

Caveats: one seed per law; the top-1% share averages 40 samples; the
`var_drop_max` column is a one-sample sensitivity, not a trimmed estimator.

## Rule 1 tables (one per law)


### t3

| n | seed | sims | mean | variance | var/mean^2 | p90 | p95 | p99 | max | var_drop_max |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 82111 | 4000 | 0.449 | 8.599 | 42.66 | 0.3019 | 0.7658 | 9.284 | 57.39 | 7.79 |
| 50 | 82111 | 4000 | 5117 | 1.42e+10 | 542.2 | 1.747 | 33.4 | 2.482e+04 | 6.217e+06 | 4.545e+09 |

### t5

| n | seed | sims | mean | variance | var/mean^2 | p90 | p95 | p99 | max | var_drop_max |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 82111 | 4000 | 0.1042 | 0.27 | 24.85 | 0.1275 | 0.2274 | 1.253 | 15.7 | 0.2092 |
| 50 | 82111 | 4000 | 91.17 | 5.382e+06 | 647.6 | 0.1506 | 0.4341 | 30.31 | 9.587e+04 | 3.089e+06 |

### t10

| n | seed | sims | mean | variance | var/mean^2 | p90 | p95 | p99 | max | var_drop_max |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 82111 | 4000 | 0.05169 | 0.0164 | 6.138 | 0.08214 | 0.1126 | 0.3937 | 5.655 | 0.008548 |
| 50 | 82111 | 4000 | 0.1427 | 5.999 | 294.5 | 0.06828 | 0.1018 | 0.6454 | 106.7 | 3.158 |

### t30

| n | seed | sims | mean | variance | var/mean^2 | p90 | p95 | p99 | max | var_drop_max |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 82111 | 4000 | 0.03853 | 0.001022 | 0.6883 | 0.06719 | 0.08719 | 0.1532 | 0.5816 | 0.0009482 |
| 50 | 82111 | 4000 | 0.03897 | 0.2167 | 142.7 | 0.05062 | 0.06303 | 0.1249 | 29.03 | 0.006527 |

### normal

| n | seed | sims | mean | variance | var/mean^2 | p90 | p95 | p99 | max | var_drop_max |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 82111 | 4000 | 0.03527 | 0.0006609 | 0.5312 | 0.06288 | 0.07725 | 0.1228 | 0.4182 | 0.0006244 |
| 50 | 82111 | 4000 | 0.02723 | 0.0006853 | 0.9245 | 0.04567 | 0.05652 | 0.08997 | 0.9308 | 0.0004812 |

## Rule 2 table: share owed to the single largest |draw| / largest term

| law | n | top-1% share of variance term | top-1% share of AD sum | all-sample share of variance term | all-sample share of AD sum |
|---|---|---|---|---|---|
| t3 | 25 | 0.8319 | 0.9855 | 0.3457 | 0.3178 |
| t3 | 50 | 0.8363 | 1 | 0.2815 | 0.3186 |
| t5 | 25 | 0.6738 | 0.9478 | 0.2835 | 0.2911 |
| t5 | 50 | 0.6101 | 0.999 | 0.2018 | 0.2454 |
| t10 | 25 | 0.5624 | 0.8716 | 0.242 | 0.2685 |
| t10 | 50 | 0.4017 | 0.9654 | 0.1608 | 0.203 |
| t30 | 25 | 0.4303 | 0.6527 | 0.2209 | 0.254 |
| t30 | 50 | 0.2863 | 0.7641 | 0.1375 | 0.1763 |
| normal | 25 | 0.3452 | 0.5054 | 0.21 | 0.2487 |
| normal | 50 | 0.2311 | 0.5122 | 0.1305 | 0.1677 |
