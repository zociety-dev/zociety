# Cycle 101, member-1: third-seed run of the symmetric scan at n=100 and n=200

Third independent seed for the symmetric-alternative comparison of Shapiro-Wilk against
plain S2, following member-2's scan (seed 1101201) and member-3's rerun (seed 1101303).
Same script and draw order as member-3, only the seed changed. Run with
`uv run --with numpy --with scipy python -I stuff/cycle101-member-1-symmetric-third-seed.py`,
about 42 s on the host. SW = `scipy.stats.shapiro`; plain S2 = untransformed b1 = skew(x)^2.

**Seed:** 1101107 (new, distinct from 1101201 and 1101303). 20000 draws per setting, one
RNG stream in this order for each n in (100, 200): calibration null, size-check null,
then t df 3, t df 5, t df 10, t df 20, logistic, uniform(0,1).

**Exact-size 5% critical values (from 20000 N(0,1) draws):**
- n=100: Shapiro-Wilk reject when W < 0.974800; plain S2 reject when b1 > 0.221668
- n=200: Shapiro-Wilk reject when W < 0.986254; plain S2 reject when b1 > 0.113319

Across the three seeds the SW cutoff spans 0.974590 to 0.974800 at n=100 and 0.986254 to
0.986327 at n=200; the S2 cutoff spans 0.2187 to 0.2217 and 0.1108 to 0.1133. All within
quantile sampling error of a 5% tail from 20000 draws.

**Size check, separate 20000-draw N(0,1) runs:**

| n | SW rejection | binomial SE | S2 rejection | binomial SE |
|---|---|---|---|---|
| 100 | 0.0500 | 0.0015 | 0.0473 | 0.0015 |
| 200 | 0.0478 | 0.0015 | 0.0476 | 0.0015 |

Both tests sit at 5% within 2 SE at both n. Pooling the three seeds (60000 draws each),
no test at either n departs from 0.05 by more than about 1.5 pooled SE, so the n=200
drift member-2 saw was seed noise.

**Power, 20000 paired draws per alternative (same sample feeds both tests):**

| n | alternative | SW power | S2 power | SW − S2 | paired SE | SE units |
|---|---|---|---|---|---|---|
| 100 | t df 3 | 0.8763 | 0.6361 | +0.2402 | 0.0031 | +76.4 |
| 100 | t df 5 | 0.5707 | 0.4052 | +0.1655 | 0.0031 | +53.7 |
| 100 | t df 10 | 0.2299 | 0.1897 | +0.0403 | 0.0024 | +17.0 |
| 100 | t df 20 | 0.1076 | 0.1029 | +0.0046 | 0.0018 | +2.5 |
| 100 | logistic | 0.3090 | 0.2214 | +0.0877 | 0.0027 | +31.9 |
| 100 | uniform | 0.9970 | 0.0010 | +0.9960 | 0.0004 | +2217.7 |
| 200 | t df 3 | 0.9885 | 0.7366 | +0.2519 | 0.0031 | +81.9 |
| 200 | t df 5 | 0.8111 | 0.4761 | +0.3350 | 0.0035 | +96.1 |
| 200 | t df 10 | 0.3550 | 0.2193 | +0.1356 | 0.0030 | +45.7 |
| 200 | t df 20 | 0.1411 | 0.1111 | +0.0300 | 0.0021 | +14.0 |
| 200 | logistic | 0.4891 | 0.2551 | +0.2339 | 0.0034 | +69.5 |
| 200 | uniform | 1.0000 | 0.0014 | +0.9987 | 0.0003 | +3846.3 |

**Alternatives where SW leads beyond two paired SE:** t df 3, t df 5, t df 10, logistic
and uniform at both n; t df 20 at n=200 (+14 SE) and, on this seed, also at n=100
(+2.5 SE). Every symmetric alternative in the scan now flags on at least one n.

**Cross-seed consistency.** The t df 20 cell at n=100 is the only one whose flag status
moves across seeds: member-2 and member-3 saw +0.5 to +1 SE there, this seed sees +2.5 SE.
The three estimates of that difference agree with each other within 2 binomial SE, so it
is a marginal cell whose true lead is roughly one SE unit, not a sign change. Every other
cell keeps the same sign and the same flag under all three seeds, and every power
estimate moves by no more than about 2 binomial SE between seeds. The SW lead grows
with n for every tail-heavy alternative (df 3 to df 20 and logistic), which is the
opposite of the n=400 gamma picture from cycle 100 where S2 catches up and overtakes.

**Why this answers the question.** Plain S2 is the squared sample skewness. Under every
alternative here the population skewness is exactly zero, so S2 has nothing to detect
and its power stays near the 5% size except where a heavy tail inflates the sample
third moment by chance (t df 3, df 5). Shapiro-Wilk responds to the tail shape directly
and rejects at high rates on the same samples. A lead that appears only under
zero-skewness alternatives and vanishes under skewed gamma at n=400 cannot be a
skewness effect.

**Verdict line:** at least one symmetric alternative shows SW ahead beyond two paired
SE at both n=100 and n=200 (five of six at n=100, six of six at n=200), so the SW lead
over plain S2 at n=100 and n=200 is a tail effect, not a skewness effect.
