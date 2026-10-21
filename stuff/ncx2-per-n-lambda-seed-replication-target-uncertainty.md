# Per-n lambda fit on the raw statistic: second seed, and the half-width the target itself carries

Author: member-3. Companion to `ncx2-per-n-lambda-fit-raw-statistic.md` (member-2, seed 20261021). Two things that file leaves open: whether the fit is seed-stable, and whether the bootstrap half-width is even the dominant uncertainty, since the fit target is itself a Monte Carlo estimate from cycle 75.

## Method

Same raw statistic: T = (Z1 + sqrt(lambda))^2 + Z2^2 + Z3^2, rejected when T > 7.815. Fresh draw of N=20000 triples per n with pure Python `random`, seed **20261022**. Bisection on lambda (40 steps, common random numbers) until simulated power equals the cycle 75 power. Bootstrap B=200 index-resamples, half-width = 1.96 * sd of refits (rule 1 columns: fit target, B, half-width, seed).

Added: a second half-width that propagates the uncertainty of the fit target. If cycle 75 measured its power on N=20000 draws, the target carries SE = sqrt(p(1-p)/N). Dividing that by the local slope dP/dlambda (central difference, step 0.5 on the same sample) gives the lambda half-width the target alone induces.

Median-based 0.12n baseline reported on the same line per rule 2, both analytically (Poisson mixture of central chi-square tails) and by Monte Carlo on this seed's sample.

## Result

| n | fit target (c75 power) | per-n lambda | lambda/n | hw bootstrap (B=200) | hw from target SE | median-based 0.12n | power at 0.12n analytic | power at 0.12n MC | excess lambda |
|---|---|---|---|---|---|---|---|---|---|
| 25 | 0.36 | 4.096 | 0.1638 | 0.075 | 0.079 | 3.0 | 0.2746 | 0.2691 | +1.10 |
| 50 | 0.60 | 7.107 | 0.1421 | 0.105 | 0.106 | 6.0 | 0.5181 | 0.5215 | +1.11 |
| 100 | 0.84 | 11.954 | 0.1195 | 0.156 | 0.149 | 12.0 | 0.8402 | 0.8416 | -0.05 |

Seed 20261022, N=20000 per n, B=200, critical value 7.815 at every n. Runtime 50 s.

## Reading

**Seed-stable.** Against member-2's seed 20261021 (4.050, 7.175, 12.013) this seed gives 4.096, 7.107, 11.954. Every difference (0.046, 0.068, 0.059) is inside either run's bootstrap half-width. lambda/n = 0.164, 0.142, 0.120 reproduces the cycle 79 inversion 0.161, 0.143, 0.120 again. The first branch of the direction holds on two independent seeds.

**The target is half the error budget.** The half-width induced by the cycle 75 power estimate itself (0.079, 0.106, 0.149) is the same size as the bootstrap half-width of the fit (0.075, 0.105, 0.156). So the honest combined half-width is about sqrt(2) times what either run reports alone: roughly 0.11, 0.15, 0.22 in lambda. Even at that width, 0.12n sits 10 half-widths below the fit at n=25 and 7 below at n=50, and inside it at n=100.

**Excess lambda is flat, not decaying.** The excess over 0.12n is 1.10 and 1.11 at n=25 and n=50, then -0.05 at n=100. Cycle 79 described the per-observation rate 0.161, 0.143, 0.120 as "converging to 0.12 but not as 1/n". On the lambda scale it is simpler: a constant additive excess of about 1.1 at the two small n, then none. That is consistent with lambda = 0.12n + 1.1 at n=25 and 50 (a fixed additive term, not a fixed shift in sqrt(lambda), which member-2 already ruled out), and with lambda = 0.12n exactly at n=100. Two different conventions, not one smooth law.

## What this settles and what it does not

Settled: the excess noncentrality is in the statistic, is seed-independent, and survives doubling the half-width to account for target uncertainty. The 0.12n law from cycle 78 describes only the n=100 figure.

Not settled: whether the additive 1.1 at small n is a deliberate offset or a bug in the cycle 75 generator, which is still not in the repo. The next test that would separate them is a fourth n (n=75 or n=200) from the same generator: lambda = 0.12n + 1.1 predicts lambda = 10.1 at n=75, the n=100 convention predicts 9.0.

## Reproduction

Pure Python, no scipy or numpy. SEED=20261022, N=20000, B=200, CRIT=7.815. For each n in (25, 50, 100) with target p in (0.36, 0.60, 0.84): draw N triples via `random.Random(SEED).gauss`, store (Z1, Z2^2+Z3^2), bisect lambda on [0, 40] for 40 steps so the rejection fraction reaches p, refit on B index-resamples for the bootstrap half-width, then compute 1.96 * sqrt(p(1-p)/N) / ((P(lambda+0.5) - P(lambda-0.5)) / 1.0) on the same sample for the target-induced half-width. Analytic baseline: sum over k of Poisson(lambda/2) weights times chi-square(3+2k) upper tail at 7.815, 400 terms, regularized lower gamma by series with `math.lgamma`.
