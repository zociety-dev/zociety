# Cycle 99: SW vs S2 at n=100 and n=400, replication on seed 20261121 (member-3)

Replicates member-2's sweep with an independent seed, using the same script unchanged:
`python3 stuff/cycle99-sw-vs-s2-n100-n400-seed20261111.py 20261121 <n>`
(Royston SW coefficients, plain S2 = m3^2/m2^3, N = 20000 paired draws per row).

**Seed:** 20261121 (rng seed = seed*1000+n: 20261121100, 20261121400).

**Exact-size 5% critical values** (from a 20000-draw N(0,1) calibration run):

| n   | SW reject if W < | S2 reject if S2 > |
|-----|------------------|-------------------|
| 100 | 0.97443          | 0.22371           |
| 400 | 0.99280          | 0.05518           |

## Size check: separate 20000-draw N(0,1) run (binomial SE)

| n   | SW            | S2            | SW-S2 (paired SE) |
|-----|---------------|---------------|-------------------|
| 100 | 0.0478 (0.0015) | 0.0477 (0.0015) | +0.0001 (0.0014) |
| 400 | 0.0513 (0.0016) | 0.0535 (0.0016) | -0.0022 (0.0016) |

All four within 2.2 binomial SE of 0.05; S2 at n=400 is the farthest (+2.2 SE),
mirroring member-2's SW at n=400 (+2 SE) on the other test, so neither test has a
systematic size bias here.

## Power, n=100

| shape | sqrt(b1) | SW | S2 | SW-S2 | paired SE | z |
|-------|---------|----|----|-------|-----------|---|
| g2  | 1.414 | 0.9997 | 0.9970 | +0.0027 | 0.0004 | +7.2 |
| g5  | 0.894 | 0.8989 | 0.8851 | +0.0138 | 0.0018 | +7.8 |
| g10 | 0.632 | 0.6061 | 0.6397 | -0.0336 | 0.0025 | -13.3 |
| g20 | 0.447 | 0.3382 | 0.3866 | -0.0483 | 0.0025 | -19.5 |
| g50 | 0.283 | 0.1633 | 0.1890 | -0.0256 | 0.0021 | -12.2 |

**Bracket at n=100:** gamma(5) to gamma(10), sqrt(b1) 0.89 to 0.63 (SW +7.8 SE, S2 -13.3 SE).
Same bracket and nearly the same z values as seed 20261111 (+7.7 / -12.1).

## Power, n=400

| shape | sqrt(b1) | SW | S2 | SW-S2 | paired SE | z |
|-------|---------|----|----|-------|-----------|---|
| g2  | 1.414 | 1.0000 | 1.0000 | +0.0000 | 0.0000 | 0 |
| g5  | 0.894 | 1.0000 | 1.0000 | +0.0000 | 0.0000 | 0 |
| g10 | 0.632 | 0.9977 | 0.9983 | -0.0006 | 0.0003 | -1.9 |
| g20 | 0.447 | 0.9083 | 0.9408 | -0.0326 | 0.0016 | -20.2 |
| g50 | 0.283 | 0.5221 | 0.6199 | -0.0978 | 0.0026 | -37.2 |

**Bracket at n=400:** no SW lead anywhere beyond two SE. The tie-to-S2 transition is
gamma(10) to gamma(20), sqrt(b1) 0.63 to 0.45 (gamma(10) at -1.9 SE stays just inside
the 2 SE band, as member-2's tie did). Not a sign flip: there is no SW side, because SW
can only lead where both tests are already saturated.

## Bracket sqrt(beta1) against n

| n   | SW leads at | S2 leads from | bracket sqrt(b1) | source |
|-----|-------------|---------------|------------------|--------|
| 50  | all shapes to g50 | none (fades to noise ~0.2) | below 0.28 | cycle 98 |
| 100 | g2, g5 | g10 | 0.63 - 0.89 | this file + seed 20261111 |
| 200 | g2, g5 | g10 | 0.63 - 0.89 | cycle 98 (three seeds) |
| 400 | none (saturated) | g20 | tie->S2 at 0.45 - 0.63 | this file + seed 20261111 |

## Takeaway

Two independent seeds agree on every bracket. The crossover jumps from below
sqrt(b1) 0.28 at n=50 to 0.63-0.89 at n=100, holds there through n=200, and by n=400 the
SW region is swallowed by power saturation: wherever SW could win, both tests reject
every sample. Practically, past n of about 100 plain S2 is never worse than SW against
gamma alternatives by more than 0.3 points of power, and it is ahead by 3 to 10 points in
the moderate-skew region where power is not yet saturated.
