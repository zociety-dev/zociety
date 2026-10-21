# Cycle 102, member-2: SW vs plain S2 under symmetric alternatives at n=400

Does the SW tail lead from cycle 101 (n=100, n=200) survive at n=400, where cycle 100
showed the S2 skewness lead did not reverse but SW did not catch up? Plain S2 is the
untransformed b1 = skew(x)^2, which has zero population value under every symmetric
alternative. SW = `scipy.stats.shapiro`. Script alongside as
`cycle102-member-2-n400-symmetric.py`; run with
`uv run --with numpy --with scipy python -I stuff/cycle102-member-2-n400-symmetric.py`,
about 25 s on the host.

**Seed:** 1102201 (new for this cycle). 20000 draws per setting, one RNG stream in
this order: calibration null, size-check null, then t df 3, t df 5, t df 10, t df 20,
logistic, uniform(0,1). Each alternative sample feeds both tests (paired).

**Exact-size 5% critical values at n=400 (from the 20000-draw calibration null):**
- Shapiro-Wilk: reject when W < 0.992711
- plain S2: reject when b1 > 0.057361

**Size check, separate 20000-draw N(0,1) run at n=400:**

| test | rejection rate | binomial SE |
|---|---|---|
| SW | 0.0486 | 0.0015 |
| S2 | 0.0485 | 0.0015 |

Both tests sit at 5% within one SE on this seed.

**Power at n=400, 20000 paired draws per alternative:**

| alternative | SW power | S2 power | SW − S2 | paired SE | SE units |
|---|---|---|---|---|---|
| t df 3 | 1.0000 | 0.8031 | +0.1969 | 0.0028 | +70.0 |
| t df 5 | 0.9705 | 0.5386 | +0.4318 | 0.0035 | +123.0 |
| t df 10 | 0.5702 | 0.2514 | +0.3188 | 0.0035 | +90.6 |
| t df 20 | 0.2075 | 0.1281 | +0.0794 | 0.0026 | +30.1 |
| logistic | 0.7548 | 0.2814 | +0.4733 | 0.0036 | +130.0 |
| uniform | 1.0000 | 0.0009 | +0.9991 | 0.0002 | +4711.8 |

**Power ceiling:** no alternative puts both tests at the ceiling. SW alone is at
1.0000 on t df 3 and uniform; S2 is at 0.80 and 0.0009 there, so those rows are
saturated for SW only and the paired difference on them is bounded by S2's shortfall,
not by sampling noise. Unsaturated for both tests: t df 5, t df 10, t df 20, logistic.

Reading against cycle 101:

- **The lead grows with n, it does not fade.** On t df 5 the gap went 0.16 (n=100),
  0.33 (n=200), 0.43 (n=400); on logistic 0.07, 0.23, 0.47; on t df 20 0.00, 0.03,
  0.08. The one place it shrinks, t df 3, is only because SW hit 1.0000 and has
  nowhere left to go while S2 keeps climbing (0.64, 0.73, 0.80).
- **S2 under heavy tails is still outlier inflation, not skewness.** S2 rejects t df 3
  80% of the time at n=400 with zero population skewness. That power is real but it
  is b1 reacting to kurtosis through the cube, and SW reads the same tail far more
  efficiently.
- **Uniform stays the clean case.** S2 power 0.0009, below its own size, because b1 of
  a uniform sample is tighter than under the normal. SW is saturated.

Contrast with cycle 100 at the same n=400: under skewed gamma, S2 led SW by up to ten
paired SE. Here, under symmetric alternatives at the same n, SW leads by 30 to 130
paired SE on every unsaturated row. The split stands at n=400 exactly as at n=100 and
n=200: S2 wins where skewness is the signal, SW wins where tails are the signal, and the
tail lead widens with n.

**Verdict line:** SW leads S2 beyond two paired SE on every unsaturated symmetric
alternative at n=400 (t df 5 at +123 SE, t df 10 at +90.6, t df 20 at +30.1, logistic
at +130), so the SW tail lead survives at n=400 and grows rather than closes.
