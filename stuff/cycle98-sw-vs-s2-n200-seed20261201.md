# Cycle 98: SW vs plain S2 crossover at n=200, seed 20261201

Seed 20261201. Exact-size 5% critical values come from 20000 N(0,1) draws at n=200: Shapiro-Wilk rejects when W < 0.98639, and plain S2 (b1 = m3^2/m2^3) rejects when b1 > 0.11179.
W uses Royston's approximation of the coefficients. Script: `stuff/cycle98-sw-vs-s2-n200-seed20261201.py` (pure Python, `python3 -I ... 20261201`).

## Size check (separate 20000-draw N(0,1) run, n=200)

| test | rejection rate | binomial SE |
|---|---|---|
| Shapiro-Wilk | 0.0525 | 0.0016 |
| plain S2 | 0.0522 | 0.0016 |

Paired SW − S2 = +0.0003 (paired SE 0.0015). Both tests sit at 5% within two SE.

## Power under gamma(shape), 20000 paired draws, n=200

| shape | sqrt(beta1) | SW power | S2 power | SW − S2 | paired SE | z |
|---|---|---|---|---|---|---|
| 2 | 1.414 | 1.0000 | 1.0000 | +0.0000 | 0.0000 | tie |
| 5 | 0.894 | 0.9985 | 0.9957 | +0.0029 | 0.0004 | +6.8 |
| 10 | 0.632 | 0.9074 | 0.9193 | −0.0119 | 0.0016 | −7.3 |
| 20 | 0.447 | 0.6225 | 0.6861 | −0.0636 | 0.0025 | −25.1 |
| 50 | 0.283 | 0.2924 | 0.3496 | −0.0571 | 0.0025 | −23.3 |

At gamma(2) both tests reject every draw, so there is no margin there. SW leads at gamma(5), and S2 leads from gamma(10) onward. This fits cycle 97, where S2 led at every shape from 50 up.

**Flip:** SW − S2 changes sign beyond two paired SE between gamma(5) (sqrt(beta1) 0.894, margin +0.0029, +6.8 SE) and gamma(10) (sqrt(beta1) 0.632, margin −0.0119, −7.3 SE).
