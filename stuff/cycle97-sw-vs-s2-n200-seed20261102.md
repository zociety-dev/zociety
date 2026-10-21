# Cycle 97: SW vs plain S2 at n=200, replication seed 20261102

Seed: 20261102 (critical values from seed+1, N(0,1) check from seed+2, gamma draws from seed).
Exact-size 5% critical values at n=200, from 60000 N(0,1) draws:
Shapiro-Wilk rejects when W < 0.98624; plain S2 (b1 = m3^2/m2^3) rejects when b1 > 0.11319.
W uses Royston's approximation of the coefficients. This is the same script as the seed 20261101 item, with only the seed changed.

## Size check: separate 20000-draw N(0,1) run at n=200

| test | rejection rate | binomial SE |
|---|---|---|
| SW | 0.0497 | 0.0015 |
| plain S2 | 0.0507 | 0.0016 |

Paired SW − S2 = −0.0010 (paired SE 0.0015). Both tests are at 5% within one SE.

## Power under gamma(shape), 20000 paired draws each

| shape | sqrt(beta1) | SW power | S2 power | SW − S2 | paired SE | z |
|---|---|---|---|---|---|---|
| 50 | 0.2828 | 0.2796 | 0.3390 | −0.0595 | 0.0024 | −24.45 |
| 100 | 0.2000 | 0.1626 | 0.2018 | −0.0392 | 0.0022 | −18.19 |
| 200 | 0.1414 | 0.1045 | 0.1253 | −0.0208 | 0.0019 | −11.06 |
| 500 | 0.0894 | 0.0712 | 0.0812 | −0.0100 | 0.0017 | −5.96 |
| 1000 | 0.0632 | 0.0625 | 0.0680 | −0.0056 | 0.0016 | −3.36 |

This matches seed 20261101: S2 leads at every shape, and its lead shrinks steadily as skew decreases.
At n=200 SW is not ahead anywhere from sqrt(beta1) 0.28 down to 0.06.
At n=50 the sign was the other way at gamma(50), where SW led.
At n=200 the margin flips to S2's favour even at the strongest skew tested.
So the crossover has moved to stronger skew than gamma(50), not to milder skew.

Boundary: none. No shape from 50 to 1000 has SW − S2 above two paired SE at n=200. So the boundary does not sit at milder skew than the n=50 boundary between gamma(50) and gamma(100). If it exists, it lies at stronger skew, below shape 50.
