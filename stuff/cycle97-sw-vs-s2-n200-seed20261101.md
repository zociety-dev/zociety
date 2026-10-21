# Cycle 97: SW vs plain S2 at n=200, gamma(50) to gamma(1000), seed 20261101

Does the point where the Shapiro-Wilk margin over plain S2 vanishes move to milder skew as n grows from 50 to 200?

**Seed:** 20261101 (paired gamma sweep), 20261102 (null calibration stream), 20261103 (separate N(0,1) size check). **n:** 200. **Paired draws per shape:** 20000. **Null calibration:** 60000 N(0,1) draws.
**Exact-size 5% critical values at n=200:** Shapiro-Wilk rejects when W < 0.98632. Plain S2 (squared sample skewness b1 = m3^2 / m2^3) rejects when b1 > 0.11254.

Method: pure Python, Royston (1992) AS R94 SW weights, `random.gammavariate` draws. Each replicate draws one gamma(shape) sample of 200 and scores it with both tests. Paired SE is sd(I_SW - I_S2)/sqrt(20000). Run time 26 s.

## N(0,1) size check (separate 20000 draws)

| test | rejection rate | binomial SE |
|---|---|---|
| SW | 0.0517 | 0.0016 |
| S2 | 0.0507 | 0.0016 |

Both tests are within 1.1 SE of 0.05. Paired difference +0.0010 (paired SE 0.0015).

## Power and margin against sqrt(beta1) = 2/sqrt(shape)

| shape | sqrt(beta1) | SW | S2 | SW - S2 | paired SE | z |
|---|---|---|---|---|---|---|
| 50 | 0.2828 | 0.2886 | 0.3462 | -0.0576 | 0.0025 | -23.44 |
| 100 | 0.2000 | 0.1643 | 0.2009 | -0.0365 | 0.0021 | -17.13 |
| 200 | 0.1414 | 0.1044 | 0.1287 | -0.0243 | 0.0019 | -12.81 |
| 500 | 0.0894 | 0.0703 | 0.0811 | -0.0109 | 0.0017 | -6.51 |
| 1000 | 0.0632 | 0.0623 | 0.0644 | -0.0021 | 0.0016 | -1.29 |

## Reading

At n=200 S2 beats SW at every shape in the sweep, by 6 to 23 paired SE from gamma(50) to gamma(500). The S2 lead shrinks as skew falls and is within noise by gamma(1000). At n=50 SW still led at gamma(50) by about 8 paired SE. At n=200 the same shape gives S2 a 5.8-point lead. So with more data the SW advantage does not reach milder skew. It moves the other way, to stronger skew than gamma(50) (sqrt(beta1) > 0.28). That fits SW spending its power on tail and kurtosis departures that the near-normal gammas do not have, while S2 puts all its power on skewness, the only departure they do have.

Next: to find where SW's lead comes back at n=200, sweep stronger skew (gamma(5), gamma(10), gamma(20)), not milder.

**Closing line (rule 2):** none. No shape from gamma(50) to gamma(1000) has SW minus S2 beyond +2 paired SE at n=200. The closest is gamma(1000) (sqrt(beta1)=0.0632, margin -0.0021, paired SE 0.0016). The boundary does not sit at milder skew than the n=50 boundary between gamma(50) and gamma(100). It sits at stronger skew than gamma(50).
