# Cycle 83: bound the top-3 share or the 1/Phi weight (member-1)

Follow-up to stuff/cap-power-replication.md, which found that capping the single
largest term cannot restore var/mean^2 <= 2/3 under t(3). Here two different bounds
are tried. Seed 83101, 2000 sims per n, n = 25, 50, 100, normal and t(3) data.

Cap rules (as numbers, rule 1):
- **top3_50**: the three largest AD terms together are capped at 0.50 of the AD sum.
- **wfloor3**: Phi(z) is floored at Phi(-3) = 0.00135 (ceiling 1 - that), so the
  1/Phi weight is at most ~741.

Power = rejection under t(3) at the normal-calibrated 0.95 critical value, so
normal rows reject at 0.050 by construction; "d" is capped minus uncapped power.
top1% = mean share of the largest term in the top 1% of sims; hit = fraction of
samples where the bound bound (rule 2).

```
law     n  version   mean     var/m2   p90    p95    p99    power  d       top1%  hit
normal  25 uncapped  0.035     0.476   0.062  0.079  0.121  0.050  +0.000  0.55  0.000
normal  25 top3_50   0.031     0.375   0.056  0.067  0.095  0.050  +0.000  0.22  0.495
normal  25 wfloor3   0.034     0.385   0.062  0.079  0.105  0.050  +0.000  0.31  0.025
normal  50 uncapped  0.027     0.711   0.046  0.056  0.086  0.050  +0.000  0.53  0.000
normal  50 top3_50   0.025     0.331   0.045  0.054  0.080  0.050  +0.000  0.20  0.086
normal  50 wfloor3   0.026     0.323   0.044  0.054  0.077  0.050  +0.000  0.16  0.082
normal 100 uncapped  0.019     0.437   0.033  0.041  0.062  0.050  +0.000  0.18  0.000
normal 100 top3_50   0.019     0.341   0.033  0.040  0.060  0.050  +0.000  0.09  0.025
normal 100 wfloor3   0.019     0.336   0.032  0.039  0.059  0.050  +0.000  0.07  0.206
t3      25 uncapped  0.516    51.379   0.301  0.812  11.41  0.378  +0.000  0.99  0.000
t3      25 top3_50   0.077     1.011   0.165  0.223  0.398  0.378  +0.000  0.40  0.475
t3      25 wfloor3   0.083     0.790   0.171  0.224  0.361  0.376  -0.002  0.17  0.348
t3      50 uncapped  3135.4   404.556  0.996  13.71  12418  0.593  +0.000  1.00  0.000
t3      50 top3_50   0.103     1.173   0.221  0.311  0.590  0.582  -0.011  0.47  0.306
t3      50 wfloor3   0.087     0.854   0.178  0.245  0.423  0.560  -0.033  0.07  0.702
t3     100 uncapped  111081    20.363  150.4  2.4e5  2.5e6  0.841  +0.000  0.99  0.000
t3     100 top3_50   0.154     1.155   0.329  0.472  0.821  0.847  +0.006  0.45  0.377
t3     100 wfloor3   0.110     0.815   0.215  0.302  0.483  0.830  -0.011  0.03  0.943
```

## Reading

- Both bounds remove single-draw dominance: the t(3) top-1% largest-term share
  falls from 0.99/1.00 to 0.40/0.47 (top3_50) and 0.17/0.07 (wfloor3) at n=25/50,
  and var/mean^2 drops from 51 and 405 to about 1. That is a factor 50-400, far
  more than any single-term cap achieved.
- Neither reaches 2/3 under t(3): best is wfloor3 at 0.79 (n=25) and 0.85 (n=50).
  The residual excess is now spread over many terms, not one draw, so it is a
  property of t(3) itself rather than of the weight blow-up.
- Power: top3_50 stays within 0.02 at every n (+0.000, -0.011, +0.006). wfloor3
  loses 0.033 at n=50, outside tolerance, because the floor binds in 70% of t(3)
  samples and flattens the very terms that detect the heavy tail.
- On normal data both bounds also pull n=50 var/mean^2 from the marginal 0.71
  (above 2/3 on this seed, consistent with cycle 82's 0.62-0.92) to 0.33, so the
  ncx2 ceiling becomes comfortably met at the Gaussian limit.
- Answer for this cycle: no bounded variant meets both clauses. top3_50 keeps
  power and gets within a factor ~1.6 of the ceiling; a floor looser than Phi(-3)
  (e.g. Phi(-4)) is the next thing to try to keep wfloor's moment gain without
  its power loss. Single seed; the n=50 wfloor3 loss should be replicated.

Files: stuff/cap-weight-floor.py (reproduces everything in ~1s),
stuff/cap-weight-floor.csv (one row per law, n, version).
