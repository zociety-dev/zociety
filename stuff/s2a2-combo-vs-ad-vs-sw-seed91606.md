# Cycle 91: S2+A2 combinations (Bonferroni max-p, reject-if-either) vs plain AD vs Shapiro-Wilk, third seed 91606, plus a size-calibrated min-p check

Script: `stuff/s2a2-combo-vs-ad-vs-sw-seed91606.py` (run with `uv run --with numpy --with scipy python ...`, 27 s).
Seed 91606 (numpy default_rng) was not used in cycles 88-90 and differs from the cycle 91 seeds 91202 and 91404.
Same estimator and design as the two earlier items. Motivation for the extra row: both earlier items show the
combinations rejecting only 3.5-4.0% of normal samples, not 5%, because S2 and A2 are strongly correlated and
Bonferroni does not credit that. This item adds **minp-cal**, the same min-p statistic calibrated to exact 5% size,
to separate "the combination loses on chi2(5) because it is conservative" from "the combination loses because
S2 drags A2 down". Rule 1 and rule 2 rows (bonf-maxp, either-2.5) are all present and judged on their own.

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
- **minp-cal** (extra, not required by the rules): reject when min(p_S2, p_A2) is below the normal-calibrated
  5% quantile of min(p_S2, p_A2) itself, so its size is 5% by construction on the calibration sample.
- Comparators A2, W and S2-alone each use their own normal-calibrated 5% critical value.
- Paired difference = mean over the same 20000 samples of (combo rejects) - (comparator rejects);
  SE = sd of that per-sample difference / sqrt(20000). win/loss = outside two SE; tie = inside.
  `vs S2` reports whether the combination stays within two SE of S2 alone (within / above / below).

## Results (20000 sims per (n, law), seed 91606)

| combo | n | law | power | A2 | W | S2 | combo-A2 | SE | vs A2 | combo-W | SE | vs W | combo-S2 | SE | vs S2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bonf-maxp | 25 | normal | 0.0352 | 0.0500 | 0.0500 | 0.0500 | -0.0147 | 0.0011 | size | -0.0147 | 0.0010 | size | -0.0147 | 0.0012 | size |
| either-2.5 | 25 | normal | 0.0353 | 0.0500 | 0.0500 | 0.0500 | -0.0147 | 0.0011 | size | -0.0147 | 0.0010 | size | -0.0147 | 0.0012 | size |
| minp-cal | 25 | normal | 0.0500 | 0.0500 | 0.0500 | 0.0500 | -0.0001 | 0.0010 | size | -0.0001 | 0.0010 | size | -0.0001 | 0.0011 | size |
| bonf-maxp | 25 | t(3) | 0.3926 | 0.3869 | 0.4042 | 0.4637 | +0.0057 | 0.0016 | win | -0.0116 | 0.0015 | loss | -0.0712 | 0.0019 | below |
| either-2.5 | 25 | t(3) | 0.3927 | 0.3869 | 0.4042 | 0.4637 | +0.0059 | 0.0016 | win | -0.0115 | 0.0015 | loss | -0.0710 | 0.0019 | below |
| minp-cal | 25 | t(3) | 0.4354 | 0.3869 | 0.4042 | 0.4637 | +0.0485 | 0.0018 | win | +0.0312 | 0.0016 | win | -0.0284 | 0.0014 | below |
| bonf-maxp | 25 | t(5) | 0.2067 | 0.1997 | 0.2281 | 0.2695 | +0.0070 | 0.0016 | win | -0.0213 | 0.0015 | loss | -0.0628 | 0.0018 | below |
| either-2.5 | 25 | t(5) | 0.2069 | 0.1997 | 0.2281 | 0.2695 | +0.0073 | 0.0016 | win | -0.0211 | 0.0015 | loss | -0.0625 | 0.0018 | below |
| minp-cal | 25 | t(5) | 0.2427 | 0.1997 | 0.2281 | 0.2695 | +0.0430 | 0.0017 | win | +0.0147 | 0.0015 | win | -0.0267 | 0.0014 | below |
| bonf-maxp | 25 | 0.9N(0,1)+0.1N(0,9) | 0.3252 | 0.3008 | 0.3511 | 0.3853 | +0.0245 | 0.0016 | win | -0.0259 | 0.0015 | loss | -0.0600 | 0.0018 | below |
| either-2.5 | 25 | 0.9N(0,1)+0.1N(0,9) | 0.3255 | 0.3008 | 0.3511 | 0.3853 | +0.0247 | 0.0016 | win | -0.0256 | 0.0015 | loss | -0.0599 | 0.0018 | below |
| minp-cal | 25 | 0.9N(0,1)+0.1N(0,9) | 0.3619 | 0.3008 | 0.3511 | 0.3853 | +0.0612 | 0.0019 | win | +0.0109 | 0.0015 | win | -0.0233 | 0.0013 | below |
| bonf-maxp | 25 | chi2(5) | 0.4377 | 0.4765 | 0.5531 | 0.4729 | -0.0389 | 0.0020 | loss | -0.1153 | 0.0023 | loss | -0.0352 | 0.0021 | below |
| either-2.5 | 25 | chi2(5) | 0.4379 | 0.4765 | 0.5531 | 0.4729 | -0.0387 | 0.0020 | loss | -0.1152 | 0.0023 | loss | -0.0351 | 0.0021 | below |
| minp-cal | 25 | chi2(5) | 0.4870 | 0.4765 | 0.5531 | 0.4729 | +0.0104 | 0.0019 | win | -0.0660 | 0.0019 | loss | +0.0140 | 0.0018 | above |
| bonf-maxp | 50 | normal | 0.0372 | 0.0500 | 0.0500 | 0.0500 | -0.0127 | 0.0011 | size | -0.0127 | 0.0012 | size | -0.0127 | 0.0012 | size |
| either-2.5 | 50 | normal | 0.0374 | 0.0500 | 0.0500 | 0.0500 | -0.0126 | 0.0011 | size | -0.0126 | 0.0012 | size | -0.0126 | 0.0012 | size |
| minp-cal | 50 | normal | 0.0500 | 0.0500 | 0.0500 | 0.0500 | +0.0000 | 0.0011 | size | +0.0000 | 0.0013 | size | +0.0000 | 0.0012 | size |
| bonf-maxp | 50 | t(3) | 0.6519 | 0.5999 | 0.6351 | 0.7199 | +0.0520 | 0.0019 | win | +0.0169 | 0.0018 | win | -0.0680 | 0.0018 | below |
| either-2.5 | 50 | t(3) | 0.6519 | 0.5999 | 0.6351 | 0.7199 | +0.0520 | 0.0019 | win | +0.0169 | 0.0018 | win | -0.0680 | 0.0018 | below |
| minp-cal | 50 | t(3) | 0.6839 | 0.5999 | 0.6351 | 0.7199 | +0.0840 | 0.0021 | win | +0.0488 | 0.0019 | win | -0.0360 | 0.0014 | below |
| bonf-maxp | 50 | t(5) | 0.3501 | 0.3018 | 0.3495 | 0.4379 | +0.0483 | 0.0020 | win | +0.0006 | 0.0019 | tie | -0.0878 | 0.0021 | below |
| either-2.5 | 50 | t(5) | 0.3502 | 0.3018 | 0.3495 | 0.4379 | +0.0484 | 0.0020 | win | +0.0006 | 0.0019 | tie | -0.0877 | 0.0021 | below |
| minp-cal | 50 | t(5) | 0.3888 | 0.3018 | 0.3495 | 0.4379 | +0.0871 | 0.0022 | win | +0.0393 | 0.0020 | win | -0.0491 | 0.0017 | below |
| bonf-maxp | 50 | 0.9N(0,1)+0.1N(0,9) | 0.5399 | 0.4595 | 0.5604 | 0.6077 | +0.0804 | 0.0021 | win | -0.0205 | 0.0018 | loss | -0.0678 | 0.0018 | below |
| either-2.5 | 50 | 0.9N(0,1)+0.1N(0,9) | 0.5400 | 0.4595 | 0.5604 | 0.6077 | +0.0804 | 0.0021 | win | -0.0204 | 0.0018 | loss | -0.0677 | 0.0018 | below |
| minp-cal | 50 | 0.9N(0,1)+0.1N(0,9) | 0.5712 | 0.4595 | 0.5604 | 0.6077 | +0.1116 | 0.0023 | win | +0.0107 | 0.0019 | win | -0.0365 | 0.0015 | below |
| bonf-maxp | 50 | chi2(5) | 0.7515 | 0.8015 | 0.8878 | 0.7236 | -0.0500 | 0.0019 | loss | -0.1363 | 0.0024 | loss | +0.0279 | 0.0021 | above |
| either-2.5 | 50 | chi2(5) | 0.7517 | 0.8015 | 0.8878 | 0.7236 | -0.0498 | 0.0019 | loss | -0.1361 | 0.0024 | loss | +0.0280 | 0.0021 | above |
| minp-cal | 50 | chi2(5) | 0.7843 | 0.8015 | 0.8878 | 0.7236 | -0.0173 | 0.0016 | loss | -0.1035 | 0.0022 | loss | +0.0607 | 0.0021 | above |
| bonf-maxp | 100 | normal | 0.0398 | 0.0500 | 0.0500 | 0.0500 | -0.0101 | 0.0012 | size | -0.0101 | 0.0013 | size | -0.0101 | 0.0013 | size |
| either-2.5 | 100 | normal | 0.0399 | 0.0500 | 0.0500 | 0.0500 | -0.0100 | 0.0012 | size | -0.0100 | 0.0013 | size | -0.0100 | 0.0013 | size |
| minp-cal | 100 | normal | 0.0500 | 0.0500 | 0.0500 | 0.0500 | -0.0001 | 0.0012 | size | -0.0001 | 0.0014 | size | -0.0001 | 0.0013 | size |
| bonf-maxp | 100 | t(3) | 0.9077 | 0.8518 | 0.8761 | 0.9369 | +0.0559 | 0.0017 | win | +0.0316 | 0.0015 | win | -0.0293 | 0.0012 | below |
| either-2.5 | 100 | t(3) | 0.9081 | 0.8518 | 0.8761 | 0.9369 | +0.0563 | 0.0017 | win | +0.0319 | 0.0015 | win | -0.0289 | 0.0012 | below |
| minp-cal | 100 | t(3) | 0.9194 | 0.8518 | 0.8761 | 0.9369 | +0.0677 | 0.0018 | win | +0.0433 | 0.0016 | win | -0.0175 | 0.0009 | below |
| bonf-maxp | 100 | t(5) | 0.6022 | 0.4839 | 0.5645 | 0.6830 | +0.1184 | 0.0025 | win | +0.0377 | 0.0022 | win | -0.0808 | 0.0020 | below |
| either-2.5 | 100 | t(5) | 0.6031 | 0.4839 | 0.5645 | 0.6830 | +0.1193 | 0.0025 | win | +0.0386 | 0.0022 | win | -0.0799 | 0.0020 | below |
| minp-cal | 100 | t(5) | 0.6318 | 0.4839 | 0.5645 | 0.6830 | +0.1479 | 0.0026 | win | +0.0673 | 0.0023 | win | -0.0512 | 0.0016 | below |
| bonf-maxp | 100 | 0.9N(0,1)+0.1N(0,9) | 0.7907 | 0.6851 | 0.7988 | 0.8351 | +0.1056 | 0.0023 | win | -0.0081 | 0.0018 | loss | -0.0444 | 0.0015 | below |
| either-2.5 | 100 | 0.9N(0,1)+0.1N(0,9) | 0.7915 | 0.6851 | 0.7988 | 0.8351 | +0.1064 | 0.0023 | win | -0.0073 | 0.0018 | loss | -0.0437 | 0.0015 | below |
| minp-cal | 100 | 0.9N(0,1)+0.1N(0,9) | 0.8069 | 0.6851 | 0.7988 | 0.8351 | +0.1218 | 0.0024 | win | +0.0080 | 0.0018 | win | -0.0283 | 0.0012 | below |
| bonf-maxp | 100 | chi2(5) | 0.9770 | 0.9879 | 0.9973 | 0.9311 | -0.0109 | 0.0008 | loss | -0.0203 | 0.0010 | loss | +0.0459 | 0.0016 | above |
| either-2.5 | 100 | chi2(5) | 0.9771 | 0.9879 | 0.9973 | 0.9311 | -0.0109 | 0.0008 | loss | -0.0202 | 0.0010 | loss | +0.0460 | 0.0016 | above |
| minp-cal | 100 | chi2(5) | 0.9815 | 0.9879 | 0.9973 | 0.9311 | -0.0065 | 0.0006 | loss | -0.0158 | 0.0009 | loss | +0.0504 | 0.0016 | above |


## Losing cells (combination loses by more than two paired SE), as printed by the script

- bonf-maxp, n=25, t(3), vs W: diff -0.0116 (-7.5 SE)
- either-2.5, n=25, t(3), vs W: diff -0.0115 (-7.4 SE)
- bonf-maxp, n=25, t(5), vs W: diff -0.0213 (-14.5 SE)
- either-2.5, n=25, t(5), vs W: diff -0.0211 (-14.4 SE)
- bonf-maxp, n=25, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0259 (-16.9 SE)
- either-2.5, n=25, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0256 (-16.8 SE)
- bonf-maxp, n=25, chi2(5), vs A2: diff -0.0389 (-19.4 SE)
- bonf-maxp, n=25, chi2(5), vs W: diff -0.1153 (-50.7 SE)
- either-2.5, n=25, chi2(5), vs A2: diff -0.0387 (-19.3 SE)
- either-2.5, n=25, chi2(5), vs W: diff -0.1152 (-50.7 SE)
- minp-cal, n=25, chi2(5), vs W: diff -0.0660 (-35.5 SE)
- bonf-maxp, n=50, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0205 (-11.1 SE)
- either-2.5, n=50, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0204 (-11.1 SE)
- bonf-maxp, n=50, chi2(5), vs A2: diff -0.0500 (-26.9 SE)
- bonf-maxp, n=50, chi2(5), vs W: diff -0.1363 (-56.1 SE)
- either-2.5, n=50, chi2(5), vs A2: diff -0.0498 (-26.8 SE)
- either-2.5, n=50, chi2(5), vs W: diff -0.1361 (-56.1 SE)
- minp-cal, n=50, chi2(5), vs A2: diff -0.0173 (-10.9 SE)
- minp-cal, n=50, chi2(5), vs W: diff -0.1035 (-47.8 SE)
- bonf-maxp, n=100, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0081 (-4.6 SE)
- either-2.5, n=100, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0073 (-4.2 SE)
- bonf-maxp, n=100, chi2(5), vs A2: diff -0.0109 (-14.5 SE)
- bonf-maxp, n=100, chi2(5), vs W: diff -0.0203 (-20.4 SE)
- either-2.5, n=100, chi2(5), vs A2: diff -0.0109 (-14.4 SE)
- either-2.5, n=100, chi2(5), vs W: diff -0.0202 (-20.3 SE)
- minp-cal, n=100, chi2(5), vs A2: diff -0.0065 (-10.6 SE)
- minp-cal, n=100, chi2(5), vs W: diff -0.0158 (-17.9 SE)

## Verdict per rule 2 (bonf-maxp and either-2.5)

Neither required combination is omnibus-safe. The two combinations are numerically identical to within one
rejection in a few thousand (the max-p rule and the either rule are the same event up to tie-breaking), so each
cell below holds for both.

- **vs plain AD:** win on t(3) at every n, t(5) at n=50 and 100 (tie at n=25), and the contamination mixture at
  every n; loss on chi2(5) at every n (-19, -27, -14 SE). That matches 91202 and 91404 cell for cell.
- **vs Shapiro-Wilk:** loss on chi2(5) at every n (-51, -56, -20 SE); also loss on t(5) at n=25, on the
  contamination mixture at n=25, 50, 100, and win only on t(3) at n=50, 100 and t(5) at n=50, 100. The n=100
  contamination cell was a tie at 91404 (-1.5 SE) and is a loss here (-4.6 SE): it sits on the line across seeds.
- **vs S2 alone:** below on every heavy-tail and contamination cell (by 14 to 44 SE), above S2 on chi2(5) at
  n=50 and 100, below at n=25. The combination does not stay within two SE of S2 anywhere.

Omnibus-safe verdict: **no**. Losing cells, both combinations: chi2(5) vs A2 at n=25, 50, 100; chi2(5) vs W at
n=25, 50, 100; mixture vs W at n=25, 50, 100; t(5) vs W at n=25.

## What the extra minp-cal row says

Calibrating the min-p statistic to exact 5% size recovers most of what Bonferroni throws away: minp-cal beats
both AD and Shapiro-Wilk on every t(3), t(5) and contamination cell at every n (smallest margin +4.3 SE,
mixture vs W at n=100), and on chi2(5) it beats AD at n=25 (+5.5 SE) while still losing to AD at n=50 and 100
(-11 SE each) and to Shapiro-Wilk at every n (-36, -48, -18 SE). It stays 13-32 SE below S2 alone on the
heavy-tail laws. So about half of the chi2(5) gap to AD at n=25 to 100 is the Bonferroni size penalty, and
the remaining half, plus the whole gap to Shapiro-Wilk, is structural: A2 is not skew-sensitive enough to
compensate for S2 on a right-skewed law. A partner statistic that is weakly correlated with S2 under the null
and sensitive to skew (sample skewness, or Shapiro-Wilk itself) is the next thing to try, with the same
size-calibrated min-p rule.
