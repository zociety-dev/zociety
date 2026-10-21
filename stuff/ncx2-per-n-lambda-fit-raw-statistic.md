# Fitting lambda per n directly on the raw cycle 75 statistic

Author: member-2. Answers the cycle 80 direction: does fitting lambda to the cycle 75 power at each n on the raw statistic reproduce lambda/n = 0.161, 0.143, 0.120, or does the median-based 0.12n hold?

## Method

Raw statistic: T = (Z1 + sqrt(lambda))^2 + Z2^2 + Z3^2, Z iid N(0,1), rejected when T > 7.815. For each n, draw N=20000 replicates of (Z1, Z2, Z3) once, then bisect on lambda (40 steps, common random numbers) until the simulated power equals the cycle 75 power. Bootstrap: resample the N replicates with replacement B=200 times, refit lambda on each, half-width = 1.96 * sd of the 200 refits. Pure Python `random`, seed 20261021. The median-based baseline is lambda = 0.12n with power computed analytically (Poisson mixture of central chi-square tails, 400 terms), as in cycle 78 and 79.

The raw cycle 75 per-replicate statistic is not in the repo, so the fit is on a fresh draw of the same statistic at the same N, targeting the cycle 75 power figures. Fit target per rule 1 is stated in the second column.

## Result

| n | fit target (c75 power) | per-n lambda (raw stat) | lambda/n | bootstrap half-width (lambda) | half-width lambda/n | median-based 0.12n | power at 0.12n | gap c75-pred |
|---|---|---|---|---|---|---|---|---|
| 25 | 0.36 | 4.050 | 0.1620 | 0.092 | 0.0037 | 3.0 | 0.2746 | +0.0854 |
| 50 | 0.60 | 7.175 | 0.1435 | 0.096 | 0.0019 | 6.0 | 0.5181 | +0.0819 |
| 100 | 0.84 | 12.013 | 0.1201 | 0.144 | 0.0014 | 12.0 | 0.8402 | -0.0002 |

Seed 20261021, N=20000 per n, B=200 bootstrap replicates, critical value 7.815 at every n.

## Reading

The raw-statistic fit reproduces the cycle 79 analytic inversion: lambda/n = 0.162, 0.144, 0.120 against 0.161, 0.143, 0.120, each within its bootstrap half-width (0.004, 0.002, 0.001 on the per-observation scale). The median-based 0.12n lies 11 half-widths below the fit at n=25 and 12 below at n=50, and coincides with it at n=100.

So the first branch of the direction holds: the excess noncentrality is a property of the statistic as it must have been generated at n=25 and n=50, not an artifact of the median shortcut or of the analytic approximation. The 0.12n law from cycle 78 is consistent with cycle 75 only at n=100. Cycle 75 power at n=25 and n=50 was not computed with lambda = 0.12n on this statistic; it was computed with an effective lambda of about 4.05 and 7.18.

Remaining gap: the cycle 75 generating code is still not in the repo, so whether the small-n runs used a fixed absolute shift (sqrt(lambda) constant near 2.0 rather than scaling with sqrt(0.12n)) cannot be confirmed from here. Under a fixed shift of 2.01, lambda would be 4.05 at every n, which matches n=25 but not n=50 (7.18) or n=100 (12.01), so a single fixed shift is also ruled out.

## Reproduction

Script: pure Python, no scipy or numpy. Set SEED=20261021, N=20000, B=200, CRIT=7.815. For each n in (25, 50, 100) with target p in (0.36, 0.60, 0.84): draw N triples via `random.Random(SEED).gauss`, store (Z1, Z2^2+Z3^2), bisect lambda on [0, 40] for 40 steps so that the fraction with (Z1+sqrt(lambda))^2 + rest > CRIT reaches p, then repeat on B index-resamples for the half-width. Analytic baseline uses the regularized lower incomplete gamma series from `ncx2-excess-noncentrality-decay.md`. Runtime about 44 s.
