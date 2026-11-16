# Cycle 110: z fits with 1/L and 1/L^2 corrections over L=12..128 (member-1)

**Data:** no new simulation runs, so this item uses no new seeds. Every number comes from
`c110-member2-tau-L12-64.md` (L=12..64, plus the two L=64 sets A and B) and `c110-member3-tau-L128.md`
(L=128). Each L has 10 independent runs, and the SE is the run-to-run SE given in those files.
Both L=64 sets go into the fits as separate points. That gives 8 points over 7 distinct L values.
Script: `stuff/c110_zfit.py` (pure Python). For each z it solves the linear amplitude(s) by weighted least squares, then scans z
in steps of 1e-4. The quoted error is the range where chi2 stays within min+1.

Models: power `A L^z`; 1/L `A L^z (1 + b/L)`; 1/L^2 `A L^z (1 + b/L^2)`.

| fit | L range | points / distinct L | z | SE | chi2/dof | dof | b |
|---|---|---|---|---|---|---|---|
| power | 32..128 | 5 / 4 | 2.084 | 0.032 | 1.74 | 3 | – |
| power | 24..128 | 6 / 5 | 2.068 | 0.020 | 1.41 | 4 | – |
| power | 16..128 | 7 / 6 | 2.078 | 0.013 | 1.22 | 5 | – |
| power | 12..128 | 8 / 7 | 2.056 | 0.011 | 2.74 | 6 | – |
| 1/L | 12..128 | 8 / 7 | 2.160 | +0.055/-0.049 | 2.23 | 5 | 3.2 |
| 1/L^2 | 12..128 | 8 / 7 | 2.113 | 0.026 | 2.02 | 5 | 17.7 |
| 1/L | 16..128 | 7 / 6 | 2.067 | +0.062/-0.056 | 1.51 | 4 | -0.3 |
| 1/L^2 | 16..128 | 7 / 6 | 2.065 | 0.035 | 1.48 | 4 | -4.9 |

**Rule 2 check (L=64 gap):** set A has 183.60 +- 6.94 and set B has 174.48 +- 3.54. The gap is 9.12 and the
combined SE is 7.79, so the gap is **1.17 SE**. That is below the 2 SE flag, so this pair gives no evidence
that the SEs are too small. All correction fits use at least 6 L values and have at least 4 dof.

## Answers to the cycle question
1. **Straight power law over L=32..128:** z = 2.084 +- 0.032. That is 2.7 SE below 2.17, so it is
   **not within 2 SE** (this matches member-3's result).
2. **1/L and 1/L^2 forms over the widest range available (L=12..128; there is no L=8 in cycle 110):** z = 2.160 +- 0.052
   and z = 2.113 +- 0.026. They differ by 0.047, which is 0.8 of their combined SE, so **they agree within
   their SEs**. Both fits use the same data, so this agreement is weaker than it looks. Compared with 2.17,
   the 1/L fit is 0.2 SE low and the 1/L^2 fit is 2.2 SE low.
3. **Caveat:** the correction fits depend on including L=12. If L=12 is dropped (L=16..128), both correction
   amplitudes come out consistent with zero and both forms give z of about 2.066 +- 0.035 to 0.06. That is still 1.7 to 3 SE
   below 2.17. So the correction terms are driven by a single lattice, and chi2/dof of about 2 at L>=12 shows
   neither form describes L=12 well. The shortfall from 2.17 is not settled by this data. Two things would
   narrow it: an L=256 point, or reruns of the five short L=128 seeds at >=1.0M sweeps.
