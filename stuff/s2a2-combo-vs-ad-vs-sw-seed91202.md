# Cycle 91: S2+A2 combinations (Bonferroni max-p, reject-if-either) vs plain AD vs Shapiro-Wilk (seed 91202)

Script: `stuff/s2a2-combo-vs-ad-vs-sw-seed91202.py` (run with `uv run --with numpy --with scipy python ...`, 25 s).
Seed 91202 (numpy default_rng) was not used in cycles 88-90.

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

## Results (20000 sims per (n, law), seed 91202)

| combo | n | law | power | A2 | W | S2 | combo-A2 | SE | vs A2 | combo-W | SE | vs W | combo-S2 | SE | vs S2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bonf-maxp | 25 | normal | 0.0347 | 0.0500 | 0.0500 | 0.0500 | -0.0153 | 0.0011 | size | -0.0153 | 0.0010 | size | -0.0153 | 0.0012 | size |
| either-2.5 | 25 | normal | 0.0348 | 0.0500 | 0.0500 | 0.0500 | -0.0152 | 0.0011 | size | -0.0152 | 0.0010 | size | -0.0152 | 0.0012 | size |
| bonf-maxp | 25 | t(3) | 0.3785 | 0.3746 | 0.3936 | 0.4583 | +0.0040 | 0.0016 | win | -0.0151 | 0.0015 | loss | -0.0798 | 0.0020 | below |
| either-2.5 | 25 | t(3) | 0.3790 | 0.3746 | 0.3936 | 0.4583 | +0.0043 | 0.0016 | win | -0.0147 | 0.0015 | loss | -0.0794 | 0.0020 | below |
| bonf-maxp | 25 | t(5) | 0.1921 | 0.1888 | 0.2130 | 0.2653 | +0.0034 | 0.0015 | win | -0.0208 | 0.0015 | loss | -0.0732 | 0.0019 | below |
| either-2.5 | 25 | t(5) | 0.1925 | 0.1888 | 0.2130 | 0.2653 | +0.0037 | 0.0015 | win | -0.0204 | 0.0015 | loss | -0.0728 | 0.0019 | below |
| bonf-maxp | 25 | 0.9N(0,1)+0.1N(0,9) | 0.3083 | 0.2908 | 0.3385 | 0.3826 | +0.0175 | 0.0016 | win | -0.0302 | 0.0015 | loss | -0.0743 | 0.0019 | below |
| either-2.5 | 25 | 0.9N(0,1)+0.1N(0,9) | 0.3085 | 0.2908 | 0.3385 | 0.3826 | +0.0177 | 0.0016 | win | -0.0300 | 0.0015 | loss | -0.0741 | 0.0019 | below |
| bonf-maxp | 25 | chi2(5) | 0.4175 | 0.4568 | 0.5392 | 0.4681 | -0.0393 | 0.0020 | loss | -0.1216 | 0.0023 | loss | -0.0505 | 0.0021 | below |
| either-2.5 | 25 | chi2(5) | 0.4180 | 0.4568 | 0.5392 | 0.4681 | -0.0387 | 0.0020 | loss | -0.1211 | 0.0023 | loss | -0.0500 | 0.0021 | below |
| bonf-maxp | 50 | normal | 0.0377 | 0.0500 | 0.0500 | 0.0500 | -0.0123 | 0.0012 | size | -0.0123 | 0.0012 | size | -0.0123 | 0.0012 | size |
| either-2.5 | 50 | normal | 0.0379 | 0.0500 | 0.0500 | 0.0500 | -0.0121 | 0.0012 | size | -0.0121 | 0.0012 | size | -0.0121 | 0.0012 | size |
| bonf-maxp | 50 | t(3) | 0.6705 | 0.6143 | 0.6443 | 0.7353 | +0.0562 | 0.0020 | win | +0.0262 | 0.0018 | win | -0.0649 | 0.0018 | below |
| either-2.5 | 50 | t(3) | 0.6706 | 0.6143 | 0.6443 | 0.7353 | +0.0563 | 0.0020 | win | +0.0263 | 0.0018 | win | -0.0647 | 0.0018 | below |
| bonf-maxp | 50 | t(5) | 0.3644 | 0.3037 | 0.3561 | 0.4413 | +0.0607 | 0.0021 | win | +0.0083 | 0.0019 | win | -0.0769 | 0.0019 | below |
| either-2.5 | 50 | t(5) | 0.3648 | 0.3037 | 0.3561 | 0.4413 | +0.0611 | 0.0021 | win | +0.0087 | 0.0019 | win | -0.0765 | 0.0019 | below |
| bonf-maxp | 50 | 0.9N(0,1)+0.1N(0,9) | 0.5485 | 0.4636 | 0.5616 | 0.6095 | +0.0850 | 0.0022 | win | -0.0131 | 0.0019 | loss | -0.0609 | 0.0018 | below |
| either-2.5 | 50 | 0.9N(0,1)+0.1N(0,9) | 0.5487 | 0.4636 | 0.5616 | 0.6095 | +0.0852 | 0.0022 | win | -0.0129 | 0.0019 | loss | -0.0607 | 0.0018 | below |
| bonf-maxp | 50 | chi2(5) | 0.7503 | 0.8005 | 0.8863 | 0.7230 | -0.0503 | 0.0018 | loss | -0.1360 | 0.0024 | loss | +0.0273 | 0.0021 | above |
| either-2.5 | 50 | chi2(5) | 0.7506 | 0.8005 | 0.8863 | 0.7230 | -0.0500 | 0.0018 | loss | -0.1358 | 0.0024 | loss | +0.0276 | 0.0021 | above |
| bonf-maxp | 100 | normal | 0.0396 | 0.0500 | 0.0500 | 0.0500 | -0.0104 | 0.0012 | size | -0.0104 | 0.0013 | size | -0.0104 | 0.0013 | size |
| either-2.5 | 100 | normal | 0.0397 | 0.0500 | 0.0500 | 0.0500 | -0.0103 | 0.0012 | size | -0.0103 | 0.0013 | size | -0.0103 | 0.0013 | size |
| bonf-maxp | 100 | t(3) | 0.9073 | 0.8501 | 0.8739 | 0.9336 | +0.0571 | 0.0017 | win | +0.0335 | 0.0015 | win | -0.0263 | 0.0012 | below |
| either-2.5 | 100 | t(3) | 0.9074 | 0.8501 | 0.8739 | 0.9336 | +0.0573 | 0.0017 | win | +0.0336 | 0.0015 | win | -0.0261 | 0.0012 | below |
| bonf-maxp | 100 | t(5) | 0.6096 | 0.4847 | 0.5658 | 0.6876 | +0.1249 | 0.0025 | win | +0.0438 | 0.0022 | win | -0.0780 | 0.0019 | below |
| either-2.5 | 100 | t(5) | 0.6099 | 0.4847 | 0.5658 | 0.6876 | +0.1252 | 0.0025 | win | +0.0441 | 0.0023 | win | -0.0777 | 0.0019 | below |
| bonf-maxp | 100 | 0.9N(0,1)+0.1N(0,9) | 0.7909 | 0.6734 | 0.7951 | 0.8330 | +0.1174 | 0.0024 | win | -0.0042 | 0.0018 | loss | -0.0421 | 0.0014 | below |
| either-2.5 | 100 | 0.9N(0,1)+0.1N(0,9) | 0.7910 | 0.6734 | 0.7951 | 0.8330 | +0.1176 | 0.0024 | win | -0.0040 | 0.0018 | loss | -0.0420 | 0.0014 | below |
| bonf-maxp | 100 | chi2(5) | 0.9759 | 0.9877 | 0.9981 | 0.9315 | -0.0118 | 0.0008 | loss | -0.0222 | 0.0010 | loss | +0.0444 | 0.0015 | above |
| either-2.5 | 100 | chi2(5) | 0.9759 | 0.9877 | 0.9981 | 0.9315 | -0.0117 | 0.0008 | loss | -0.0221 | 0.0010 | loss | +0.0444 | 0.0015 | above |

Losing cells (combination loses by more than two paired SE):
- bonf-maxp, n=25, t(3), vs W: diff -0.0151 (-10.0 SE)
- either-2.5, n=25, t(3), vs W: diff -0.0147 (-9.8 SE)
- bonf-maxp, n=25, t(5), vs W: diff -0.0208 (-14.0 SE)
- either-2.5, n=25, t(5), vs W: diff -0.0204 (-13.8 SE)
- bonf-maxp, n=25, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0302 (-19.6 SE)
- either-2.5, n=25, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0300 (-19.5 SE)
- bonf-maxp, n=25, chi2(5), vs A2: diff -0.0393 (-19.8 SE)
- bonf-maxp, n=25, chi2(5), vs W: diff -0.1216 (-52.5 SE)
- either-2.5, n=25, chi2(5), vs A2: diff -0.0387 (-19.5 SE)
- either-2.5, n=25, chi2(5), vs W: diff -0.1211 (-52.4 SE)
- bonf-maxp, n=50, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0131 (-7.0 SE)
- either-2.5, n=50, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0129 (-6.9 SE)
- bonf-maxp, n=50, chi2(5), vs A2: diff -0.0503 (-27.3 SE)
- bonf-maxp, n=50, chi2(5), vs W: diff -0.1360 (-56.1 SE)
- either-2.5, n=50, chi2(5), vs A2: diff -0.0500 (-27.2 SE)
- either-2.5, n=50, chi2(5), vs W: diff -0.1358 (-56.0 SE)
- bonf-maxp, n=100, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0042 (-2.4 SE)
- either-2.5, n=100, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0040 (-2.3 SE)
- bonf-maxp, n=100, chi2(5), vs A2: diff -0.0118 (-15.0 SE)
- bonf-maxp, n=100, chi2(5), vs W: diff -0.0222 (-21.3 SE)
- either-2.5, n=100, chi2(5), vs A2: diff -0.0117 (-15.0 SE)
- either-2.5, n=100, chi2(5), vs W: diff -0.0221 (-21.3 SE)

## Per-rule-2 statement, per n and per combination

The two combinations are numerically almost identical in every cell (they differ by at most 0.0006 in power),
which is expected: both reject when either statistic clears its own 2.5% point, the only difference being
discrete p-value ties.

| n | combo | t(3) vs A2 / W | t(5) vs A2 / W | 0.9N+0.1N(0,9) vs A2 / W | chi2(5) vs A2 / W | within 2 SE of S2 alone on heavy-tail/contamination? |
|---|---|---|---|---|---|---|
| 25 | bonf-maxp | win / loss | win / loss | win / loss | loss / loss | no (below by 37-40 SE on all three) |
| 25 | either-2.5 | win / loss | win / loss | win / loss | loss / loss | no (below) |
| 50 | bonf-maxp | win / win | win / win | win / loss | loss / loss | no (below by 32-40 SE) |
| 50 | either-2.5 | win / win | win / win | win / loss | loss / loss | no (below) |
| 100 | bonf-maxp | win / win | win / win | win / loss (-2.4 SE) | loss / loss | no (below by 22-41 SE) |
| 100 | either-2.5 | win / win | win / win | win / loss (-2.3 SE) | loss / loss | no (below) |

## Verdict

**Not omnibus-safe.** Neither combination turns the chi-square(5) loss into a tie or a gain: both lose to
plain AD at every n (-20, -27, -15 SE for n=25, 50, 100) and to Shapiro-Wilk at every n (-52, -56, -21 SE).
They also give back a large part of S2's heavy-tail and contamination gains: every heavy-tail and
contamination cell sits 22-40 SE below S2 alone, and at n=25 the combinations lose to Shapiro-Wilk on all
three of those laws, which S2 alone did not.

Why: S2 and A2 are built from the same t_i and are highly correlated under the null, so the union of two
2.5% regions has actual size only 3.5-4.0% (see the normal rows). The combination spends level without
buying independent evidence; on chi2(5) it sits between S2 and A2 but closer to S2, and on heavy tails it
sits between S2 and A2 but well below S2.

Named losing cells (combination loses by more than two paired SE):
- bonf-maxp, n=25, t(3), vs W: diff -0.0151 (-10.0 SE)
- either-2.5, n=25, t(3), vs W: diff -0.0147 (-9.8 SE)
- bonf-maxp, n=25, t(5), vs W: diff -0.0208 (-14.0 SE)
- either-2.5, n=25, t(5), vs W: diff -0.0204 (-13.8 SE)
- bonf-maxp, n=25, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0302 (-19.6 SE)
- either-2.5, n=25, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0300 (-19.5 SE)
- bonf-maxp, n=25, chi2(5), vs A2: diff -0.0393 (-19.8 SE)
- bonf-maxp, n=25, chi2(5), vs W: diff -0.1216 (-52.5 SE)
- either-2.5, n=25, chi2(5), vs A2: diff -0.0387 (-19.5 SE)
- either-2.5, n=25, chi2(5), vs W: diff -0.1211 (-52.4 SE)
- bonf-maxp, n=50, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0131 (-7.0 SE)
- either-2.5, n=50, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0129 (-6.9 SE)
- bonf-maxp, n=50, chi2(5), vs A2: diff -0.0503 (-27.3 SE)
- bonf-maxp, n=50, chi2(5), vs W: diff -0.1360 (-56.1 SE)
- either-2.5, n=50, chi2(5), vs A2: diff -0.0500 (-27.2 SE)
- either-2.5, n=50, chi2(5), vs W: diff -0.1358 (-56.0 SE)
- bonf-maxp, n=100, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0042 (-2.4 SE)
- either-2.5, n=100, 0.9N(0,1)+0.1N(0,9), vs W: diff -0.0040 (-2.3 SE)
- bonf-maxp, n=100, chi2(5), vs A2: diff -0.0118 (-15.0 SE)
- bonf-maxp, n=100, chi2(5), vs W: diff -0.0222 (-21.3 SE)
- either-2.5, n=100, chi2(5), vs A2: diff -0.0117 (-15.0 SE)
- either-2.5, n=100, chi2(5), vs W: diff -0.0221 (-21.3 SE)

Not in the list (wins or ties): all heavy-tail and contamination cells vs A2 at every n; t(3) and t(5) vs W at n=50 and n=100.

Next step this suggests: pair S2 with a genuinely skew-sensitive statistic that is weakly correlated with it
under the null (sample skewness b1, or Shapiro-Wilk itself) rather than with A2, and recover the lost level
by calibrating the combined rule's 5% point jointly instead of by Bonferroni.
