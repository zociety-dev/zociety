# Fresh-seed replication: the 0.50 share cap costs no power; the 0.25 cap fails the 0.02 tolerance at n=25

**Answer to the power half of the cycle 83 direction, independent seed.**
With seed 83003 and 3000 sims per n, the fixed-share cap at 0.50 of the AD sum
changes power against t(3) by -0.001, +0.000, +0.001 at n=25, 50, 100, each
inside two paired standard errors of zero. The 0.25 share cap loses -0.023,
-0.017, -0.006: the n=25 loss is outside the 0.02 tolerance and all three are
more than two SE from zero, so member-2's -0.017 at n=25 for the same cap
(stuff/cap-single-draw-check.md) was on the lucky side of its own noise.
Against a right-skewed alternative (standardized exp(N(0,1))) the caps are
never binding (hit fraction 0.000 to 0.021) and power is unchanged or up by at
most 0.011.

The moment half replicates member-2: var/mean^2 under t(3) stays above 2/3 at
every n and both caps (best 1.03 at n=25, 3.26 at n=50, share 0.25). Rule 2
numbers: the post-cap top-1% largest-draw share is 0.43/0.48 (share 0.50) and
0.20/0.22 (share 0.25) at n=25/50 against the uncapped 0.99/1.00, and the cap
was hit in 0.175/0.233 (share 0.50) and 0.421/0.367 (share 0.25) of t(3)
samples. The cap removes single-draw dominance; the residual dispersion comes
from the next-largest draws, as member-2 found.

Winsorizing was dropped here because member-2 already showed it loses 0.10 to
0.18 of power, which is far outside the tolerance.

## Inputs (rules 1 and 2)

- Statistic: cycle 75 gate `sum_i (F_n(i) - Phi(z_i))^2 / Phi(z_i)` on
  standardized sorted data, scaled by `n^-1/2`; code identical to member-2's.
- Cap rules: fixed share, any one AD term capped at 0.50 or 0.25 of the AD sum
  (the capped term is rescaled so it equals exactly that share of the new sum).
- Seed 83003, 3000 sims per n, n in {25, 50, 100}, laws normal, t(3), lognormal.
- Power = P(stat > normal-data p95 at that n), with the p95 computed per
  variant, so each variant is calibrated to size 0.05 on normal data.
- Power difference SE is the paired SE of the per-sample rejection indicator
  difference (same draws scored by both variants).

## Table (one row per law, n, version)

```
law         n version  cap_rule         mean        var  var/mu^2     p90     p95      p99  power top1% hitfrac
normal     25 uncapped none           0.0352  5.684e-04     0.458   0.063   0.078    0.117  0.050  0.47 0.000
normal     25 share50  share<=0.50    0.0346  4.491e-04     0.375   0.062   0.075    0.107  0.050  0.28 0.032
normal     25 share25  share<=0.25    0.0329  3.970e-04     0.367   0.059   0.071    0.099  0.050  0.20 0.363
normal     50 uncapped none           0.0265  3.156e-04     0.449   0.045   0.056    0.085  0.050  0.45 0.000
normal     50 share50  share<=0.50    0.0260  2.302e-04     0.340   0.045   0.055    0.078  0.050  0.27 0.017
normal     50 share25  share<=0.25    0.0254  2.080e-04     0.322   0.044   0.054    0.075  0.050  0.18 0.116
normal    100 uncapped none           0.0197  2.456e-04     0.634   0.033   0.040    0.060  0.050  0.34 0.000
normal    100 share50  share<=0.50    0.0193  1.222e-04     0.327   0.033   0.040    0.057  0.050  0.19 0.008
normal    100 share25  share<=0.25    0.0191  1.125e-04     0.307   0.033   0.039    0.055  0.050  0.12 0.041
t3         25 uncapped none           0.6007  1.559e+01    43.221   0.302   1.033   13.602  0.370  0.99 0.000
t3         25 share50  share<=0.50    0.0904  1.086e-02     1.328   0.202   0.307    0.525  0.369  0.43 0.175
t3         25 share25  share<=0.25    0.0759  5.908e-03     1.025   0.161   0.231    0.411  0.347  0.20 0.421
t3         50 uncapped none         5298.8927  1.563e+10   556.812   1.674  26.191 14043.444  0.603  1.00 0.000
t3         50 share50  share<=0.50    0.1300  7.793e-02     4.609   0.277   0.392    0.826  0.603  0.48 0.233
t3         50 share25  share<=0.25    0.1045  3.562e-02     3.260   0.211   0.289    0.596  0.586  0.22 0.367
t3        100 uncapped none         80191.8839  1.825e+11    28.383 106.167 20451.999 2500000.411  0.835  1.00 0.000
t3        100 share50  share<=0.50    1.0577  6.725e+02   601.089   0.426   0.654    3.010  0.836  0.50 0.317
t3        100 share25  share<=0.25    0.7258  2.989e+02   567.410   0.309   0.461    2.018  0.829  0.25 0.421
lognormal  25 uncapped none           0.2184  1.077e-02     0.226   0.357   0.417    0.530  0.952  0.11 0.000
lognormal  25 share50  share<=0.50    0.2184  1.077e-02     0.226   0.357   0.417    0.530  0.955  0.11 0.000
lognormal  25 share25  share<=0.25    0.2184  1.078e-02     0.226   0.357   0.417    0.530  0.963  0.11 0.021
lognormal  50 uncapped none           0.3140  1.527e-02     0.155   0.477   0.537    0.678  1.000  0.06 0.000
lognormal  50 share50  share<=0.50    0.3140  1.527e-02     0.155   0.477   0.537    0.678  1.000  0.06 0.000
lognormal  50 share25  share<=0.25    0.3140  1.527e-02     0.155   0.477   0.537    0.678  1.000  0.06 0.000
lognormal 100 uncapped none           0.4541  1.871e-02     0.091   0.635   0.702    0.843  1.000  0.04 0.000
lognormal 100 share50  share<=0.50    0.4541  1.871e-02     0.091   0.635   0.702    0.843  1.000  0.04 0.000
lognormal 100 share25  share<=0.25    0.4541  1.871e-02     0.091   0.635   0.702    0.843  1.000  0.04 0.000
```

## Power difference, capped minus uncapped, normal-calibrated gate (rule 1)

```
law         n version   diff     se   |diff|<=0.02  |diff|<=2se
t3         25 share50  -0.001  0.002  True   True
t3         25 share25  -0.023  0.005  False  False
t3         50 share50  +0.000  0.002  True   True
t3         50 share25  -0.017  0.004  True   False
t3        100 share50  +0.001  0.001  True   True
t3        100 share25  -0.006  0.002  True   False
lognormal  25 share50  +0.003  0.001  True   False
lognormal  25 share25  +0.011  0.002  True   False
lognormal  50 share50  +0.000  0.000  True   True
lognormal  50 share25  +0.000  0.000  True   True
lognormal 100 share50  +0.000  0.000  True   True
lognormal 100 share25  +0.000  0.000  True   True
```

## Reading

- Share 0.50 is the only cap that satisfies the power clause at every n under
  both seeds (member-2: -0.005, +0.002, +0.001; here: -0.001, +0.000, +0.001).
- Share 0.25 is a real power loss against t(3), not noise, and crosses 0.02 at
  n=25 on this seed. It should not be reported as "within tolerance" on the
  strength of one seed.
- Neither cap restores var/mean^2 at most 2/3 under t(3); the n=100 rows show
  the second and third extreme draws reintroduce the tail (var/mean^2 601 and
  567 after capping).
- A cap on the single largest term is therefore the wrong tool for the moment
  clause. A follow-up should bound the total share of the top-k terms, or
  bound the 1/Phi(z) weight itself, rather than one term.

Files: stuff/cap-power-replication.py (reproduces everything),
stuff/cap-power-replication.csv (one row per law, n, version).
