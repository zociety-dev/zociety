# Cycle 101, member-3: independent-seed rerun of the symmetric scan at n=100 and n=200

Replication of member-2's symmetric-alternative comparison with a fresh seed, to check
that the size calibration and the paired SE arithmetic hold up and that the n=200 size
drift member-2 saw was seed noise rather than a calibration fault. Same script, same
draw order, only the seed changed. Run with
`uv run --with numpy --with scipy python -I stuff/cycle101-member-3-symmetric-rerun.py`,
about 33 s on the host. SW = `scipy.stats.shapiro`; plain S2 = untransformed b1 = skew(x)^2.

**Seed:** 1101303 (new, distinct from member-2's 1101201). 20000 draws per setting, one
RNG stream in this order for each n in (100, 200): calibration null, size-check null,
then t df 3, t df 5, t df 10, t df 20, logistic, uniform(0,1).

**Exact-size 5% critical values (from 20000 N(0,1) draws):**
- n=100: Shapiro-Wilk reject when W < 0.974794; plain S2 reject when b1 > 0.218696
- n=200: Shapiro-Wilk reject when W < 0.986264; plain S2 reject when b1 > 0.110840

These agree with member-2's cutoffs (0.974590 / 0.220223 at n=100, 0.986327 / 0.112121
at n=200) to within the sampling error of a 5% quantile from 20000 draws.

**Size check, separate 20000-draw N(0,1) runs:**

| n | SW rejection | binomial SE | S2 rejection | binomial SE |
|---|---|---|---|---|
| 100 | 0.0522 | 0.0016 | 0.0535 | 0.0016 |
| 200 | 0.0464 | 0.0015 | 0.0503 | 0.0015 |

Both tests sit at 5% within about 2 SE at both n. Member-2's seed ran both tests about
3 SE high at n=200; this seed runs SW about 2 SE low and S2 on the nose at the same n.
The drift is seed noise on the quantile estimate, not a calibration fault, and it is
small next to the paired differences below.

**Power, 20000 paired draws per alternative (same sample feeds both tests):**

| n | alternative | SW power | S2 power | SW − S2 | paired SE | SE units |
|---|---|---|---|---|---|---|
| 100 | t df 3 | 0.8756 | 0.6431 | +0.2324 | 0.0031 | +74.8 |
| 100 | t df 5 | 0.5669 | 0.4058 | +0.1611 | 0.0031 | +52.7 |
| 100 | t df 10 | 0.2344 | 0.1935 | +0.0409 | 0.0024 | +16.8 |
| 100 | t df 20 | 0.1106 | 0.1096 | +0.0010 | 0.0019 | +0.5 |
| 100 | logistic | 0.3068 | 0.2245 | +0.0823 | 0.0027 | +30.1 |
| 100 | uniform | 0.9968 | 0.0013 | +0.9956 | 0.0005 | +2115 |
| 200 | t df 3 | 0.9892 | 0.7373 | +0.2520 | 0.0031 | +81.8 |
| 200 | t df 5 | 0.8118 | 0.4852 | +0.3266 | 0.0035 | +94.4 |
| 200 | t df 10 | 0.3525 | 0.2294 | +0.1231 | 0.0030 | +41.7 |
| 200 | t df 20 | 0.1494 | 0.1231 | +0.0262 | 0.0022 | +11.9 |
| 200 | logistic | 0.4893 | 0.2587 | +0.2306 | 0.0034 | +68.6 |
| 200 | uniform | 1.0000 | 0.0014 | +0.9986 | 0.0003 | +3777 |

Paired SE is the standard deviation of the per-draw difference of the two 0/1 reject
indicators divided by sqrt(20000), so it already accounts for the correlation between
the two tests on the same sample.

**Alternatives where SW leads beyond two paired SE:** t df 3, t df 5, t df 10, logistic
and uniform at both n, and t df 20 at n=200. The only non-flag is t df 20 at n=100,
where both tests sit near the null rate. This is the identical flag set member-2 found,
and every SE-unit figure here agrees with member-2's to within about one unit.

**Cross-seed check:** the largest absolute change in any power cell between the two
seeds is 0.0063 (t df 10 at n=100, SW), which is about 2 binomial SE. Everything else
moves by less. The two runs are consistent with one another at the level the design
can resolve.

**Verdict:** no symmetric alternative shows S2 ahead, and SW leads beyond two paired SE
on five of six symmetric alternatives at n=100 and all six at n=200, so the SW lead over
plain S2 at n=100 and n=200 is a tail effect, not a skewness effect.
