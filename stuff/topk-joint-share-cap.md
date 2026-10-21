# Joint share cap on the top k AD terms (cycle 84)

The winsorize sweep (stuff/topk-winsorize-sweep.md) ended by naming this as
the next probe: instead of moving draws, cap the k largest AD gate terms
*jointly* at half the total, leaving the draws, the standardization and the
other n-k terms untouched. k = 0 is the uncapped baseline, in the same table.

Seed 84003, 20000 sims per n per law (normal and t(3)), n = 25, 50, 100,
cap share C = 1/2. Power is P(stat > normal-data p95 of the same variant at
the same n) on t(3), the cycle 83 convention used by the other two items.
Script: stuff/topk-joint-share-cap.py (pure python, ~8 s); data:
stuff/topk-joint-share-cap.csv.

| n | k | var/mean^2 (t3) | top-1% share of top k | power (t3) | power - k0 | normal p95 |
|---|---|---|---|---|---|---|
| 25 | 0 | 46.97 | 0 | 0.3749 | +0.0000 | 0.07892 |
| 25 | 1 | 1.247 | 0.4634 | 0.3695 | -0.0054 | 0.07701 |
| 25 | 2 | 1.103 | 0.4502 | 0.3617 | -0.0132 | 0.07459 |
| 25 | 3 | 1.037 | 0.4382 | 0.3532 | -0.0217 | 0.07004 |
| 25 | 5 | 1.162 | 0.4749 | 0.3532 | -0.0217 | 0.05327 |
| 50 | 0 | 391.7 | 0 | 0.5861 | +0.0000 | 0.05774 |
| 50 | 1 | 3.617 | 0.4812 | 0.5821 | -0.0040 | 0.05672 |
| 50 | 2 | 1.299 | 0.4623 | 0.5825 | -0.0036 | 0.05583 |
| 50 | 3 | 1.236 | 0.4566 | 0.578 | -0.0081 | 0.0551 |
| 50 | 5 | 1.159 | 0.4488 | 0.5686 | -0.0174 | 0.05285 |
| 100 | 0 | 26.39 | 0 | 0.8317 | +0.0000 | 0.04099 |
| 100 | 1 | 6131 | 0.4985 | 0.8349 | +0.0032 | 0.04024 |
| 100 | 2 | 1.38 | 0.4692 | 0.834 | +0.0023 | 0.04009 |
| 100 | 3 | 1.106 | 0.4561 | 0.8333 | +0.0016 | 0.03995 |
| 100 | 5 | 1.066 | 0.4418 | 0.8322 | +0.0005 | 0.03964 |

## Verdict (rule 2)

- n = 25: none. Best is k=3 at 1.04, still above 2/3; k=3 and k=5 also lose
  0.022 power, outside 0.02.
- n = 50: none. Best is k=5 at 1.16 (power -0.017, inside 0.02).
- n = 100 (power only by the direction; var/mean^2 reported for context):
  none; k=5 gives 1.07.

No k reaches var/mean^2 at most 2/3 at any n. Unlike the winsorize sweep,
the joint share cap keeps power: every row is within 0.02 of uncapped except
k=3, 5 at n=25 (-0.022, about 1.5 SE of 0.0034 at 20000 sims).

## Where the excess lives

- In the top 1% of t(3) sims the capped top k still hold 0.42 to 0.48 of the
  statistic, i.e. the cap binds in essentially every extreme sim. The rest
  (n-k terms) carries the other half, and it is not small: var/mean^2 sits
  near 1.1 to 1.2 for k >= 2 and moves little from k=2 to k=5. The residual
  excess is spread across the bulk of the terms, consistent with cycle 83's
  "remaining terms, not the largest".
- k=1 is not enough: with only one term capped a second extreme draw keeps
  the tail (3.6 at n=50, 6131 at n=100 from a handful of sims with two huge
  terms). k >= 2 removes that.

## Caveats

- Capping is pointwise downward, so var/mean^2 can rise above uncapped (n=100,
  k=1) when the capped mean is much smaller than the outlier-driven uncapped
  mean; the n=100 uncapped value (26) is itself unstable at this sims count.
- One cap share (1/2) only; a lower C would bring the top k share down but
  cannot touch the n-k bulk, which already sits near var/mean^2 of 1 on its
  own, so lower C is unlikely to reach 2/3.
