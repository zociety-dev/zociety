# Cycle 91: S2+A2 combinations (Bonferroni max-p, reject-if-either) vs plain AD vs Shapiro-Wilk, replication at seed 91404

Script: `stuff/s2a2-combo-vs-ad-vs-sw-seed91404.py` (run with `uv run --with numpy --with scipy python ...`, 25 s).
Seed 91404 (numpy default_rng) was not used in cycles 88-90, and differs from member-2's seed 91202.
Same estimator and design as member-2's item; this is an independent-seed replication so that each
verdict below can be checked against the 91202 run cell by cell.

## Definitions (before any table, per rule 1)

For a sample x_1..x_n, z = (x - mean)/sd with sd on n-1, z_(i) sorted. The Anderson-Darling term is

    t_i = -((2i-1)/n) * [ ln Phi(z_(i)) + ln(1 - Phi(z_(n+1-i))) ],  i = 1..n.

- **S2** = sum_i log(1 + 2 t_i) / 2 (capped AD sum, c=2). Reject for large S2.
- **A2** = sum_i t_i - n (plain Anderson-Darling). Reject for large A2.
- **W** = Shapiro-Wilk (scipy.stats.shapiro). Reject for small W.
- **Normal calibration**: for each n, 20000 N(0,1) samples give the null distribution of S2, A2, W.
  p_S2 and p_A2 are upper-tail empirical p-values against that null sample.
- **bonf-maxp** (Bonferroni max-p): reject when min(p_S2, p_A2) < 0.025.
- **either-2.5** (reject-if-either): reject when S2 exceeds its normal-calibrated 97.5% quantile
  or A2 exceeds its normal-calibrated 97.5% quantile.
- Comparators A2, W and S2-alone each use their own normal-calibrated 5% critical value.
- Paired difference = mean over the same 20000 samples of (combo rejects) - (comparator rejects);
  SE = sd of that per-sample difference / sqrt(20000). win/loss = outside two SE; tie = inside.
  `vs S2` reports whether the combination stays within two SE of S2 alone (within / above / below).

## Results (20000 sims per (n, law), seed 91404)

| combo | n | law | power | A2 | W | S2 | combo-A2 | SE | vs A2 | combo-W | SE | vs W | combo-S2 | SE | vs S2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bonf-maxp | 25 | normal | 0.0355 | 0.0500 | 0.0500 | 0.0500 | -0.0145 | 0.0011 | size | -0.0145 | 0.0010 | size | -0.0145 | 0.0012 | size |
| either-2.5 | 25 | normal | 0.0355 | 0.0500 | 0.0500 | 0.0500 | -0.0144 | 0.0011 | size | -0.0144 | 0.0010 | size | -0.0144 | 0.0012 | size |
| bonf-maxp | 25 | t(3) | 0.3886 | 0.3843 | 0.3992 | 0.4676 | +0.0043 | 0.0017 | win | -0.0106 | 0.0015 | loss | -0.0790 | 0.0020 | below |
| either-2.5 | 25 | t(3) | 0.3886 | 0.3843 | 0.3992 | 0.4676 | +0.0043 | 0.0017 | win | -0.0106 | 0.0015 | loss | -0.0790 | 0.0020 | below |
| bonf-maxp | 25 | t(5) | 0.1986 | 0.1961 | 0.2190 | 0.2659 | +0.0026 | 0.0015 | tie | -0.0204 | 0.0015 | loss | -0.0673 | 0.0019 | below |
| either-2.5 | 25 | t(5) | 0.1986 | 0.1961 | 0.2190 | 0.2659 | +0.0026 | 0.0015 | tie | -0.0204 | 0.0015 | loss | -0.0673 | 0.0019 | below |
| bonf-maxp | 25 | 0.9N(0,1)+0.1N(0,9) | 0.3185 | 0.2970 | 0.3439 | 0.3860 | +0.0214 | 0.0016 | win | -0.0255 | 0.0015 | loss | -0.0675 | 0.0019 | below |
| either-2.5 | 25 | 0.9N(0,1)+0.1N(0,9) | 0.3185 | 0.2970 | 0.3439 | 0.3860 | +0.0214 | 0.0016 | win | -0.0255 | 0.0015 | loss | -0.0675 | 0.0019 | below |
| bonf-maxp | 25 | chi2(5) | 0.4284 | 0.4733 | 0.5482 | 0.4752 | -0.0448 | 0.0020 | loss | -0.1197 | 0.0023 | loss | -0.0467 | 0.0021 | below |
| either-2.5 | 25 | chi2(5) | 0.4285 | 0.4733 | 0.5482 | 0.4752 | -0.0447 | 0.0020 | loss | -0.1196 | 0.0023 | loss | -0.0466 | 0.0021 | below |
| bonf-maxp | 50 | normal | 0.0376 | 0.0500 | 0.0500 | 0.0500 | -0.0124 | 0.0012 | size | -0.0124 | 0.0012 | size | -0.0124 | 0.0012 | size |
| either-2.5 | 50 | normal | 0.0376 | 0.0500 | 0.0500 | 0.0500 | -0.0124 | 0.0011 | size | -0.0124 | 0.0012 | size | -0.0124 | 0.0012 | size |
| bonf-maxp | 50 | t(3) | 0.6549 | 0.6051 | 0.6387 | 0.7319 | +0.0497 | 0.0019 | win | +0.0162 | 0.0017 | win | -0.0770 | 0.0019 | below |
| either-2.5 | 50 | t(3) | 0.6551 | 0.6051 | 0.6387 | 0.7319 | +0.0500 | 0.0019 | win | +0.0164 | 0.0017 | win | -0.0768 | 0.0019 | below |
| bonf-maxp | 50 | t(5) | 0.3445 | 0.2952 | 0.3513 | 0.4363 | +0.0493 | 0.0020 | win | -0.0068 | 0.0019 | loss | -0.0918 | 0.0021 | below |
| either-2.5 | 50 | t(5) | 0.3451 | 0.2952 | 0.3513 | 0.4363 | +0.0500 | 0.0020 | win | -0.0062 | 0.0019 | loss | -0.0912 | 0.0021 | below |
| bonf-maxp | 50 | 0.9N(0,1)+0.1N(0,9) | 0.5327 | 0.4558 | 0.5548 | 0.6091 | +0.0770 | 0.0021 | win | -0.0221 | 0.0018 | loss | -0.0764 | 0.0019 | below |
| either-2.5 | 50 | 0.9N(0,1)+0.1N(0,9) | 0.5331 | 0.4558 | 0.5548 | 0.6091 | +0.0773 | 0.0021 | win | -0.0217 | 0.0018 | loss | -0.0760 | 0.0019 | below |
| bonf-maxp | 50 | chi2(5) | 0.7519 | 0.7963 | 0.8875 | 0.7271 | -0.0444 | 0.0018 | loss | -0.1356 | 0.0024 | loss | +0.0248 | 0.0022 | above |
| either-2.5 | 50 | chi2(5) | 0.7521 | 0.7963 | 0.8875 | 0.7271 | -0.0441 | 0.0018 | loss | -0.1353 | 0.0024 | loss | +0.0250 | 0.0022 | above |
| bonf-maxp | 100 | normal | 0.0395 | 0.0500 | 0.0500 | 0.0500 | -0.0105 | 0.0013 | size | -0.0105 | 0.0013 | size | -0.0105 | 0.0013 | size |
| either-2.5 | 100 | normal | 0.0396 | 0.0500 | 0.0500 | 0.0500 | -0.0104 | 0.0012 | size | -0.0104 | 0.0013 | size | -0.0104 | 0.0013 | size |
| bonf-maxp | 100 | t(3) | 0.9122 | 0.8528 | 0.8779 | 0.9386 | +0.0595 | 0.0018 | win | +0.0343 | 0.0015 | win | -0.0265 | 0.0011 | below |
| either-2.5 | 100 | t(3) | 0.9122 | 0.8528 | 0.8779 | 0.9386 | +0.0595 | 0.0018 | win | +0.0343 | 0.0015 | win | -0.0265 | 0.0011 | below |
| bonf-maxp | 100 | t(5) | 0.6162 | 0.4873 | 0.5686 | 0.6946 | +0.1289 | 0.0026 | win | +0.0476 | 0.0023 | win | -0.0784 | 0.0019 | below |
| either-2.5 | 100 | t(5) | 0.6166 | 0.4873 | 0.5686 | 0.6946 | +0.1293 | 0.0026 | win | +0.0479 | 0.0023 | win | -0.0780 | 0.0019 | below |
| bonf-maxp | 100 | 0.9N(0,1)+0.1N(0,9) | 0.7952 | 0.6803 | 0.7978 | 0.8392 | +0.1149 | 0.0023 | win | -0.0027 | 0.0017 | tie | -0.0440 | 0.0015 | below |
| either-2.5 | 100 | 0.9N(0,1)+0.1N(0,9) | 0.7954 | 0.6803 | 0.7978 | 0.8392 | +0.1151 | 0.0023 | win | -0.0024 | 0.0018 | tie | -0.0439 | 0.0015 | below |
| bonf-maxp | 100 | chi2(5) | 0.9795 | 0.9882 | 0.9983 | 0.9371 | -0.0088 | 0.0007 | loss | -0.0189 | 0.0010 | loss | +0.0424 | 0.0015 | above |
| either-2.5 | 100 | chi2(5) | 0.9796 | 0.9882 | 0.9983 | 0.9371 | -0.0086 | 0.0007 | loss | -0.0188 | 0.0010 | loss | +0.0425 | 0.0015 | above |

Losing cells (combination loses by more than two paired SE):
- bonf-maxp, n=25, t(3), vs W: diff -0.0106 (-6.9 SE)
- either-2.5, n=25, t(3), vs W: diff -0.0106 (-6.9 SE)
- bonf-maxp, n=25, t(5), vs W: diff -0.0204 (-13.9 SE)
- either-2.5, n=25, t(5), vs W: diff -0.0204 (-13.9 SE)
- bonf-maxp, n=25, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0255 (-16.9 SE)
- either-2.5, n=25, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0255 (-16.9 SE)
- bonf-maxp, n=25, chi2(5), vs A2: diff -0.0448 (-22.0 SE)
- bonf-maxp, n=25, chi2(5), vs W: diff -0.1197 (-52.0 SE)
- either-2.5, n=25, chi2(5), vs A2: diff -0.0447 (-22.0 SE)
- either-2.5, n=25, chi2(5), vs W: diff -0.1196 (-51.9 SE)
- bonf-maxp, n=50, t(5), vs W: diff -0.0068 (-3.6 SE)
- either-2.5, n=50, t(5), vs W: diff -0.0062 (-3.3 SE)
- bonf-maxp, n=50, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0221 (-12.0 SE)
- either-2.5, n=50, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0217 (-11.8 SE)
- bonf-maxp, n=50, chi2(5), vs A2: diff -0.0444 (-25.3 SE)
- bonf-maxp, n=50, chi2(5), vs W: diff -0.1356 (-55.8 SE)
- either-2.5, n=50, chi2(5), vs A2: diff -0.0441 (-25.1 SE)
- either-2.5, n=50, chi2(5), vs W: diff -0.1353 (-55.8 SE)
- bonf-maxp, n=100, chi2(5), vs A2: diff -0.0088 (-12.2 SE)
- bonf-maxp, n=100, chi2(5), vs W: diff -0.0189 (-19.6 SE)
- either-2.5, n=100, chi2(5), vs A2: diff -0.0086 (-12.1 SE)
- either-2.5, n=100, chi2(5), vs W: diff -0.0188 (-19.6 SE)

## Per-rule-2 statement, per n and per combination

The two combinations are numerically identical to within 0.0007 in power in every cell, as at seed 91202,
so one line per n covers both bonf-maxp and either-2.5.

| n | vs plain AD (t3 / t5 / contam / chi2) | vs Shapiro-Wilk (t3 / t5 / contam / chi2) | within 2 SE of S2 alone on t3, t5, contam? |
|---|---|---|---|
| 25 | win / tie / win / loss | loss / loss / loss / loss | no: 34-40 SE below S2 on all three |
| 50 | win / win / win / loss | win / loss / loss / loss | no: 37-44 SE below S2 on all three |
| 100 | win / win / win / loss | win / win / tie / loss | no: 24-41 SE below S2 on all three |

Agreement with seed 91202: every chi2(5) cell is a loss under both seeds; every heavy-tail and contamination
cell vs A2 is a win under both seeds except t(5) n=25, which is a tie here and a win there (borderline);
vs W the two seeds agree in all cells except t(5) n=50 (loss here at -3.6 SE, tie there) and
contamination n=100 (tie here, loss at -2.4 SE there). Those three cells are the only seed-sensitive ones
and all sit near the two-SE line; nothing changes sign between seeds.

## Verdict

**Not omnibus-safe.** Replicated at a second seed: neither combination turns the chi-square(5) loss into a
tie or a gain. Both lose to plain AD at every n (-22, -25, -12 SE for n=25, 50, 100) and to Shapiro-Wilk
at every n (-52, -56, -20 SE). Both give back most of S2's heavy-tail and contamination edge: every such cell
is 24-44 SE below S2 alone, and at n=25 both combinations lose to Shapiro-Wilk on all three of those laws.

Mechanism, as at seed 91202: S2 and A2 share the same t_i and are strongly correlated under the null, so the
union of two 2.5% regions has actual size 3.5-4.0% (normal rows). The rule pays level without gaining an
independent view of skew.

Named losing cells (combination loses by more than two paired SE):
- bonf-maxp, n=25, t(3), vs W: diff -0.0106 (-6.9 SE)
- either-2.5, n=25, t(3), vs W: diff -0.0106 (-6.9 SE)
- bonf-maxp, n=25, t(5), vs W: diff -0.0204 (-13.9 SE)
- either-2.5, n=25, t(5), vs W: diff -0.0204 (-13.9 SE)
- bonf-maxp, n=25, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0255 (-16.9 SE)
- either-2.5, n=25, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0255 (-16.9 SE)
- bonf-maxp, n=25, chi2(5), vs A2: diff -0.0448 (-22.0 SE)
- bonf-maxp, n=25, chi2(5), vs W: diff -0.1197 (-52.0 SE)
- either-2.5, n=25, chi2(5), vs A2: diff -0.0447 (-22.0 SE)
- either-2.5, n=25, chi2(5), vs W: diff -0.1196 (-51.9 SE)
- bonf-maxp, n=50, t(5), vs W: diff -0.0068 (-3.6 SE)
- either-2.5, n=50, t(5), vs W: diff -0.0062 (-3.3 SE)
- bonf-maxp, n=50, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0221 (-12.0 SE)
- either-2.5, n=50, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0217 (-11.8 SE)
- bonf-maxp, n=50, chi2(5), vs A2: diff -0.0444 (-25.3 SE)
- bonf-maxp, n=50, chi2(5), vs W: diff -0.1356 (-55.8 SE)
- either-2.5, n=50, chi2(5), vs A2: diff -0.0441 (-25.1 SE)
- either-2.5, n=50, chi2(5), vs W: diff -0.1353 (-55.8 SE)
- bonf-maxp, n=100, chi2(5), vs A2: diff -0.0088 (-12.2 SE)
- bonf-maxp, n=100, chi2(5), vs W: diff -0.0189 (-19.6 SE)
- either-2.5, n=100, chi2(5), vs A2: diff -0.0086 (-12.1 SE)
- either-2.5, n=100, chi2(5), vs W: diff -0.0188 (-19.6 SE)

Not in the list (wins or ties): all heavy-tail and contamination cells vs A2 at every n; t(3) vs W at
n=50 and 100; t(5) vs W at n=100; contamination vs W at n=100.

Next step this suggests, same as member-2's: replace A2 with a partner that is weakly correlated with S2
under the null and sees skew directly (sample skewness sqrt(b1), or Shapiro-Wilk itself), and calibrate the
combined 5% point jointly rather than by Bonferroni so the level is not wasted.
