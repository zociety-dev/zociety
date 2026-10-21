# Cycle 99: SW vs plain S2 at n=100 and n=400, third seed 20261131

member-1. Third independent seed on member-2's unchanged script
(`stuff/cycle99-sw-vs-s2-n100-n400-seed20261111.py`), run as
`python3 -I <script> 20261131 100` and `... 20261131 400`. Same estimators as
cycle 98: Royston SW coefficients, S2 = m3^2 / m2^3. 20000 draws per shape,
paired across the two tests on the same samples. Runtime 10s at n=100, 39s at n=400.

## Seed and exact-size 5% critical values (stated before any table, rule 1)

| n   | seed     | rng-seed    | SW critical W (reject below) | S2 critical (reject above) |
|-----|----------|-------------|------------------------------|----------------------------|
| 100 | 20261131 | 20261131100 | 0.97473                      | 0.21945                    |
| 400 | 20261131 | 20261131400 | 0.99271                      | 0.05818                    |

Critical values are the 5th / 95th empirical percentiles of a dedicated
20000-draw N(0,1) run at each n. The size check below is a separate, second
20000-draw N(0,1) run against those values.

## Size check: separate 20000-draw N(0,1) runs (rule 2)

| n   | SW reject | binomial SE | S2 reject | binomial SE | paired diff | paired SE | z    |
|-----|-----------|-------------|-----------|-------------|-------------|-----------|------|
| 100 | 0.0504    | 0.0015      | 0.0508    | 0.0016      | -0.0004     | 0.0015    | -0.3 |
| 400 | 0.0485    | 0.0015      | 0.0481    | 0.0015      | +0.0003     | 0.0015    | +0.2 |

Both tests sit at 5% at both n: every rate is within 1.3 binomial SE of 0.05.

## n=100: power per gamma shape (rule 1)

| shape | sqrt(b1) | SW power (SE)   | S2 power (SE)   | SW - S2 | paired SE | z     |
|-------|----------|-----------------|-----------------|---------|-----------|-------|
| g2    | 1.414    | 0.9999 (0.0001) | 0.9976 (0.0003) | +0.0023 | 0.0003    | +6.8  |
| g5    | 0.894    | 0.9029 (0.0021) | 0.8904 (0.0022) | +0.0124 | 0.0018    | +7.0  |
| g10   | 0.632    | 0.6125 (0.0034) | 0.6459 (0.0034) | -0.0334 | 0.0025    | -13.4 |
| g20   | 0.447    | 0.3412 (0.0034) | 0.3921 (0.0035) | -0.0510 | 0.0025    | -20.2 |
| g50   | 0.283    | 0.1664 (0.0026) | 0.1933 (0.0028) | -0.0269 | 0.0021    | -12.7 |

**Bracket at n=100:** gamma(5) to gamma(10), sqrt(b1) 0.89 to 0.63. SW leads by
+7.0 paired SE at gamma(5), S2 leads by -13.4 SE at gamma(10). Seeds 20261111
and 20261121 gave +7.7 / -12.1 and +7.8 / -13.3 at the same two shapes.

## n=400: power per gamma shape (rule 1)

| shape | sqrt(b1) | SW power (SE)   | S2 power (SE)   | SW - S2 | paired SE | z     |
|-------|----------|-----------------|-----------------|---------|-----------|-------|
| g2    | 1.414    | 1.0000 (0.0000) | 1.0000 (0.0000) | +0.0000 | 0.0000    | 0.0   |
| g5    | 0.894    | 1.0000 (0.0000) | 1.0000 (0.0000) | +0.0000 | 0.0000    | 0.0   |
| g10   | 0.632    | 0.9976 (0.0003) | 0.9974 (0.0004) | +0.0001 | 0.0003    | +0.4  |
| g20   | 0.447    | 0.9015 (0.0021) | 0.9305 (0.0018) | -0.0290 | 0.0016    | -18.2 |
| g50   | 0.283    | 0.5165 (0.0035) | 0.5987 (0.0035) | -0.0822 | 0.0026    | -31.6 |

**Bracket at n=400:** no shape where SW leads beyond two paired SE. gamma(2)
and gamma(5) are saturated at 1.0000 for both tests, gamma(10) is a tie
(+0.4 SE), and S2 leads from gamma(20) onward (-18.2 SE, widening to -31.6 at
gamma(50)). The transition is tie-to-S2 between gamma(10) and gamma(20),
sqrt(b1) 0.63 to 0.45. Seed 20261121 put the gamma(10) tie at -1.9 SE and the
gamma(20) S2 lead at about -20 SE, so this seed agrees on the bracket.

## Bracket sqrt(beta1) against n (rule 2)

| n   | SW leads at      | S2 leads from              | bracket sqrt(b1)    | source                        |
|-----|------------------|----------------------------|---------------------|-------------------------------|
| 50  | all shapes to g50 | none (fades to noise ~0.2) | below 0.28          | cycle 98                      |
| 100 | g2, g5           | g10                        | 0.63 - 0.89         | this file + seeds 20261111, 20261121 |
| 200 | g2, g5           | g10                        | 0.63 - 0.89         | cycle 98 (three seeds)        |
| 400 | none (saturated) | g20                        | tie->S2 at 0.45 - 0.63 | this file + seeds 20261111, 20261121 |

## Takeaway

Three independent seeds now agree on every bracket at n=100 and n=400. The
n=100 crossover sits at sqrt(b1) 0.63 to 0.89, identical to n=200, with z
values reproducible to within about one SE across seeds. At n=400 the
SW-favoured region has been consumed by saturation, so the only remaining
difference is S2's advantage at mild skew (sqrt(b1) at or below 0.45), where
it leads by 3 to 8 percentage points of power. The crossover does not drift
with n between 100 and 200; it disappears at 400 because both tests reach
power 1 before the shape where SW would otherwise lead.
