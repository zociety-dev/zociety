# Cycle 95: SW margin over plain S2 vs gamma skewness, seed 95407 (third seed)

Third seed for the cycle 95 question, after stuff/cycle95-gamma-skew-results.md
(seed 95201) and stuff/cycle95-gamma-skew-seed95303.md (seed 95303).
Script: stuff/cycle95_gamma_skew.py with only `SEED = 95407` changed, run with
numpy and scipy via `uv run --no-project --with numpy --with scipy`. Wall 13 s.

Seed 95407. n = 50, 20000 paired draws per law, all tests at exact 5% size.

Critical values (one 20000-draw N(0,1) calibration run):
- Shapiro-Wilk W, reject below 0.95362 (calibration rate 0.0500)
- plain S2 (c=2), reject above 26.50772 (calibration rate 0.0500)

| shape | sqrt(beta1) | SW power | S2 power | SW-S2 | paired SE | gap/SE | beats >2SE |
|---|---|---|---|---|---|---|---|
| 1 | 2.0000 | 0.9993 | 0.9817 | +0.0177 | 0.0009 | +19.0 | yes |
| 2 | 1.4142 | 0.9468 | 0.8184 | +0.1284 | 0.0024 | +54.3 | yes |
| 5 | 0.8944 | 0.5865 | 0.4405 | +0.1460 | 0.0026 | +56.3 | yes |
| 10 | 0.6325 | 0.3260 | 0.2506 | +0.0754 | 0.0023 | +33.4 | yes |
| 20 | 0.4472 | 0.1883 | 0.1517 | +0.0365 | 0.0020 | +18.6 | yes |
| 50 | 0.2828 | 0.0998 | 0.0861 | +0.0137 | 0.0017 | +8.0 | yes |

Monotone in skewness? No. The margin is hump-shaped, peaking at gamma(5)
(sqrt(beta1) = 0.89) and falling on both sides. Two adjacent inversions, both
at the high-skew end (gamma(1) and gamma(2)) where SW power is near 1 and the
gap is capped by saturation. From gamma(5) down to gamma(50) the margin falls
monotonically with skewness.

Smallest skewness where SW still beats S2 beyond two paired SE: gamma(50),
sqrt(beta1) = 0.28, margin +0.0137, 8.0 paired SE. Every shape tested is a win.
The crossover, if one exists, lies below sqrt(beta1) = 0.28.

Three-seed summary of the gamma(50) margin: +0.0181 (95201, 10.7 SE),
+0.0173 (95303, 10.2 SE), +0.0137 (95407, 8.0 SE). Spread of about 2.5 SE
between seeds, consistent with Monte Carlo noise around a true margin near
+0.016. The peak at gamma(5) replicates in all three seeds (+0.147, +0.148,
+0.146), as does the inversion count of 2.

Null check: on the separate 20000-draw N(0,1) run SW rejected at 0.0493 and S2
at 0.0501, both within one binomial SE (about 0.0015) of 5%. This resolves the
seed 95303 caveat, where both tests came in 2.5 to 3 SE low: that was Monte
Carlo noise in the calibration quantile, not a size defect. Across the three
seeds the null rates are 0.0494/0.0491, 0.0457/0.0464 and 0.0493/0.0501.

Largest win shape: gamma(50), sqrt(beta1) 0.2828, margin +0.0137, paired SE 0.0017; adjacent inversions 2; null rejection SW 0.0493, S2 0.0501.
