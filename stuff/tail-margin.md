# How big a fixed tail margin would the pooled floor need?

This is for the cycle 67 direction: should the floor add a fixed tail margin,
wait for a larger pool, or switch tests? Here I work out the margin option
analytically, at the population level, for the three heavy tails that
cycle 66 simulated.

## Setup

The floor fits a lognormal to log outages and sets its p99 at
`mu_hat + 2.326 * sd_hat` in log space. When the true tail is heavier, the
true log-p99 sits above that line. The **gap** is the margin, in units of the
fitted sd, that you would have to add to recover the true p99.

| true log-tail                   | sd of log (units of scale s) | fitted p99 | true p99 | gap (s) | gap (fitted sd) |
|---------------------------------|------------------------------|------------|----------|---------|-----------------|
| normal (lognormal)              | 1.000                        | 2.326      | 2.326    | 0       | 0               |
| log-t df=5                      | sqrt(5/3) = 1.291            | 3.003      | 3.365    | 0.36    | **0.28**        |
| log-t df=3                      | sqrt(3) = 1.732              | 4.029      | 4.541    | 0.51    | **0.30**        |
| 10% mixture at 3x sd            | sqrt(0.9+0.9) = 1.342        | 3.121      | ~3.85    | 0.73    | **0.54**        |

The mixture p99 comes from solving `0.9*Phi(x) + 0.1*Phi(x/3) = 0.99`.
Phi(3.8) gives 0.98968 and Phi(3.9) gives 0.99028, so x is about 3.85.

## What this says

- For the log-t tails a margin of about **0.3 fitted sd** is enough, and it
  barely changes between df=5 and df=3. The fitted sd grows with the tail,
  so the sd soaks up most of the extra weight.
- The mixture needs almost twice that, **about 0.55 fitted sd**. Contamination
  in a small fraction of the data is the hard case. Anderson-Darling flagged it
  only 46% of the time.
- On a lognormal pool, a 0.55 sd margin moves the floor from z=2.326 to
  z=2.876. That is a p99.8 floor instead of p99. Rule 1 judges a fix by the
  floor's p99 against tolerance, so whether this overshoot is acceptable
  depends on whether that tolerance is one-sided.

## What this does not cover

- Sampling noise at n=50 is left out. `sd_hat` itself varies by about
  ±10% (1/sqrt(2n)), and heavy tails make that worse. A simulated margin will
  come out larger than these population numbers.
- I did not check this against rule 1's tolerance value. These are gaps, not
  pass/fail results.
- I did not compare the margin with "wait for a larger pool" or with a
  different test (rule 2).

Next step: simulate n=50 pools from each row and add margin m in
{0.3, 0.55}. Report the floor's simulated p99 against rule 1's tolerance,
using the same harness as the cycle 66 Anderson-Darling run.
