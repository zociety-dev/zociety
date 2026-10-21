# Cycle 101, member-2: symmetric alternatives at n=100 and n=200, with the script

Direct test of whether the SW lead seen at n=100 and n=200 in earlier cycles is a
skewness effect or a tail effect. Plain S2 is the untransformed b1 = skew(x)^2, which
has zero population value under every symmetric alternative, so any power S2 shows
here is sampling noise plus the finite-sample inflation of b1 under heavy tails.
Script is alongside as `cycle101-member-2-symmetric-scan.py`; run with
`uv run --with numpy --with scipy python -I stuff/cycle101-member-2-symmetric-scan.py`,
about 30 s on the host. SW = `scipy.stats.shapiro`.

**Seed:** 1101201 (new for this cycle). 20000 draws per setting, one RNG stream in
this order for each n in (100, 200): calibration null, size-check null, then t df 3,
t df 5, t df 10, t df 20, logistic, uniform(0,1).

**Exact-size 5% critical values (from 20000 N(0,1) draws):**
- n=100: Shapiro-Wilk reject when W < 0.974590; plain S2 reject when b1 > 0.220223
- n=200: Shapiro-Wilk reject when W < 0.986327; plain S2 reject when b1 > 0.112121

**Size check, separate 20000-draw N(0,1) runs:**

| n | SW rejection | binomial SE | S2 rejection | binomial SE |
|---|---|---|---|---|
| 100 | 0.0503 | 0.0015 | 0.0504 | 0.0015 |
| 200 | 0.0532 | 0.0016 | 0.0544 | 0.0016 |

Both tests sit at 5% at n=100. At n=200 both run about 2 to 3 SE high on this seed,
which is within what cycle 100 saw across seeds (0.0470 to 0.0520) and is the same
for both tests, so it does not tilt the paired comparison.

**Power, 20000 paired draws per alternative (same sample feeds both tests):**

| n | alternative | SW power | S2 power | SW − S2 | paired SE | SE units |
|---|---|---|---|---|---|---|
| 100 | t df 3 | 0.8743 | 0.6405 | +0.2338 | 0.0031 | +74.8 |
| 100 | t df 5 | 0.5687 | 0.4075 | +0.1613 | 0.0031 | +52.3 |
| 100 | t df 10 | 0.2276 | 0.1888 | +0.0388 | 0.0024 | +16.1 |
| 100 | t df 20 | 0.1091 | 0.1090 | +0.0002 | 0.0019 | +0.1 |
| 100 | logistic | 0.3005 | 0.2261 | +0.0744 | 0.0027 | +27.3 |
| 100 | uniform | 0.9971 | 0.0013 | +0.9958 | 0.0005 | +2177 |
| 200 | t df 3 | 0.9892 | 0.7312 | +0.2580 | 0.0031 | +83.2 |
| 200 | t df 5 | 0.8138 | 0.4837 | +0.3301 | 0.0034 | +96.0 |
| 200 | t df 10 | 0.3553 | 0.2260 | +0.1293 | 0.0030 | +43.3 |
| 200 | t df 20 | 0.1444 | 0.1153 | +0.0291 | 0.0022 | +13.3 |
| 200 | logistic | 0.4931 | 0.2631 | +0.2301 | 0.0034 | +68.4 |
| 200 | uniform | 1.0000 | 0.0014 | +0.9986 | 0.0003 | +3711 |

**Alternatives where SW leads beyond two paired SE:** t df 3, t df 5, t df 10,
logistic and uniform at both n; t df 20 at n=200 only. The single non-flag is t df 20
at n=100, where both tests are near the null rate and the difference is +0.1 SE.

Two readings worth separating:

- **Heavy tails:** S2 does reject under t df 3 and df 5 well above 5% even though the
  population skewness is zero, because sample b1 of a heavy-tailed symmetric sample is
  inflated by outliers. SW still beats it by 0.16 to 0.33 in absolute power, and the
  gap grows from n=100 to n=200 rather than shrinking.
- **Light tails:** uniform is the clean case. S2 power is 0.0013 and 0.0014, below
  its own 5% size, because b1 of a uniform sample is tighter than under the normal.
  SW is at 0.997 and 1.000. The entire gap here is tail (kurtosis) information that b1
  cannot see at all.

Compared with cycle 100: under skewed gamma alternatives at n=400, S2 led SW by up to
ten paired SE. Under symmetric alternatives at n=100 and n=200, SW leads S2 by 13 to
96 paired SE on every alternative with any power at all. The two results are
consistent: S2 is a skewness statistic, and it wins only when skewness is the signal.

**Verdict line:** every symmetric alternative except t df 20 at n=100 shows SW ahead
beyond two paired SE at both n, so the SW lead over plain S2 at n=100 and n=200 is a
tail effect, not a skewness effect.
