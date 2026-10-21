# Cycle 85: concave term transforms on the cycle 75 gate (log(1+ct)/c, sqrt)

Third item of the cycle. The two earlier items (`tail-trim-rankweight-sweep.md`, `tail-trimfrac-invrank-sweep.md`) changed **which** AD terms are kept and stalled at var/mean^2 0.79-0.95: once the top m terms by |draw| rank are dropped, the next term inherits the dominance, and r^-p rank weights move the wrong way. This item leaves every term in and changes **how each term is computed**, passing t_i = (F_n(i) - Phi(z_i))^2 / Phi(z_i) through a concave map h before summation: n^-1/2 * sum_i w_i h(t_i).

- `log(1+ct)/c` for c = 1, 10, 30, 50, 100 (the /c keeps h(t) ~ t for the bulk, where ct is small, so the normal-data calibration barely moves; only the few huge terms are compressed).
- `sqrt(t)`.
- `log(1+t)` combined with the m=ceil(0.1n) trim.
- The rule 1 variants (trimmed sum m=ceil(0.1n), rank-weighted r^-1, r^-2) and the k=0 uncapped baseline, in the same table, on the same draws.

**Seed 85002, 4000 sims per n per law** (normal and t(3)), n = 25, 50, 100. Script: `stuff/tail-logterm-transform-sweep.py` (pure python, about 4 s). Raw rows: `stuff/tail-logterm-transform-sweep.csv`. Seed and stream match the earlier two items, so the k0/trim/rw1/rw2 rows reproduce their numbers exactly. Power is P(stat > normal-data p95 of the same variant at the same n) on t(3) data; loss is against k=0 at each n. Within a variant the power and loss columns repeat across the n=25 and n=50 rows. "Top-1% AD share of top 3 draws" is the share of the transformed, weighted statistic carried by the 3 largest |draws|, averaged over the top 1% of t(3) sims by statistic value.

## Answer to the direction

**Yes, one variant meets both halves: `log(1+30t)/30`.** var/mean^2 is 0.497 at n=25 and 0.572 at n=50 (bound 2/3), and normal-calibrated t(3) power is within 0.02 of the uncapped gate at every n (-0.012 at n=25, +0.019 at n=50, -0.002 at n=100). Its top-3-draw share in the top 1% of sims falls from 0.99-1.00 (k=0) to 0.27-0.31, so the ordered tail still carries most of the statistic, but no longer all of it.

Why this works where trimming did not: the tail excess is a single term of order F^-1 from the most negative standardized draw, and whichever term is largest after a trim inherits it. A concave map caps the contribution of any one term at roughly log(c t_max)/c without zeroing the small terms that carry the t(3) signal, so power is untouched while the variance collapses. The scale c trades the two halves against each other:

| c | var/mean^2 n=25 | var/mean^2 n=50 | worst power loss (n) | meets both |
|---|---|---|---|---|
| 1 | 2.52 | 3.25 | 0.004 (25) | no, var/mean^2 |
| 10 | 0.77 | 0.91 | 0.007 (25) | no, var/mean^2 |
| **30** | **0.50** | **0.57** | **0.012 (25)** | **yes** |
| 50 | 0.41 | 0.47 | 0.021 (25) | no, power by 0.001 |
| 100 | 0.31 | 0.35 | 0.027 (25) | no, power |

The power loss at n=25 grows monotonically with c while var/mean^2 falls; c in roughly 20-45 is the window where both hold on this seed. `sqrt(t)` is too weak a compression (var/mean^2 78 at n=50, one sim with a F~1e-12 term still dominates). Trimming on top of the log transform brings back the trim's 0.03-0.07 power loss and gains nothing on var/mean^2, so the two fixes do not stack.

**Caveat:** the +0.019 power at n=50 for c=30 and the -0.021 at n=25 for c=50 are each within one Monte Carlo standard error (about 0.008 at 4000 sims) of the 0.02 line, so the exact edge of the c window is seed-dependent; the qualitative ordering (c=10 fails on variance, c=100 fails on power, c~30 passes) is not. A re-run at 20000 sims with c in 20, 25, 30, 35, 40 would pin the window.

### Rule 1 table: t(3), k=0 is the uncapped baseline

| n | variant | m dropped | mean | variance | var/mean^2 | p99 | top-1% AD share of top 3 draws | power n=25 | power n=50 | power n=100 | loss n=25 | loss n=50 | loss n=100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | k=0 uncapped | 0 | 0.5308 | 12.04 | 42.73 | 11.71 | 0.990 | 0.379 | 0.567 | 0.827 | +0.000 | +0.000 | +0.000 |
| 25 | trimmed sum (drop top m=ceil(0.1n)) | 3 | 0.06044 | 0.003154 | 0.8634 | 0.2931 | 0.000 | 0.311 | 0.537 | 0.808 | -0.067 | -0.030 | -0.019 |
| 25 | rank-weighted r^-1 | 0 | 0.4715 | 11.88 | 53.42 | 11.49 | 0.999 | 0.333 | 0.447 | 0.631 | -0.046 | -0.120 | -0.196 |
| 25 | rank-weighted r^-2 | 0 | 0.4641 | 11.85 | 55.04 | 11.46 | 1.000 | 0.294 | 0.382 | 0.520 | -0.084 | -0.185 | -0.307 |
| 25 | log(1+t) terms | 0 | 0.117 | 0.03456 | 2.522 | 1.036 | 0.804 | 0.374 | 0.569 | 0.828 | -0.004 | +0.002 | +0.000 |
| 25 | log(1+10t)/10 terms | 0 | 0.06871 | 0.00364 | 0.7711 | 0.2937 | 0.448 | 0.371 | 0.581 | 0.824 | -0.007 | +0.014 | -0.003 |
| 25 | log(1+30t)/30 terms | 0 | 0.05049 | 0.001268 | 0.4974 | 0.1743 | 0.311 | 0.366 | 0.586 | 0.825 | -0.012 | +0.019 | -0.002 |
| 25 | log(1+50t)/50 terms | 0 | 0.04237 | 0.0007296 | 0.4065 | 0.1329 | 0.270 | 0.358 | 0.582 | 0.825 | -0.021 | +0.015 | -0.002 |
| 25 | log(1+100t)/100 terms | 0 | 0.0321 | 0.0003175 | 0.308 | 0.08895 | 0.236 | 0.352 | 0.587 | 0.827 | -0.027 | +0.020 | -0.001 |
| 25 | sqrt(t) terms | 0 | 0.5214 | 0.1722 | 0.6332 | 2.443 | 0.724 | 0.364 | 0.598 | 0.840 | -0.015 | +0.031 | +0.013 |
| 25 | log(1+t) terms, drop top m=ceil(0.1n) | 3 | 0.05893 | 0.002835 | 0.8163 | 0.2772 | 0.000 | 0.312 | 0.538 | 0.808 | -0.066 | -0.029 | -0.019 |
| 50 | k=0 uncapped | 0 | 4216 | 9.545e+09 | 536.9 | 7025 | 1.000 | 0.379 | 0.567 | 0.827 | +0.000 | +0.000 | +0.000 |
| 50 | trimmed sum (drop top m=ceil(0.1n)) | 5 | 0.07285 | 0.005059 | 0.9532 | 0.3622 | 0.000 | 0.311 | 0.537 | 0.808 | -0.067 | -0.030 | -0.019 |
| 50 | rank-weighted r^-1 | 0 | 4216 | 9.545e+09 | 536.9 | 7025 | 1.000 | 0.333 | 0.447 | 0.631 | -0.046 | -0.120 | -0.196 |
| 50 | rank-weighted r^-2 | 0 | 4216 | 9.545e+09 | 536.9 | 7025 | 1.000 | 0.294 | 0.382 | 0.520 | -0.084 | -0.185 | -0.307 |
| 50 | log(1+t) terms | 0 | 0.1971 | 0.1261 | 3.246 | 1.789 | 0.846 | 0.374 | 0.569 | 0.828 | -0.004 | +0.002 | +0.000 |
| 50 | log(1+10t)/10 terms | 0 | 0.0887 | 0.007122 | 0.9051 | 0.4158 | 0.426 | 0.371 | 0.581 | 0.824 | -0.007 | +0.014 | -0.003 |
| 50 | log(1+30t)/30 terms | 0 | 0.06402 | 0.002344 | 0.5719 | 0.2356 | 0.273 | 0.366 | 0.586 | 0.825 | -0.012 | +0.019 | -0.002 |
| 50 | log(1+50t)/50 terms | 0 | 0.05387 | 0.001355 | 0.4669 | 0.18 | 0.224 | 0.358 | 0.582 | 0.825 | -0.021 | +0.015 | -0.002 |
| 50 | log(1+100t)/100 terms | 0 | 0.0412 | 0.000602 | 0.3546 | 0.1197 | 0.182 | 0.352 | 0.587 | 0.827 | -0.027 | +0.020 | -0.001 |
| 50 | sqrt(t) terms | 0 | 2.755 | 595.6 | 78.49 | 32.57 | 0.986 | 0.364 | 0.598 | 0.840 | -0.015 | +0.031 | +0.013 |
| 50 | log(1+t) terms, drop top m=ceil(0.1n) | 5 | 0.0713 | 0.004593 | 0.9033 | 0.3457 | 0.000 | 0.312 | 0.538 | 0.808 | -0.066 | -0.029 | -0.019 |

### Normal data, same variants (calibration rows; power is 0.05 by construction)

| n | variant | mean | variance | var/mean^2 | p95 (critical value) |
|---|---|---|---|---|---|
| 25 | k=0 uncapped | 0.03669 | 0.001037 | 0.7701 | 0.07827 |
| 25 | trimmed sum (drop top m=ceil(0.1n)) | 0.02979 | 0.0003222 | 0.3631 | 0.06393 |
| 25 | rank-weighted r^-1 | 0.007543 | 0.0005357 | 9.416 | 0.02006 |
| 25 | rank-weighted r^-2 | 0.00435 | 0.0005131 | 27.11 | 0.01451 |
| 25 | log(1+t) terms | 0.03565 | 0.0005949 | 0.4681 | 0.07665 |
| 25 | log(1+10t)/10 terms | 0.03152 | 0.0002945 | 0.2965 | 0.06458 |
| 25 | log(1+30t)/30 terms | 0.02679 | 0.0001626 | 0.2266 | 0.05116 |
| 25 | log(1+50t)/50 terms | 0.0239 | 0.0001117 | 0.1954 | 0.04418 |
| 25 | log(1+100t)/100 terms | 0.01956 | 5.981e-05 | 0.1563 | 0.03432 |
| 25 | sqrt(t) terms | 0.3149 | 0.008752 | 0.08825 | 0.4913 |
| 25 | log(1+t) terms, drop top m=ceil(0.1n) | 0.02942 | 0.0003063 | 0.354 | 0.06284 |
| 50 | k=0 uncapped | 0.0271 | 0.0004562 | 0.6213 | 0.05919 |
| 50 | trimmed sum (drop top m=ceil(0.1n)) | 0.02204 | 0.0001638 | 0.3374 | 0.04672 |
| 50 | rank-weighted r^-1 | 0.004051 | 0.0002227 | 13.57 | 0.01085 |
| 50 | rank-weighted r^-2 | 0.002356 | 0.0002158 | 38.87 | 0.007561 |
| 50 | log(1+t) terms | 0.02655 | 0.0002901 | 0.4117 | 0.05795 |
| 50 | log(1+10t)/10 terms | 0.02447 | 0.0001775 | 0.2964 | 0.05069 |
| 50 | log(1+30t)/30 terms | 0.02189 | 0.0001162 | 0.2425 | 0.04276 |
| 50 | log(1+50t)/50 terms | 0.02016 | 8.744e-05 | 0.2152 | 0.03817 |
| 50 | log(1+100t)/100 terms | 0.01732 | 5.329e-05 | 0.1777 | 0.03089 |
| 50 | sqrt(t) terms | 0.3197 | 0.008172 | 0.07996 | 0.4878 |
| 50 | log(1+t) terms, drop top m=ceil(0.1n) | 0.02189 | 0.0001594 | 0.3327 | 0.04609 |
| 100 | k=0 uncapped | 0.01958 | 0.0002108 | 0.5497 | 0.04039 |
| 100 | trimmed sum (drop top m=ceil(0.1n)) | 0.01584 | 8.231e-05 | 0.3279 | 0.03281 |
| 100 | rank-weighted r^-1 | 0.002074 | 9.084e-05 | 21.11 | 0.005295 |
| 100 | rank-weighted r^-2 | 0.001229 | 8.807e-05 | 58.28 | 0.003463 |
| 100 | log(1+t) terms | 0.01929 | 0.0001442 | 0.3875 | 0.04006 |
| 100 | log(1+10t)/10 terms | 0.01832 | 9.78e-05 | 0.2915 | 0.0375 |
| 100 | log(1+30t)/30 terms | 0.01706 | 7.349e-05 | 0.2525 | 0.03377 |
| 100 | log(1+50t)/50 terms | 0.01615 | 6.03e-05 | 0.2313 | 0.031 |
| 100 | log(1+100t)/100 terms | 0.01451 | 4.195e-05 | 0.1993 | 0.0267 |
| 100 | sqrt(t) terms | 0.3238 | 0.00778 | 0.07419 | 0.484 |
| 100 | log(1+t) terms, drop top m=ceil(0.1n) | 0.01579 | 8.115e-05 | 0.3255 | 0.03266 |

### Rule 2 verdict and frontier

- trimmed sum (drop top m=ceil(0.1n)): var/mean^2 n=25 0.8634, n=50 0.9532 (bound missed); power loss n=25 -0.067, n=50 -0.030, n=100 -0.019 (within 0.02: no); meets both: no
- rank-weighted r^-1: var/mean^2 n=25 53.42, n=50 536.9 (bound missed); power loss n=25 -0.046, n=50 -0.120, n=100 -0.196 (within 0.02: no); meets both: no
- rank-weighted r^-2: var/mean^2 n=25 55.04, n=50 536.9 (bound missed); power loss n=25 -0.084, n=50 -0.185, n=100 -0.307 (within 0.02: no); meets both: no
- log(1+t) terms: var/mean^2 n=25 2.522, n=50 3.246 (bound missed); power loss n=25 -0.004, n=50 +0.002, n=100 +0.000 (within 0.02: yes); meets both: no
- log(1+10t)/10 terms: var/mean^2 n=25 0.7711, n=50 0.9051 (bound missed); power loss n=25 -0.007, n=50 +0.014, n=100 -0.003 (within 0.02: yes); meets both: no
- log(1+30t)/30 terms: var/mean^2 n=25 0.4974, n=50 0.5719 (bound met); power loss n=25 -0.012, n=50 +0.019, n=100 -0.002 (within 0.02: yes); meets both: YES
- log(1+50t)/50 terms: var/mean^2 n=25 0.4065, n=50 0.4669 (bound met); power loss n=25 -0.021, n=50 +0.015, n=100 -0.002 (within 0.02: no); meets both: no
- log(1+100t)/100 terms: var/mean^2 n=25 0.308, n=50 0.3546 (bound met); power loss n=25 -0.027, n=50 +0.020, n=100 -0.001 (within 0.02: no); meets both: no
- sqrt(t) terms: var/mean^2 n=25 0.6332, n=50 78.49 (bound missed); power loss n=25 -0.015, n=50 +0.031, n=100 +0.013 (within 0.02: no); meets both: no
- log(1+t) terms, drop top m=ceil(0.1n): var/mean^2 n=25 0.8163, n=50 0.9033 (bound missed); power loss n=25 -0.066, n=50 -0.029, n=100 -0.019 (within 0.02: no); meets both: no
- smallest power loss among variants reaching var/mean^2 <= 2/3 at both n: log(1+30t)/30 terms (worst loss 0.012)
