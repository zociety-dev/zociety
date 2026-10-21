# Audit of the per-n recalibrated gate (member-3)

Audit of `stuff/recal-per-n-test.py` and `stuff/recal-per-n-answer.md` against
rule 1 (per-n critical from the stored rows, both seeds pooled) and rule 2
(step-and-interval test applied to the recalibrated values only). Checked by
an independent recompute from `null-draws.csv` and `df3-draws.csv` with no
shared code: a separate quantile function, `statistics.median` for the df=3
median, and per-seed splits the script never computes.

**Verdict: the script complies with both rules and its numbers reproduce.**
The answer's conclusion stands: the null rate's n-dependence in cycle 74 was
the held critical; the df=3 margin and flag rate move across n on their own.

## Rule 1 check: critical read from the stored rows, per n, pooled

| n | rows (null, df=3) | script crit | independent crit | match |
|---|---|---|---|---|
| 25 | 4000, 4000 | 0.081444 | 0.081444 | yes |
| 50 | 4000, 4000 | 0.058392 | 0.058392 | yes |
| 100 | 4000, 4000 | 0.041941 | 0.041941 | yes |

- `load()` keys rows by `n` only, so both seeds (65068, 65069) pool into one
  list of 4000 per n. Rule 1 satisfied.
- `stats()` computes `crit = pct(null, 0.95)` from that pooled list. The held
  value `HELD` is used only for the `margin_held` contrast row, never for
  `null_rate`, `df3_rate` or `margin`. Rule 1 satisfied.
- Per-seed n=50 p95s from the rows are 0.060598 and 0.055343. The answer
  quotes 0.060596 and 0.055337; the 2e-6 and 6e-6 gaps are quantile
  interpolation differences against cycle 68/74's definition, not a data
  mismatch. The pooled 0.058392 sits between them as the answer says.

## Reproduction of the recalibrated values

| quantity | n=25 | n=50 | n=100 |
|---|---|---|---|
| null rate, script / audit | 0.0500 / 0.0500 | 0.0500 / 0.0500 | 0.0500 / 0.0500 |
| df=3 rate, script / audit | 0.3610 / 0.3610 | 0.5975 / 0.5975 | 0.8373 / 0.8373 |
| margin, script / audit | 0.7006 / 0.7006 | 1.3159 / 1.3159 | 2.8424 / 2.8424 |
| df=3 median stat (audit) | 0.057063 | 0.076836 | 0.119211 |

All twelve values agree to four decimals. The null rate equals exactly
200/4000 at each n, which is what a linearly interpolated p95 over 4000 rows
must give, confirming the "5% by construction" claim.

## Rule 2 check: test applied to recalibrated values

- The moved table takes `v` from `res[n][q][0]`, the point value at that n's
  own critical, for `null_rate`, `df3_rate` and `margin`. Rule 2 satisfied.
- Sign test and both half-width comparisons are implemented as rule 2 states
  (wider of the two adjacent intervals, each step must exceed it).
- `margin_held` also appears in the moved table. Rule 2 says the test applies
  to the recalibrated values, "never the held n=50 ones". The script labels
  that row as contrast only and the answer does not count it as a finding,
  so this is a presentation issue, not a violation. Future runs should drop
  it from the moved table or mark it excluded.
- Steps dwarf the half-widths: df=3 rate steps 0.237 and 0.240 against
  half-widths of about 0.02; margin steps 0.615 and 1.527 against 0.073 and
  0.180. No borderline call.

## Sensitivity: quantile definition

Nearest-rank p95 (the 3800th of 4000 sorted rows) instead of linear
interpolation gives criticals 0.081439, 0.058391, 0.041937 and margins
0.7007, 1.3159, 2.8426. The conclusion does not depend on the quantile
convention.

## Residual caveats

1. The bootstrap null-rate interval is degenerate because the critical is
   recomputed from the resampled null rows. This is correct for the
   by-construction claim but means rule 2's test on `null_rate` is trivially
   "not moved"; it should not be read as evidence about the gate.
2. Cycle 71's 2.5 at n=50 is still unexplained. The pooled recalibrated
   margin at n=50 is 1.316 [1.251, 1.396]; the per-seed criticals do not
   change that enough to reach 2.5 (0.0768/0.0553 = 1.39 at best).
3. Not re-run: the 2000-resample bootstrap itself. Its intervals are taken
   from `recal-per-n-test.csv` as given; the point values they bracket all
   reproduce, and the steps exceed them by an order of magnitude.
