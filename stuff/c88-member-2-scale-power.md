# Cycle 88: per-term scale fixed, power alone, c-grid under AD and x^2 terms

Author: member-2. Seed 2026102188 (fresh; numpy default_rng). 20000 sims per n. Script: stuff/c88_scale_power.py (uv run --with numpy --with scipy).

## Per-term scales (defined before any table)

Sample x_1..x_n is standardized once: z_j = (x_j - xbar) / s with s the sample SD (ddof=1). Phi is the standard normal CDF; z_(i) is the i-th order statistic of z.

- AD scale: t_i = -((2i-1)/n) * [ln Phi(z_(i)) + ln(1 - Phi(z_(n+1-i)))], i = 1..n. Each t_i >= 0 and sum t_i = A^2 + n.
- x^2 scale: t_i = z_i^2 on the same standardized sample. Note sum t_i = n-1 identically, so c=0 is a constant.

Statistic: G_c = sum_i log(1 + c t_i) / c for c in 1, 5, 20, 40; G_0 = sum_i t_i (uncapped). Reject when G_c exceeds the 95% quantile of G_c under the normal at the same n (normal-calibrated 5%, same 20000 normal sims). For t(3) the paired gain is mean(reject_c - reject_0) over the same 20000 t(3) samples with paired SE = sd(diff)/sqrt(20000). G_0 on the x^2 scale is rounded to 1e-9 so float noise does not fake rejections; its power is therefore exactly 0 everywhere.

## Table: one row per (scale, c, n, law)

Columns: scale, c, n, law, power at normal-calibrated 5%, then for t(3) the paired gain over c=0 and its paired SE.

```
/tmp/c88_scale_power.py:71: RuntimeWarning: invalid value encountered in scalar divide
  zs = " ".join(f"{summary[(scale, c, n)][0] / summary[(scale, c, n)][1]:+.1f}" for n in NS)
scale	c	n	law	power	gain_t3	se_t3
ad	0	25	normal	0.0500
ad	0	25	t3	0.3804	+0.0000	0.0000
ad	0	25	t5	0.1908
ad	0	25	mix	0.2879
ad	1	25	normal	0.0500
ad	1	25	t3	0.4581	+0.0777	0.0021
ad	1	25	t5	0.2537
ad	1	25	mix	0.3638
ad	5	25	normal	0.0500
ad	5	25	t3	0.4501	+0.0697	0.0023
ad	5	25	t5	0.2540
ad	5	25	mix	0.3761
ad	20	25	normal	0.0500
ad	20	25	t3	0.4040	+0.0236	0.0025
ad	20	25	t5	0.2292
ad	20	25	mix	0.3525
ad	40	25	normal	0.0500
ad	40	25	t3	0.3769	-0.0035	0.0027
ad	40	25	t5	0.2170
ad	40	25	mix	0.3344
ad	0	50	normal	0.0500
ad	0	50	t3	0.6019	+0.0000	0.0000
ad	0	50	t5	0.3044
ad	0	50	mix	0.4593
ad	1	50	normal	0.0500
ad	1	50	t3	0.7167	+0.1148	0.0023
ad	1	50	t5	0.4339
ad	1	50	mix	0.5899
ad	5	50	normal	0.0500
ad	5	50	t3	0.7147	+0.1128	0.0025
ad	5	50	t5	0.4449
ad	5	50	mix	0.6181
ad	20	50	normal	0.0500
ad	20	50	t3	0.6653	+0.0634	0.0026
ad	20	50	t5	0.4051
ad	20	50	mix	0.6031
ad	40	50	normal	0.0500
ad	40	50	t3	0.6283	+0.0263	0.0027
ad	40	50	t5	0.3756
ad	40	50	mix	0.5800
ad	0	100	normal	0.0500
ad	0	100	t3	0.8538	+0.0000	0.0000
ad	0	100	t5	0.4817
ad	0	100	mix	0.6805
ad	1	100	normal	0.0500
ad	1	100	t3	0.9342	+0.0804	0.0019
ad	1	100	t5	0.6753
ad	1	100	mix	0.8236
ad	5	100	normal	0.0500
ad	5	100	t3	0.9339	+0.0801	0.0020
ad	5	100	t5	0.6939
ad	5	100	mix	0.8555
ad	20	100	normal	0.0500
ad	20	100	t3	0.9091	+0.0553	0.0020
ad	20	100	t5	0.6525
ad	20	100	mix	0.8551
ad	40	100	normal	0.0500
ad	40	100	t3	0.8827	+0.0289	0.0021
ad	40	100	t5	0.6140
ad	40	100	mix	0.8422
x2	0	25	normal	0.0000
x2	0	25	t3	0.0000	+0.0000	0.0000
x2	0	25	t5	0.0000
x2	0	25	mix	0.0000
x2	1	25	normal	0.0500
x2	1	25	t3	0.0046	+0.0046	0.0005
x2	1	25	t5	0.0139
x2	1	25	mix	0.0178
x2	5	25	normal	0.0500
x2	5	25	t3	0.0056	+0.0056	0.0005
x2	5	25	t5	0.0145
x2	5	25	mix	0.0180
x2	20	25	normal	0.0500
x2	20	25	t3	0.0063	+0.0063	0.0006
x2	20	25	t5	0.0155
x2	20	25	mix	0.0185
x2	40	25	normal	0.0500
x2	40	25	t3	0.0064	+0.0064	0.0006
x2	40	25	t5	0.0162
x2	40	25	mix	0.0188
x2	0	50	normal	0.0000
x2	0	50	t3	0.0000	+0.0000	0.0000
x2	0	50	t5	0.0000
x2	0	50	mix	0.0000
x2	1	50	normal	0.0500
x2	1	50	t3	0.0011	+0.0011	0.0002
x2	1	50	t5	0.0066
x2	1	50	mix	0.0083
x2	5	50	normal	0.0500
x2	5	50	t3	0.0015	+0.0015	0.0003
x2	5	50	t5	0.0072
x2	5	50	mix	0.0082
x2	20	50	normal	0.0500
x2	20	50	t3	0.0016	+0.0016	0.0003
x2	20	50	t5	0.0076
x2	20	50	mix	0.0083
x2	40	50	normal	0.0500
x2	40	50	t3	0.0016	+0.0016	0.0003
x2	40	50	t5	0.0073
x2	40	50	mix	0.0084
x2	0	100	normal	0.0000
x2	0	100	t3	0.0000	+0.0000	0.0000
x2	0	100	t5	0.0000
x2	0	100	mix	0.0000
x2	1	100	normal	0.0500
x2	1	100	t3	0.0000	+0.0000	0.0000
x2	1	100	t5	0.0008
x2	1	100	mix	0.0018
x2	5	100	normal	0.0500
x2	5	100	t3	0.0000	+0.0000	0.0000
x2	5	100	t5	0.0008
x2	5	100	mix	0.0019
x2	20	100	normal	0.0500
x2	20	100	t3	0.0001	+0.0001	0.0000
x2	20	100	t5	0.0009
x2	20	100	mix	0.0021
x2	40	100	normal	0.0500
x2	40	100	t3	0.0001	+0.0001	0.0001
x2	40	100	t5	0.0010
x2	40	100	mix	0.0024
```

## Which (scale, c) pairs gain t(3) power over c=0 by more than two paired SE at every n

gain/SE at n = 25, 50, 100:

- AD, c=1: YES (+37.7, +49.3, +41.5)
- AD, c=5: YES (+30.2, +45.3, +40.0)
- AD, c=20: YES (+9.5, +24.8, +27.2)
- AD, c=40: no (-1.3, +9.9, +13.7); fails at n=25
- x^2, c=1: no; x^2, c=5: no; x^2, c=20: no; x^2, c=40: no. The x^2 gains are 0.000-0.006 in absolute terms and vanish at n=100 (gain 0.0000-0.0001, SE 0.0000-0.0001), so no x^2 pair clears two SE at every n. These "gains" are only measured against a degenerate c=0 with power 0; every capped x^2 statistic has t(3) power far below its 5% size (0.000-0.006), because concavity of the cap on a sample forced to sum z^2 = n-1 makes heavy tails shrink G_c rather than grow it.

## Verdict on cycle 86 c=20

Under the AD scale a c=20 gain over c=0 is recovered: +0.024, +0.063, +0.055 at n = 25, 50, 100, each more than nine paired SE. It is not the best c: c=1 and c=5 beat c=20 at every n by 0.025-0.05, and c=40 loses the gain at n=25. Under the x^2 scale cycle 86 c=20 gain is not recovered: c=0 is a constant, and the capped statistics have t(3) power 0.006, 0.002, 0.000 at n = 25, 50, 100, below size. The sign of the cycle 86 result therefore depends entirely on the per-term scale, confirming the cycle 87 learning: the AD term scale gives the gain, the x^2 scale gives a test with no power at all.

The cycle 86 numeric value is not in this branch (stuff/ was empty at cycle 88 start), so this is a verdict on sign and significance, not on matching its magnitude.
