# Cycle 85: trim-fraction sweep and inverted rank weights on the cycle 75 gate

Follow-up to `tail-trim-rankweight-sweep.md`, which found the m=ceil(0.1n) trimmed sum the cheapest variant so far but short of var/mean^2 at most 2/3, and found r^-p rank weighting moves the wrong way because rank 1 keeps weight 1. This item runs the two follow-ups suggested there:

- **Trim fraction sweep:** drop the top m=ceil(f n) AD terms by |draw| rank for f = 0.10, 0.15 and 0.20.
- **Inverted rank weights** that damp the extremes instead of the bulk: w = 1 - r^-1, w = 1 - r^-2, and a linear ramp w = min(1, (r-1)/ceil(0.2n)).

The rule 1 variants (trim f=0.10, r^-1, r^-2) and the k=0 baseline appear in the same table. Each variant is computed on the same draws.

**Seed 85002, 4000 sims per n per law** (normal and t(3)), at n = 25, 50 and 100. Script: `stuff/tail-trimfrac-invrank-sweep.py` (pure python, about 3 s). Raw rows: `stuff/tail-trimfrac-invrank-sweep.csv`. The seed and stream match the earlier item, so the k0/trim/rw1/rw2 rows reproduce its numbers exactly. Power is P(stat > normal-data p95 of the same variant at the same n) on t(3) data. Loss is measured against k=0 at each n. Within a variant, the power and loss columns are the same in the n=25 and n=50 rows.

### Rule 1 table: t(3), k=0 is the uncapped baseline

| n | variant | m dropped | mean | variance | var/mean^2 | p99 | top-1% AD share of top 3 draws | power n=25 | power n=50 | power n=100 | loss n=25 | loss n=50 | loss n=100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | k=0 uncapped | 0 | 0.5308 | 12.04 | 42.73 | 11.71 | 0.990 | 0.379 | 0.567 | 0.827 | +0.000 | +0.000 | +0.000 |
| 25 | trimmed sum (drop top m=ceil(0.1n)) | 3 | 0.06044 | 0.003154 | 0.8634 | 0.2931 | 0.000 | 0.311 | 0.537 | 0.808 | -0.067 | -0.030 | -0.019 |
| 25 | rank-weighted r^-1 | 0 | 0.4715 | 11.88 | 53.42 | 11.49 | 0.999 | 0.333 | 0.447 | 0.631 | -0.046 | -0.120 | -0.196 |
| 25 | rank-weighted r^-2 | 0 | 0.4641 | 11.85 | 55.04 | 11.46 | 1.000 | 0.294 | 0.382 | 0.520 | -0.084 | -0.185 | -0.307 |
| 25 | trimmed sum m=ceil(0.15n) | 4 | 0.05711 | 0.002695 | 0.8262 | 0.2658 | 0.000 | 0.314 | 0.546 | 0.808 | -0.065 | -0.021 | -0.020 |
| 25 | trimmed sum m=ceil(0.2n) | 5 | 0.05372 | 0.002286 | 0.7923 | 0.2392 | 0.000 | 0.310 | 0.543 | 0.799 | -0.069 | -0.023 | -0.028 |
| 25 | inverted 1-r^-1 | 0 | 0.05931 | 0.003141 | 0.8931 | 0.2824 | 0.120 | 0.315 | 0.532 | 0.805 | -0.064 | -0.034 | -0.023 |
| 25 | inverted 1-r^-2 | 0 | 0.06675 | 0.004244 | 0.9523 | 0.3207 | 0.152 | 0.317 | 0.537 | 0.805 | -0.062 | -0.029 | -0.022 |
| 25 | ramp min(1,(r-1)/ceil(0.2n)) | 5 | 0.06085 | 0.00315 | 0.8507 | 0.2876 | 0.055 | 0.315 | 0.545 | 0.805 | -0.064 | -0.022 | -0.022 |
| 50 | k=0 uncapped | 0 | 4216 | 9.545e+09 | 536.9 | 7025 | 1.000 | 0.379 | 0.567 | 0.827 | +0.000 | +0.000 | +0.000 |
| 50 | trimmed sum (drop top m=ceil(0.1n)) | 5 | 0.07285 | 0.005059 | 0.9532 | 0.3622 | 0.000 | 0.311 | 0.537 | 0.808 | -0.067 | -0.030 | -0.019 |
| 50 | rank-weighted r^-1 | 0 | 4216 | 9.545e+09 | 536.9 | 7025 | 1.000 | 0.333 | 0.447 | 0.631 | -0.046 | -0.120 | -0.196 |
| 50 | rank-weighted r^-2 | 0 | 4216 | 9.545e+09 | 536.9 | 7025 | 1.000 | 0.294 | 0.382 | 0.520 | -0.084 | -0.185 | -0.307 |
| 50 | trimmed sum m=ceil(0.15n) | 8 | 0.06702 | 0.00395 | 0.8794 | 0.3151 | 0.000 | 0.314 | 0.546 | 0.808 | -0.065 | -0.021 | -0.020 |
| 50 | trimmed sum m=ceil(0.2n) | 10 | 0.06248 | 0.003256 | 0.8343 | 0.2874 | 0.000 | 0.310 | 0.543 | 0.799 | -0.069 | -0.023 | -0.028 |
| 50 | inverted 1-r^-1 | 0 | 0.08009 | 0.008897 | 1.387 | 0.4429 | 0.404 | 0.315 | 0.532 | 0.805 | -0.064 | -0.034 | -0.023 |
| 50 | inverted 1-r^-2 | 0 | 0.08872 | 0.01376 | 1.748 | 0.4995 | 0.522 | 0.317 | 0.537 | 0.805 | -0.062 | -0.029 | -0.022 |
| 50 | ramp min(1,(r-1)/ceil(0.2n)) | 10 | 0.07299 | 0.00507 | 0.9516 | 0.3634 | 0.058 | 0.315 | 0.545 | 0.805 | -0.064 | -0.022 | -0.022 |

### Normal data, same variants (calibration rows; power is 0.05 by construction)

| n | variant | mean | variance | var/mean^2 | p95 (critical value) |
|---|---|---|---|---|---|
| 25 | k=0 uncapped | 0.03669 | 0.001037 | 0.7701 | 0.07827 |
| 25 | trimmed sum (drop top m=ceil(0.1n)) | 0.02979 | 0.0003222 | 0.3631 | 0.06393 |
| 25 | rank-weighted r^-1 | 0.007543 | 0.0005357 | 9.416 | 0.02006 |
| 25 | rank-weighted r^-2 | 0.00435 | 0.0005131 | 27.11 | 0.01451 |
| 25 | trimmed sum m=ceil(0.15n) | 0.02824 | 0.0002958 | 0.371 | 0.06062 |
| 25 | trimmed sum m=ceil(0.2n) | 0.0268 | 0.0002748 | 0.3826 | 0.05815 |
| 25 | inverted 1-r^-1 | 0.02915 | 0.0002967 | 0.3492 | 0.06189 |
| 25 | inverted 1-r^-2 | 0.03234 | 0.0003657 | 0.3496 | 0.06863 |
| 25 | ramp min(1,(r-1)/ceil(0.2n)) | 0.02992 | 0.0003149 | 0.3517 | 0.06388 |
| 50 | k=0 uncapped | 0.0271 | 0.0004562 | 0.6213 | 0.05919 |
| 50 | trimmed sum (drop top m=ceil(0.1n)) | 0.02204 | 0.0001638 | 0.3374 | 0.04672 |
| 50 | rank-weighted r^-1 | 0.004051 | 0.0002227 | 13.57 | 0.01085 |
| 50 | rank-weighted r^-2 | 0.002356 | 0.0002158 | 38.87 | 0.007561 |
| 50 | trimmed sum m=ceil(0.15n) | 0.02031 | 0.0001445 | 0.3502 | 0.04295 |
| 50 | trimmed sum m=ceil(0.2n) | 0.01927 | 0.0001352 | 0.364 | 0.04073 |
| 50 | inverted 1-r^-1 | 0.02305 | 0.000178 | 0.3351 | 0.0493 |
| 50 | inverted 1-r^-2 | 0.02474 | 0.0002078 | 0.3394 | 0.0525 |
| 50 | ramp min(1,(r-1)/ceil(0.2n)) | 0.02194 | 0.0001606 | 0.3338 | 0.04589 |
| 100 | k=0 uncapped | 0.01958 | 0.0002108 | 0.5497 | 0.04039 |
| 100 | trimmed sum (drop top m=ceil(0.1n)) | 0.01584 | 8.231e-05 | 0.3279 | 0.03281 |
| 100 | rank-weighted r^-1 | 0.002074 | 9.084e-05 | 21.11 | 0.005295 |
| 100 | rank-weighted r^-2 | 0.001229 | 8.807e-05 | 58.28 | 0.003463 |
| 100 | trimmed sum m=ceil(0.15n) | 0.01477 | 7.421e-05 | 0.34 | 0.03095 |
| 100 | trimmed sum m=ceil(0.2n) | 0.01382 | 6.695e-05 | 0.3505 | 0.02952 |
| 100 | inverted 1-r^-1 | 0.01751 | 9.569e-05 | 0.3121 | 0.03635 |
| 100 | inverted 1-r^-2 | 0.01836 | 0.0001063 | 0.3154 | 0.0381 |
| 100 | ramp min(1,(r-1)/ceil(0.2n)) | 0.01588 | 8.084e-05 | 0.3205 | 0.03305 |

### Rule 2 verdict and frontier

- trimmed sum (drop top m=ceil(0.1n)): var/mean^2 n=25 0.8634, n=50 0.9532 (bound missed); power loss n=25 -0.067, n=50 -0.030, n=100 -0.019 (within 0.02: no); meets both: no
- rank-weighted r^-1: var/mean^2 n=25 53.42, n=50 536.9 (bound missed); power loss n=25 -0.046, n=50 -0.120, n=100 -0.196 (within 0.02: no); meets both: no
- rank-weighted r^-2: var/mean^2 n=25 55.04, n=50 536.9 (bound missed); power loss n=25 -0.084, n=50 -0.185, n=100 -0.307 (within 0.02: no); meets both: no
- trimmed sum m=ceil(0.15n): var/mean^2 n=25 0.8262, n=50 0.8794 (bound missed); power loss n=25 -0.065, n=50 -0.021, n=100 -0.020 (within 0.02: no); meets both: no
- trimmed sum m=ceil(0.2n): var/mean^2 n=25 0.7923, n=50 0.8343 (bound missed); power loss n=25 -0.069, n=50 -0.023, n=100 -0.028 (within 0.02: no); meets both: no
- inverted 1-r^-1: var/mean^2 n=25 0.8931, n=50 1.387 (bound missed); power loss n=25 -0.064, n=50 -0.034, n=100 -0.023 (within 0.02: no); meets both: no
- inverted 1-r^-2: var/mean^2 n=25 0.9523, n=50 1.748 (bound missed); power loss n=25 -0.062, n=50 -0.029, n=100 -0.022 (within 0.02: no); meets both: no
- ramp min(1,(r-1)/ceil(0.2n)): var/mean^2 n=25 0.8507, n=50 0.9516 (bound missed); power loss n=25 -0.064, n=50 -0.022, n=100 -0.022 (within 0.02: no); meets both: no
- smallest power loss among variants reaching var/mean^2 <= 2/3 at both n: none

## Reading

- **Trimming more helps var/mean^2 only slowly, and never reaches 2/3.** Going from f=0.10 to 0.15 to 0.20 moves var/mean^2 from 0.863 to 0.826 to 0.792 at n=25, and from 0.953 to 0.879 to 0.834 at n=50. That is about 0.035 to 0.06 per 0.05 of trim fraction. A linear extrapolation reaches 2/3 at n=50 only near f of about 0.35.
- **Power has a floor at n=25 that trimming cannot remove.** Every damping variant (all trims, both inverted weights and the ramp) loses 0.062 to 0.069 at n=25. The loss does not depend on how much is removed, so the gate loses that power as soon as the top draws are touched at all. At n=50 and 100 the losses fall to 0.02-0.03; f=0.15 comes closest at -0.021 and -0.020, just outside 0.02.
- **The inverted weights fix the direction but not the size.** 1 - r^-1 and 1 - r^-2 take the top-1% top-3 share down from 0.99-1.00 (k0, r^-p) to 0.12-0.15 at n=25. At n=50, though, the share is 0.40-0.52 and var/mean^2 is 1.39-1.75. The partial weight on ranks 2-3 is still enough to dominate when n is larger. The ramp, which zeros rank 1 and phases ranks 2..ceil(0.2n) in linearly, behaves like a soft f=0.10 trim (0.851 / 0.952) at f=0.15 power cost.
- **Frontier (var/mean^2 n=25 / n=50 ; worst power loss over n=25, 50, 100):** trim f=0.20 0.792/0.834 ; 0.069. trim f=0.15 0.826/0.879 ; 0.065. ramp 0.851/0.952 ; 0.064. trim f=0.10 0.863/0.953 ; 0.067. 1-r^-1 0.893/1.387 ; 0.064. 1-r^-2 0.952/1.748 ; 0.062. r^-1 53.4/537 ; 0.196. r^-2 55.0/537 ; 0.307.
- **Rule 2 answer:** no variant meets both halves. No variant reaches var/mean^2 at most 2/3 at both n, so the variant with the smallest power loss among those reaching the bound is **none**. On the frontier, trim f=0.20 has the lowest var/mean^2 at both n. Trim f=0.15 has the best power at n=50 and 100 among trims.
- **Implication:** the power cost at n=25 comes from removing any of the tail, and var/mean^2 falls only slowly with the trim fraction. Under t(3), any whole-tail reweighting of this AD gate trades about 0.065 of n=25 power for a var/mean^2 that stays above 0.79. Reaching 2/3 likely needs a change in how terms are computed, for example a bounded per-term transform such as log(1+term), rather than in which terms are kept.
