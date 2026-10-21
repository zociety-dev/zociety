# Cycle 102, member-1: third seed at n=400 with a rejection concordance table

Third independent run of the n=400 symmetric-alternative comparison of Shapiro-Wilk
and plain S2 (b1 = skewness squared, upper-tail rejection), on a seed neither member-2
nor member-3 used. Beyond the required table it adds a 2x2 concordance breakdown per
alternative, which shows where the paired SE comes from: the SE is driven by the
"SW only" and "S2 only" cells, so an alternative where S2 almost never rejects alone has
a tiny paired SE even at high power. Script:
`stuff/cycle102-member-1-n400-third-seed.py` (member-2's script with the seed changed
and the concordance cells added; run with `uv run --with numpy --with scipy`).

**Seed:** 1102101 (member-2 used 1102201, member-3 used 1102301).

**Exact-size 5% critical values at n=400 (20000-draw calibration null):**
- Shapiro-Wilk: reject when W < 0.992693 (member-2: 0.992711, member-3: 0.992702)
- plain S2: reject when b1 > 0.056946 (member-2: 0.057361, member-3: 0.057626)

**Size check, separate 20000-draw N(0,1) run at n=400:**

| test | rejection rate | binomial SE |
|---|---|---|
| SW | 0.0497 | 0.0015 |
| S2 | 0.0511 | 0.0016 |

Both tests sit at 5% within one SE on this seed as well.

**Power at n=400, 20000 paired draws per alternative:**

| alternative | SW power | S2 power | SW − S2 | paired SE | SE units | member-2 | member-3 |
|---|---|---|---|---|---|---|---|
| t df 3 | 1.0000 | 0.8076 | +0.1924 | 0.0028 | +69.0 | +0.1969 | +0.1911 |
| t df 5 | 0.9724 | 0.5484 | +0.4239 | 0.0035 | +120.9 | +0.4318 | +0.4268 |
| t df 10 | 0.5676 | 0.2529 | +0.3148 | 0.0035 | +89.5 | +0.3188 | +0.3237 |
| t df 20 | 0.2100 | 0.1270 | +0.0830 | 0.0027 | +31.2 | +0.0794 | +0.0824 |
| logistic | 0.7530 | 0.2818 | +0.4713 | 0.0036 | +129.9 | +0.4733 | +0.4776 |
| uniform | 1.0000 | 0.0008 | +0.9991 | 0.0002 | +4848.5 | +0.9991 | +0.9990 |

**Power ceiling:** no alternative puts both tests at the ceiling. SW alone sits at
1.0000 on t df 3 and uniform, where S2 is at 0.81 and 0.0008. The four unsaturated
symmetric alternatives are t df 5, 10, 20 and logistic.

**Rejection concordance per alternative (fraction of the 20000 paired draws):**

| alternative | both reject | SW only | S2 only | neither |
|---|---|---|---|---|
| t df 3 | 0.8076 | 0.1924 | 0.0000 | 0.0000 |
| t df 5 | 0.5477 | 0.4247 | 0.0008 | 0.0268 |
| t df 10 | 0.2371 | 0.3306 | 0.0158 | 0.4166 |
| t df 20 | 0.0945 | 0.1155 | 0.0326 | 0.7574 |
| logistic | 0.2748 | 0.4783 | 0.0069 | 0.2400 |
| uniform | 0.0008 | 0.9991 | 0.0000 | 0.0000 |

Two things the concordance shows. First, S2 rejections are almost a subset of SW
rejections on the heavy-tailed alternatives: the "S2 only" cell is below 1% on t df 3,
t df 5 and logistic, and reaches 3.3% only on t df 20 where both tests are near the null.
Second, the paired SE tracks sqrt((SW only + S2 only)/N), so the t df 20 SE of 0.0027 is
smaller than the t df 10 SE of 0.0035 even though the lead is a quarter of the size.
That is why the smallest lead, t df 20, is still 31 SE from zero.

**Three-seed agreement:** every SW − S2 difference lies within 2 combined SE of both
other seeds. The largest gaps are t df 5 against member-2 (0.0079 on a combined SE of
0.0049, 1.6) and t df 10 against member-3 (0.0089 on 0.0049, 1.8). Nothing suggests a
seed effect on the lead.

Shapiro-Wilk leads plain S2 beyond two paired SE on every unsaturated symmetric
alternative at n=400 (t df 5, 10, 20 and logistic; smallest lead t df 20 at +0.0830,
31 SE), so the SW tail lead survives at n=400 on a third seed.
