# Cycle 88, member-3: independent replicate with fresh seed, and the paired-SE bookkeeping

Author: member-3. Seed 2026102103 (fresh; numpy default_rng; member-2 used 2026102188). 20000 sims per n. Script: stuff/c88_member3_paired_se.py (uv run --with numpy --with scipy python stuff/c88_member3_paired_se.py).

## Per-term scales (defined before any table)

Sample x_1..x_n is standardized once: z_j = (x_j - xbar) / s, s the sample SD (ddof=1). Phi is the standard normal CDF; z_(i) is the i-th order statistic of z.

- AD scale: t_i = -((2i-1)/n) * [ln Phi(z_(i)) + ln(1 - Phi(z_(n+1-i)))], i = 1..n. Each t_i >= 0; sum t_i = A^2 + n.
- x^2 scale: t_i = z_i^2 on the same standardized sample. sum t_i = n-1 identically, so G_0 is a constant.

Statistic: G_c = sum_i log(1 + c t_i) / c for c in 1, 5, 20, 40; G_0 = sum_i t_i (uncapped; rounded to 1e-9 on the x^2 scale so float noise cannot fake rejections). Reject when G_c exceeds the 95% quantile of G_c under the normal at the same n (normal-calibrated 5%, 20000 normal sims). For t(3) the paired gain is mean(reject_c - reject_0) over the same 20000 t(3) samples; paired SE = sd(diff)/sqrt(20000); z = gain/SE.

## Table: one row per (scale, c, n, law)

Columns: scale, c, n, law, power at normal-calibrated 5%; for t(3) rows the paired gain over c=0, its paired SE, and z = gain/SE. "-" marks columns that only apply to t(3); "n/a" marks c=0 where the paired difference is identically zero.

```
scale	c	n	law	power	gain_t3	se_t3	z
ad	0	25	normal	0.0500	-	-	-
ad	0	25	t3	0.3782	+0.0000	0.0000	n/a
ad	0	25	t5	0.1892	-	-	-
ad	0	25	mix	0.2934	-	-	-
ad	1	25	normal	0.0500	-	-	-
ad	1	25	t3	0.4572	+0.0789	0.0021	+38.3
ad	1	25	t5	0.2515	-	-	-
ad	1	25	mix	0.3672	-	-	-
ad	5	25	normal	0.0500	-	-	-
ad	5	25	t3	0.4522	+0.0740	0.0023	+31.7
ad	5	25	t5	0.2524	-	-	-
ad	5	25	mix	0.3775	-	-	-
ad	20	25	normal	0.0500	-	-	-
ad	20	25	t3	0.4063	+0.0280	0.0025	+11.3
ad	20	25	t5	0.2279	-	-	-
ad	20	25	mix	0.3537	-	-	-
ad	40	25	normal	0.0500	-	-	-
ad	40	25	t3	0.3789	+0.0006	0.0027	+0.2
ad	40	25	t5	0.2147	-	-	-
ad	40	25	mix	0.3337	-	-	-
ad	0	50	normal	0.0500	-	-	-
ad	0	50	t3	0.6171	+0.0000	0.0000	n/a
ad	0	50	t5	0.3015	-	-	-
ad	0	50	mix	0.4653	-	-	-
ad	1	50	normal	0.0500	-	-	-
ad	1	50	t3	0.7296	+0.1124	0.0023	+48.8
ad	1	50	t5	0.4268	-	-	-
ad	1	50	mix	0.5952	-	-	-
ad	5	50	normal	0.0500	-	-	-
ad	5	50	t3	0.7250	+0.1079	0.0025	+43.8
ad	5	50	t5	0.4406	-	-	-
ad	5	50	mix	0.6256	-	-	-
ad	20	50	normal	0.0500	-	-	-
ad	20	50	t3	0.6780	+0.0608	0.0026	+23.7
ad	20	50	t5	0.4051	-	-	-
ad	20	50	mix	0.6131	-	-	-
ad	40	50	normal	0.0500	-	-	-
ad	40	50	t3	0.6351	+0.0179	0.0027	+6.6
ad	40	50	t5	0.3740	-	-	-
ad	40	50	mix	0.5863	-	-	-
ad	0	100	normal	0.0500	-	-	-
ad	0	100	t3	0.8521	+0.0000	0.0000	n/a
ad	0	100	t5	0.4793	-	-	-
ad	0	100	mix	0.6798	-	-	-
ad	1	100	normal	0.0500	-	-	-
ad	1	100	t3	0.9333	+0.0812	0.0019	+41.7
ad	1	100	t5	0.6683	-	-	-
ad	1	100	mix	0.8208	-	-	-
ad	5	100	normal	0.0500	-	-	-
ad	5	100	t3	0.9333	+0.0812	0.0020	+40.4
ad	5	100	t5	0.6885	-	-	-
ad	5	100	mix	0.8537	-	-	-
ad	20	100	normal	0.0500	-	-	-
ad	20	100	t3	0.9085	+0.0565	0.0020	+27.7
ad	20	100	t5	0.6513	-	-	-
ad	20	100	mix	0.8538	-	-	-
ad	40	100	normal	0.0500	-	-	-
ad	40	100	t3	0.8808	+0.0286	0.0021	+13.4
ad	40	100	t5	0.6119	-	-	-
ad	40	100	mix	0.8406	-	-	-
x2	0	25	normal	0.0000	-	-	-
x2	0	25	t3	0.0000	+0.0000	0.0000	n/a
x2	0	25	t5	0.0000	-	-	-
x2	0	25	mix	0.0000	-	-	-
x2	1	25	normal	0.0500	-	-	-
x2	1	25	t3	0.0050	+0.0050	0.0005	+10.0
x2	1	25	t5	0.0136	-	-	-
x2	1	25	mix	0.0186	-	-	-
x2	5	25	normal	0.0500	-	-	-
x2	5	25	t3	0.0059	+0.0059	0.0005	+10.8
x2	5	25	t5	0.0152	-	-	-
x2	5	25	mix	0.0194	-	-	-
x2	20	25	normal	0.0500	-	-	-
x2	20	25	t3	0.0066	+0.0066	0.0006	+11.5
x2	20	25	t5	0.0158	-	-	-
x2	20	25	mix	0.0196	-	-	-
x2	40	25	normal	0.0500	-	-	-
x2	40	25	t3	0.0067	+0.0067	0.0006	+11.7
x2	40	25	t5	0.0158	-	-	-
x2	40	25	mix	0.0193	-	-	-
x2	0	50	normal	0.0000	-	-	-
x2	0	50	t3	0.0000	+0.0000	0.0000	n/a
x2	0	50	t5	0.0000	-	-	-
x2	0	50	mix	0.0000	-	-	-
x2	1	50	normal	0.0500	-	-	-
x2	1	50	t3	0.0009	+0.0009	0.0002	+4.4
x2	1	50	t5	0.0041	-	-	-
x2	1	50	mix	0.0069	-	-	-
x2	5	50	normal	0.0500	-	-	-
x2	5	50	t3	0.0010	+0.0010	0.0002	+4.5
x2	5	50	t5	0.0043	-	-	-
x2	5	50	mix	0.0077	-	-	-
x2	20	50	normal	0.0500	-	-	-
x2	20	50	t3	0.0013	+0.0013	0.0003	+5.1
x2	20	50	t5	0.0051	-	-	-
x2	20	50	mix	0.0086	-	-	-
x2	40	50	normal	0.0500	-	-	-
x2	40	50	t3	0.0014	+0.0014	0.0003	+5.2
x2	40	50	t5	0.0056	-	-	-
x2	40	50	mix	0.0091	-	-	-
x2	0	100	normal	0.0000	-	-	-
x2	0	100	t3	0.0000	+0.0000	0.0000	n/a
x2	0	100	t5	0.0000	-	-	-
x2	0	100	mix	0.0000	-	-	-
x2	1	100	normal	0.0500	-	-	-
x2	1	100	t3	0.0001	+0.0001	0.0000	+1.0
x2	1	100	t5	0.0010	-	-	-
x2	1	100	mix	0.0014	-	-	-
x2	5	100	normal	0.0500	-	-	-
x2	5	100	t3	0.0001	+0.0001	0.0000	+1.0
x2	5	100	t5	0.0011	-	-	-
x2	5	100	mix	0.0013	-	-	-
x2	20	100	normal	0.0500	-	-	-
x2	20	100	t3	0.0001	+0.0001	0.0000	+1.0
x2	20	100	t5	0.0012	-	-	-
x2	20	100	mix	0.0019	-	-	-
x2	40	100	normal	0.0500	-	-	-
x2	40	100	t3	0.0001	+0.0001	0.0000	+1.0
x2	40	100	t5	0.0015	-	-	-
x2	40	100	mix	0.0021	-	-	-
```

## Paired-SE bookkeeping (rule 2)

z = gain/SE per n. Binding n is the n with the smallest z. Verdict is YES only if z > 2 at every n in 25, 50, 100.

```
scale	c	z25	z50	z100	binding_n	verdict
ad	1	+38.3	+48.8	+41.7	25	YES
ad	5	+31.7	+43.8	+40.4	25	YES
ad	20	+11.3	+23.7	+27.7	25	YES
ad	40	+0.2	+6.6	+13.4	25	no
x2	1	+10.0	+4.4	+1.0	100	no
x2	5	+10.8	+4.5	+1.0	100	no
x2	20	+11.5	+5.1	+1.0	100	no
x2	40	+11.7	+5.2	+1.0	100	no
```

## Which (scale, c) pairs clear two paired SE at every n

- AD scale: c=1, c=5 and c=20 clear two SE at every n. c=40 does not: its binding n is 25, where z is +0.2.
- x^2 scale: none. c=0 has power exactly 0 (constant statistic), and every capped x^2 statistic has t(3) power between 0.0001 and 0.007, far below its 5% size. At n=100 the z values are about +1.0, so no pair clears two SE at every n. The positive z at n=25 and 50 are gains over a zero baseline, not evidence of a usable test.

Note on the x^2 column: a z of +10 at n=25 with power 0.005 is a statistically real but practically empty gain. The paired SE is small because the two indicators almost never differ. Rule 2's criterion is met only at n=25 and 50 there, and fails at n=100, so the verdict stays "none" with no caveat needed.

## Verdict on cycle 86's c=20 gain

- AD scale: recovered in sign and significance. c=20 gains +0.028, +0.061 and +0.057 at n=25, 50, 100 (z = +11.3, +23.7, +27.7). It is dominated by c=1 and c=5 at every n (gains +0.079 to +0.112), so c=20 is not the best cap, only a positive one.
- x^2 scale: not recovered. c=20 has t(3) power of 0.0066, 0.0013 and 0.0001 at n=25, 50, 100, against a size of 5%. The log cap on z^2 terms shrinks the heavy-tail signal below the normal reference.

## Agreement with member-2's run (seed 2026102188)

Independent seed, same code path. AD-scale t(3) gains agree within about one paired SE at every (c, n): for example c=1 at n=25 is +0.0789 here against +0.0777 there, c=20 at n=25 is +0.0280 against +0.0236. Both runs give the same pair set (AD c=1, 5, 20 YES; AD c=40 no; x^2 all no) and the same two verdicts. The per-term scale decides the sign; this replicate removes seed luck as the explanation.
