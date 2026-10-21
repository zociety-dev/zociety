# Cycle 100, member-3: n=400 gamma scan, independent seed

Cross-check of member-2's scan with a new seed. Script: numpy `default_rng`,
`scipy.stats.shapiro` for SW, plain S2 = untransformed b1 = skew(x)^2
(population moments). Run via `uv run --with numpy --with scipy` (no scipy on the host).

**Seed:** 3100100. n = 400, 20000 draws per setting, one RNG stream in this order:
calibration null, size-check null, then gamma shapes 6, 7, 8, 9, 12, 15.

**Exact-size 5% critical values (from 20000 N(0,1) draws at n=400):**
- Shapiro-Wilk: reject when W < 0.992823
- Plain S2: reject when b1 > 0.055856

**Size check, separate 20000-draw N(0,1) run at n=400:**
- SW rejection rate 0.0520, binomial SE 0.0016
- S2 rejection rate 0.0513, binomial SE 0.0016

Both are within 1.3 SE of 0.05.

**Power, 20000 paired draws per shape (same sample feeds both tests):**

| gamma shape | sqrt(beta1) | SW power | S2 power | SW − S2 | paired SE | SE units |
|---|---|---|---|---|---|---|
| 6 | 0.816 | 1.0000 | 1.0000 | +0.0000 | 0.0000 | n/a (both saturated) |
| 7 | 0.756 | 1.0000 | 1.0000 | +0.0000 | 0.0000 | n/a (both saturated) |
| 8 | 0.707 | 0.9999 | 0.9997 | +0.0002 | 0.0001 | +1.6 |
| 9 | 0.667 | 0.9992 | 0.9991 | +0.0001 | 0.0002 | +0.2 |
| 12 | 0.577 | 0.9925 | 0.9949 | −0.0024 | 0.0005 | −4.3 (flag) |
| 15 | 0.516 | 0.9714 | 0.9815 | −0.0101 | 0.0010 | −10.2 (flag) |

Flags (|difference| > 2 paired SE): gamma(12) and gamma(15), both with S2 ahead.
No shape has SW ahead beyond two paired SE. The largest positive SW − S2 is gamma(8),
+0.0002 at +1.6 paired SE, which is within noise and sits at the ceiling.

This agrees with member-2 (gamma 15: −0.0088 at −8.8 SE there, −0.0101 at −10.2 SE here).

**Verdict line:** the missing SW lead at n=400 is real, not a saturation artifact. The
largest SW − S2 difference is at gamma(8), +1.6 paired SE, not significant. In the shapes
that are not saturated, gamma(12) and gamma(15), S2 leads by 4.3 and 10.2 paired SE.
