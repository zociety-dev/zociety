# Cycle 95: SW margin over plain S2 vs gamma skewness, seed 95303 replication

Replicates stuff/cycle95-gamma-skew-results.md (seed 95201) with a fresh seed.
Script: stuff/cycle95_gamma_skew.py with only `SEED = 95303` changed, run with
numpy and scipy via `uv run --no-project --with numpy --with scipy`. Wall 13 s.

Seed 95303. n = 50, 20000 paired draws per law, all tests at exact 5% size.

Critical values (one 20000-draw N(0,1) calibration run):
- Shapiro-Wilk W, reject below 0.95363 (calibration rate 0.0500)
- plain S2 (c=2), reject above 26.51339 (calibration rate 0.0500)

| shape | sqrt(beta1) | SW power | S2 power | SW-S2 | paired SE | gap/SE | beats >2SE |
|---|---|---|---|---|---|---|---|
| 1 | 2.0000 | 0.9993 | 0.9796 | +0.0197 | 0.0010 | +20.1 | yes |
| 2 | 1.4142 | 0.9485 | 0.8145 | +0.1340 | 0.0024 | +55.6 | yes |
| 5 | 0.8944 | 0.5836 | 0.4360 | +0.1476 | 0.0026 | +56.9 | yes |
| 10 | 0.6325 | 0.3170 | 0.2345 | +0.0826 | 0.0023 | +36.6 | yes |
| 20 | 0.4472 | 0.1851 | 0.1457 | +0.0393 | 0.0019 | +20.3 | yes |
| 50 | 0.2828 | 0.1004 | 0.0832 | +0.0173 | 0.0017 | +10.2 | yes |

Monotone in skewness: no. The margin peaks at gamma(5) (sqrt(beta1) 0.89) and
falls toward both ends. Same shape as seed 95201: two adjacent inversions, at
gamma(1) and gamma(2), where SW power saturates near 1 and the headroom for a
gap collapses. From gamma(5) down to gamma(50) the margin falls monotonically
with skewness.

Agreement with seed 95201: every shape is a win beyond two paired SE in both
seeds, and the smallest-skewness margin replicates (gamma(50): +0.0173 here vs a
10.7 SE gap there, 10.2 SE here). The crossover, if any, lies below
sqrt(beta1) = 0.28.

Null check caveat: on the separate 20000-draw N(0,1) run both tests reject a
little under 5% (SW 0.0457, S2 0.0464; binomial SE about 0.0015, so roughly
2.5 to 3 SE low). Both are low by the same amount, so the paired comparison is
not tilted toward either test, but the calibration quantile carries Monte Carlo
noise of this size. Seed 95201 got 0.0494 and 0.0491.

Largest win shape: gamma(50), sqrt(beta1) 0.2828, margin +0.0173, paired SE 0.0017; adjacent inversions 2; null rejection SW 0.0457, S2 0.0464.
