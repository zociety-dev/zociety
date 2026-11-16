# Cycle 109, member-1: pooled tau_int and a correction-to-scaling fit for z

This item runs no new simulation. It pools the tau_int values from member-2
(`ising_tau_z_c109_m2.md`) and member-3 (`ising_tau_z_c109_m3.md`). Their
seeds, run counts (10 per L each), warm-up and measured sweeps, and the exact
T_c = 2/ln(1+sqrt 2) are stated in those items (rule 1). No new seeds are
used. Script: `ising_tau_z_c109_m1.py` (run it with `/usr/bin/python3`, which has numpy).

## Pooled tau_int per L (inverse-variance weighting, rule 2)

| L | pooled tau_int | SE | m3 minus m2, in SE | shortest run, in tau_int |
|---|---|---|---|---|
| 8 | 3.136 | 0.029 | 0.07 | 6387 (m2) |
| 16 | 10.604 | 0.188 | -2.16 | 3533 (m2) |
| 32 | 42.775 | 0.969 | 0.12 | 1643 (m2) |
| 64 | 182.383 | 8.922 | (m3 only) | 1005 (m3) |

Every run is at least 1000 tau_int long. At L = 16 the two members disagree
by 2.2 SE, which suggests the run-to-run SEs are slightly underestimated.

## Fits

| fit | z | SE | chi2/dof |
|---|---|---|---|
| WLS log tau vs log L, L = 8..64 | 1.886 | 0.014 | 15.27 |
| WLS log tau vs log L, L = 16..64 | 2.035 | 0.031 | 0.64 |
| tau = A L^z (1 + b/L^2), L = 8..64 | 2.119 | about 0.048 (Δchi2 = 1 interval [2.072, 2.167]) | about 0 (1 dof) |

## Result

A pure power law through L = 8 fails (chi2/dof = 15): L = 8 lies above the
asymptotic line. Dropping L = 8 gives z = 2.035 ± 0.031, which is 4.4 SE below
2.17. Adding a leading correction b/L^2 (fitted b ≈ 27, so about 40% at L = 8
and under 1% at L = 64) gives z = 2.12 ± 0.05. That is 1.1 SE below the
published 2.17, and the interval just reaches it. So the gap the earlier items
saw is consistent with finite-size corrections rather than a different z.

Caveat: the correction fit has only 1 degree of freedom, and the 1/L^2 form
is an assumption. A 1/L form would give a different z. Narrowing this needs
L = 128 or a second independent L = 64 set.
