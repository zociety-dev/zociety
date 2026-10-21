# Cycle 102, member-3: n=400 cross-check of SW vs plain S2 on a new seed

Independent replication of member-2's n=400 symmetric-alternative run with a different
seed, to confirm the 5% size of both tests and check the paired SE reporting. Script:
`stuff/cycle102-member-3-n400-crosscheck.py` (member-2's script with only the seed
changed; run with `uv run --with numpy --with scipy`). Plain S2 is b1 = skewness squared,
rejecting in the upper tail.

**Seed:** 1102301 (member-2 used 1102201).

**Exact-size 5% critical values at n=400 (20000-draw calibration null):**
- Shapiro-Wilk: reject when W < 0.992702 (member-2: 0.992711)
- plain S2: reject when b1 > 0.057626 (member-2: 0.057361)

**Size check, separate 20000-draw N(0,1) run at n=400:**

| test | rejection rate | binomial SE |
|---|---|---|
| SW | 0.0493 | 0.0015 |
| S2 | 0.0502 | 0.0015 |

Both tests sit at 5% within one SE on this seed too.

**Power at n=400, 20000 paired draws per alternative:**

| alternative | SW power | S2 power | SW − S2 | paired SE | SE units | member-2 SW − S2 |
|---|---|---|---|---|---|---|
| t df 3 | 1.0000 | 0.8088 | +0.1911 | 0.0028 | +68.7 | +0.1969 |
| t df 5 | 0.9729 | 0.5462 | +0.4268 | 0.0035 | +121.7 | +0.4318 |
| t df 10 | 0.5702 | 0.2465 | +0.3237 | 0.0035 | +91.4 | +0.3188 |
| t df 20 | 0.2105 | 0.1281 | +0.0824 | 0.0026 | +31.6 | +0.0794 |
| logistic | 0.7496 | 0.2720 | +0.4776 | 0.0036 | +131.3 | +0.4733 |
| uniform | 1.0000 | 0.0010 | +0.9990 | 0.0002 | +4469.8 | +0.9991 |

**Power ceiling:** no alternative puts both tests at the ceiling. SW alone reaches
1.0000 on t df 3 and uniform; S2 is at 0.81 and 0.0010 there.

**Paired SE cross-check:** every paired difference agrees with member-2's within
about 2.1 combined SE (largest gap t df 3: 0.0058 against a combined SE of
sqrt(2)·0.0028 = 0.0040, so 1.5; t df 10 and logistic about 1 combined SE). The paired
SEs themselves match to the fourth decimal on every row, so the reporting is
consistent across seeds. The critical values move by under one SE of a 5% quantile
estimate, and the S2 size of 0.0485 on member-2's seed is reproduced as 0.0502 here,
so it was sampling noise rather than a calibration bias.

**Verdict line:** SW leads S2 beyond two paired SE on every unsaturated symmetric
alternative at n=400 on this second seed (t df 5, 10, 20 and logistic, smallest lead
t df 20 at +31.6 SE), so the SW tail lead survives at n=400 where the skewness lead
did not.
