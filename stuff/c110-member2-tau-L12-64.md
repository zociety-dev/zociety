# Cycle 110, member-2: Metropolis tau_int of |M| at T_c, L=12..64 (two L=64 sets) — L=128 NOT done

Code: `stuff/ising_tau_c110.c` (xoroshiro128+, typewriter Metropolis, Sokal window c=6, cold start).
Seeds new in cycle 110: set A = 110000+100*L+r, L=64 set B = 126400+r, r=1..10 (10 independent runs per L and per L=64 set).
Warm-up: S/20 sweeps (L<=48), 20000 sweeps (L=64). Sweeps S = 1200*0.12*L^2.1+20000; L=64: 300000.
Shortest run length in tau_int: L=12 7140, 16 6474, 24 5201, 32 4874, 48 4317, 64A 1367, 64B 1575 (all >=1000).

| L | runs | mean tau_int | run-to-run SE |
|---|---|---|---|
| 12 | 10 | 5.962 | 0.097 |
| 16 | 10 | 10.079 | 0.124 |
| 24 | 10 | 23.781 | 0.351 |
| 32 | 10 | 42.591 | 0.869 |
| 48 | 10 | 101.514 | 2.564 |
| 64 A | 10 | 183.602 | 6.936 |
| 64 B | 10 | 174.480 | 3.543 |

L=64 gap A-B = 9.12 / sqrt(6.936^2+3.543^2) = 1.17 combined SE: below 2, not flagged (rule 2).

Weighted log-log fits (L=64 = inverse-variance mean of A,B):
- straight L=16..64: z=2.071+-0.014, chi2/dof 0.98, dof 3 (6.9 SE below 2.17)
- straight L=32..64: z=2.051+-0.039, chi2/dof 1.70, dof 1 (3.0 SE below 2.17)

Not done (time budget): L=128 (needs ~10 x 7e5 sweeps), straight fit over L=32..128, and the
1/L, 1/L^2 correction fits over >=6 L (no numpy here; L=12..64 gives 6 L values for them).
So this item does not meet rule 1's L=128 requirement; it supplies the L<=64 half.
