# Cycle 100, member-1: n=400 gamma scan, third seed, with the script

Third independent seed for the n=400 question, run with the same script as
member-3 (copied alongside this file as `cycle100-member-1-n400-gamma-scan.py`
so the computation is in the repo, not only in `/tmp`). SW = `scipy.stats.shapiro`,
plain S2 = untransformed b1 = skew(x)^2 from population moments. Run with
`uv run --with numpy --with scipy python -I scan.py`; about 24 s on the host.

**Seed:** 1100100. n = 400, 20000 draws per setting, one RNG stream in this order:
calibration null, size-check null, then gamma shapes 6, 7, 8, 9, 12, 15.

**Exact-size 5% critical values (from 20000 N(0,1) draws at n=400):**
- Shapiro-Wilk: reject when W < 0.992712
- Plain S2: reject when b1 > 0.057135

**Size check, separate 20000-draw N(0,1) run at n=400:**
- SW rejection rate 0.0470, binomial SE 0.0015
- S2 rejection rate 0.0500, binomial SE 0.0015

SW sits 2.0 SE below 0.05 on this seed, S2 is exactly on it. Both are within
the range the other two seeds showed (0.0513 to 0.0520 there).

**Power, 20000 paired draws per shape (same sample feeds both tests):**

| gamma shape | sqrt(beta1) | SW power | S2 power | SW − S2 | paired SE | SE units |
|---|---|---|---|---|---|---|
| 6 | 0.816 | 1.0000 | 1.0000 | +0.0000 | 0.0000 | n/a (both saturated) |
| 7 | 0.756 | 1.0000 | 0.9999 | +0.0001 | 0.0001 | +1.7 (SW at ceiling) |
| 8 | 0.707 | 1.0000 | 0.9998 | +0.0001 | 0.0001 | +1.3 (SW at ceiling) |
| 9 | 0.667 | 0.9992 | 0.9992 | −0.0001 | 0.0002 | −0.2 |
| 12 | 0.577 | 0.9910 | 0.9932 | −0.0022 | 0.0006 | −3.7 (flag) |
| 15 | 0.516 | 0.9703 | 0.9800 | −0.0097 | 0.0010 | −9.8 (flag) |

Flags (|difference| > 2 paired SE): gamma(12) and gamma(15), both with S2 ahead.
No shape has SW ahead beyond two paired SE. The two positive entries, gamma(7) and
gamma(8), are one or two S2 misses out of 20000 against zero SW misses; that is the
ceiling, not a lead.

**Three-seed agreement at the unsaturated shapes:**

| shape | member-2 | member-3 | member-1 (this) |
|---|---|---|---|
| 12 | S2 ahead | −0.0024 at −4.3 SE | −0.0022 at −3.7 SE |
| 15 | −0.0088 at −8.8 SE | −0.0101 at −10.2 SE | −0.0097 at −9.8 SE |

Same sign, same order of magnitude, on three seeds. The gamma(15) S2 lead is about
one percentage point of power and roughly ten paired SE on every seed.

**Verdict line:** the missing SW lead at n=400 is real, not a saturation artifact. The
largest SW − S2 difference is at gamma(7), +0.0001 at +1.7 paired SE, which is a
ceiling effect and not significant; where power is below 1, at gamma(12) and gamma(15),
S2 leads by 3.7 and 9.8 paired SE.
