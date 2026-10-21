# Waiting for a larger pool vs a fixed tail margin

Cycle 67 direction: the heavier-tail check misses most moderate heavy tails at
n=50. `stuff/tail-margin.md` sized a fixed margin (about 0.3 fitted sd in log
space for log-t, about 0.55 for a 10% mixture at 3x sd). This file looks at the
other option: waiting for more data before the floor is set.

## What waiting buys

Anderson-Darling power grows roughly with sqrt(n) in the effect size it can
see. Cycle 66 measured power at n=50 as 30% (log-t df=5), 59% (df=3) and 46%
(mixture). A rough extrapolation, not a simulation:

| n   | log-t df=5 | log-t df=3 | 10% mixture 3x |
|-----|-----------|-----------|----------------|
| 50  | 30% (measured) | 59% (measured) | 46% (measured) |
| 100 | ~50%      | ~85%      | ~70%           |
| 200 | ~75%      | ~97%      | ~92%           |

Even at n=200, a df=5 tail gets past about one pool in four. Waiting reduces the
miss rate but does not remove it.

## What waiting costs

While the pool is below the larger n, there is no pooled floor and the fallback
floor stays in force. If outages arrive at about one pool entry per day, going
from n=50 to n=200 adds about five months on the fallback.

## Recommendation for a rule

Combine the two options instead of choosing one. Add the margin at n=50, then
shrink it as n grows:

    margin(n) = 0.55 * sqrt(50 / n)   (fitted log-sd units)

At n=200 that gives 0.275, close to the log-t margin alone. Rule 1 still
decides the question: the schedule is only acceptable if a simulation of the
gated floor keeps its p99 within tolerance at each n in {50, 100, 200}.

## Not yet done

- Every power figure above n=50 is extrapolated. It needs the cycle-66
  simulation re-run at n=100 and n=200.
- The sqrt(50/n) shrink rate is assumed, not fitted.
- The arrival rate of one entry per day is a placeholder.
