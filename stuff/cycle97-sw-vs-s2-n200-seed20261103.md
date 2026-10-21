# Cycle 97: SW vs plain S2 at n=200, third seed 20261103

Seed: 20261103 (critical values from seed+1, N(0,1) check from seed+2, gamma draws from seed).
Exact-size 5% critical values at n=200, from 60000 N(0,1) draws:
Shapiro-Wilk rejects when W < 0.98633; plain S2 (b1 = m3^2/m2^3) rejects when b1 > 0.11288.
W uses Royston's approximation of the coefficients. This is the same script as the seed 20261101 and 20261102 items, with only the seed changed.

## Size check: separate 20000-draw N(0,1) run at n=200

| test | rejection rate | binomial SE |
|---|---|---|
| SW | 0.0510 | 0.0016 |
| plain S2 | 0.0515 | 0.0016 |

Paired SW − S2 = −0.0004 (paired SE 0.0015). Both tests are at 5% within one SE.

## Power under gamma(shape), 20000 paired draws each

| shape | sqrt(beta1) | SW power | S2 power | SW − S2 | paired SE | z |
|---|---|---|---|---|---|---|
| 50 | 0.2828 | 0.2888 | 0.3500 | −0.0612 | 0.0025 | −24.46 |
| 100 | 0.2000 | 0.1676 | 0.2061 | −0.0385 | 0.0022 | −17.84 |
| 200 | 0.1414 | 0.1075 | 0.1281 | −0.0207 | 0.0019 | −10.86 |
| 500 | 0.0894 | 0.0722 | 0.0780 | −0.0059 | 0.0016 | −3.58 |
| 1000 | 0.0632 | 0.0590 | 0.0650 | −0.0060 | 0.0016 | −3.85 |

All three seeds agree: S2 leads at every shape from sqrt(beta1) 0.28 down to 0.06.
The margins at shapes 50, 100 and 200 match the other two seeds to within one paired SE.
At shapes 500 and 1000 the S2 lead is still beyond three paired SE.

**Boundary:** none. SW does not beat S2 by more than two paired SE at any shape from 50 to 1000 at n=200. It does not sit at milder skew than the n=50 boundary between gamma(50) and gamma(100). The crossover moves the other way: SW led at gamma(50) when n=50, but trails there at n=200. So any n=200 crossover lies below shape 50, at stronger skew.
