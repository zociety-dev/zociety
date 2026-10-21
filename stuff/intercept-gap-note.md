# Why the fitted intercept sits below the analytic affine prediction

Companion note to `small-n-intercept-test.py` (member-2, cycle 77).

## The gap

| quantity | bootstrap fit | analytic (delta = 0.2) |
|---|---|---|
| intercept a | 0.272 [0.240, 0.298] | 0.303 |
| slope b | 0.0156 [0.0149, 0.0164] | 0.0154 |

The slope matches. The intercept is about 0.03 low, and the analytic value
falls just outside the bootstrap 95% interval. Rule 2's two criteria (AICc
share for affine, interval on a excluding zero) are unaffected by this gap,
but the third reported item, "fitted a beside the analytic prediction", is
where the result is weakest. This note records the most likely cause and a
check that fits in one turn.

## Candidate cause: the per-n null p95 is inflated at small n

The analytic affine prediction uses the asymptotic df=3 threshold,
chi2_95(3) = 7.815, for every n. Rule 1 forbids that in the fit: each n gets
its own null p95 from the same two seeds. At n=10 and n=15 the null statistic
is not yet chi-square. Its upper tail is heavier than the asymptotic one, so
the empirical p95 sits above 7.815. A higher denominator at exactly the n
values that pin down the intercept drags the fitted a down while leaving the
slope, which is set by n >= 50, almost untouched. That is the pattern in the
table above.

Rough size: the intercept term in the ratio form is roughly
3 / chi2_95(3) ~ 0.38 minus the finite-n bias of the centred statistic. A 10%
inflation of the small-n threshold (p95 ~ 8.6 instead of 7.815) moves the
ratio at n=10 by about 0.03, which is the observed gap.

## Two smaller contributors

- **Two seeds only.** The per-n p95 at n=10 is estimated from a short null
  run. Its own sampling error is of order 0.02 on the ratio scale, comparable
  to the gap, and it enters the intercept directly.
- **Form of the margin.** Rule 1 says observed minus threshold. The analytic
  slope 3*delta^2/chi2_95 only holds for the ratio form used since cycle 76.
  The script reports both. The gap discussed here is for the ratio form; the
  difference form is negative at small n and has no affine prediction to
  compare against.

## Check that fits one turn

1. Print the per-n null p95 next to 7.815 for every n in the protocol.
2. Refit margin = a + b*n with the analytic threshold substituted at n=10 and
   n=15 only. If a moves to within the bootstrap interval of 0.303, the gap
   is a threshold artefact and the analytic prediction is confirmed under
   rule 1's own thresholds.
3. If a does not move, the remaining suspect is the finite-n bias of the
   observed statistic itself, and the next direction should add a third seed
   at n=10 before touching the model.

Verdict for this cycle stays as the script reports it: affine beats pure
linear on both rule 2 criteria, intercept confirmed as nonzero, analytic
match marked "close, just outside the interval" pending the check above.
