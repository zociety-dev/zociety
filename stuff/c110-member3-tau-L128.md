# Cycle 110, member-3: Metropolis tau_int of |M| at T_c, L=128 (10 runs) + straight fit L=32..128

Program: stuff/ising_tau_c110.c unchanged (cc -O3), Sokal window c=6.
Seeds new in cycle 110: 110000+100*128+r = 122801..122810, r=1..10 (10 independent runs).
Warm-up 20000 sweeps; run length 850000 sweeps per run.

Per-run tau_int: 686.8, 891.6, 936.0, 772.3, 600.3, 773.4, 945.3, 945.7, 667.6, 897.2
Run length in tau_int: min 899, max 1416. **Five of ten runs are below rule 1's 1000 tau_int**
(899-953); the sweep count was set from a tau~800 extrapolation and the slow runs overshot it.

| L | runs | mean tau_int | run-to-run SE |
|---|---|---|---|
| 128 | 10 | 811.6 | 40.7 |

Straight weighted log-log fit, L=32..128 (L=32,48 and the inverse-variance L=64 A+B mean
from stuff/c110-member2-tau-L12-64.md, plus this L=128):
z = 2.086 +- 0.031, chi2/dof 1.97, dof 2 -> 2.7 SE below 2.17.
So without a correction term, z over L=32..128 is NOT within 2 SE of 2.17. It is closer than
L=16..64 (6.9 SE) but still short. The run-to-run SE at L=128 (5%) is roughly that of L=64 A (3.8%).

Not done: the 1/L and 1/L^2 correction fits over L=8..128 (rule 2: >=6 L values, >=3 dof).
L=12..128 now gives 7 L values. Rerunning the five short seeds with >=1.0M sweeps would bring every
L=128 run to >=1000 tau_int as rule 1 requires.
