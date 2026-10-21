# Option 3: switch to a more tail-sensitive test

Covers the third option in this cycle's direction question. `stuff/tail-margin.md` covers the fixed margin, and `stuff/pool-wait.md` covers waiting for a larger pool.

## What rule 2 asks for

A replacement test has to clear two bars. Both are simulated at n=50:
1. Calibrated to a 5% false-alarm rate, it flags log-t df=5 tails more than 30% of the time. 30% is Anderson-Darling's power from cycle 66.
2. The floor it gates keeps its p99 within rule 1's tolerance.

## Candidates

| test on log outages | why it might beat AD on tails | expected df=5 power at n=50 |
|---|---|---|
| upper-tail-weighted AD (weight 1/(1-F)) | puts all its weight on the right tail, which is where the floor's p99 comes from | ~40% (estimate) |
| sample kurtosis (one-sided) | measures tail weight directly | ~35% (estimate) |
| Hill-type tail-index check on top 10 | looks only at the extreme order statistics | ~25% (estimate; 10 points are noisy) |

None of these power figures are measured. They are guesses from how the tests are built and have to be simulated with the cycle 66 harness before anyone cites them.

## Why switching alone is not enough

Say a test reaches 40%. It still lets 60% of df=5 pools through as lognormal. Rule 1 judges the floor's p99, not the test's pass rate. So a better test only shrinks the number of bad pools that reach the floor. It does not keep their p99 within tolerance.

## Proposal

Use the upper-tail-weighted AD as the gate **and** keep the margin from `stuff/pool-wait.md`, `0.55·sqrt(50/n)`. The tighter gate catches more heavy pools. The margin covers the ones that still pass. If the new test clears rule 2's first bar, the margin could then be re-tuned smaller, but only once rule 1's p99 simulation shows the combination stays within tolerance.

## Still to simulate

- Calibrated power of the three candidates on df=5, df=3 and the 10% mixture, at n=50.
- The floor's p99 under the weighted-AD gate plus margin, compared with AD plus margin.
