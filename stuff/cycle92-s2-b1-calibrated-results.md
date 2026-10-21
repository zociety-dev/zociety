# Cycle 92, stuff 2 (member-3): S2 + |b1| exact-size calibrated, 20000 sims per n, seed 92101

Runs the script in stuff 1 (`cycle92-s2-b1-calibrated-design.md`) unchanged. Seed **92101**,
20000 draws per (n, law), one `default_rng(92101)` stream consumed in order n=25, 50, 100,
laws normal, chi2(5), t3, t5, Laplace, cont10, cont5 per n. Wall clock 35 s
(`uv run --with numpy --with scipy python cycle92_s2_b1.py`).

## Definitions (rule 1, before any table)

Same as stuff 1: z = standardized sorted sample (n-1 sd); t_i = -((2i-1)/n)[ln Phi(z_(i)) + ln(1-Phi(z_(n+1-i)))];
**S2** = sum log(1+2 t_i)/2 (reject large); **A2** = sum t_i - n (plain AD, reject large);
**W** = Shapiro-Wilk (reject small); **partner |b1|** = |m3/m2^1.5| (sample skewness, two-sided, reject large).

Exact-size calibration: p_S2 and p_b1 are empirical upper-tail p-values against the 20000 null
S2 and |b1| values; the combination rejects when min(p_S2, p_b1) < c_n, with c_n the 5% null
quantile of min-p. MC SE of size = 0.0015; independence would give c_n = 0.0253.

## Null calibration (rule 1)

| n   | corr(S2,|b1|) Pearson | Spearman | c_n    | achieved null size | S2 5% crit | A2 5% crit | W 5% crit |
|-----|------------------------|----------|--------|--------------------|------------|------------|-----------|
| 25  | 0.761                  | 0.665    | 0.0371 | 0.0500             | 13.396     | 0.7365     | 0.9193    |
| 50  | 0.630                  | 0.538    | 0.0332 | 0.0500             | 26.509     | 0.7433     | 0.9544    |
| 100 | 0.491                  | 0.415    | 0.0305 | 0.0500             | 52.709     | 0.7489     | 0.9746    |

The "weakly correlated" premise of the direction is false at small n: S2 and |b1| have null
Pearson correlation 0.76 at n=25, falling to 0.49 at n=100. c_n sits well above the
independence value 0.0253 at every n, so the correlation buys back some of the min-p split.

## Comparison (rule 2): power at exact 5% size, 20000 draws per cell, all tests scored on the same draws

Gap = combo minus other, paired SE in parentheses. Verdict: beats if gap > 2 SE, loses if gap < -2 SE, else tie.

| n   | law     | combo  | S2     | A2     | W      | combo-A2 (SE)    | vs AD | combo-W (SE)     | vs SW | combo-S2 (SE)    | within 2 SE of S2? |
|-----|---------|--------|--------|--------|--------|------------------|-------|------------------|-------|------------------|--------------------|
| 25  | chi2(5) | 0.4841 | 0.4704 | 0.4650 | 0.5468 | +0.0191 (0.0028) | beats | -0.0627 (0.0024) | loses | +0.0137 (0.0015) | no (above)         |
| 25  | t3      | 0.4556 | 0.4620 | 0.3769 | 0.4012 | +0.0787 (0.0023) | beats | +0.0544 (0.0019) | beats | -0.0064 (0.0015) | no (below)         |
| 25  | t5      | 0.2620 | 0.2634 | 0.1898 | 0.2211 | +0.0722 (0.0023) | beats | +0.0409 (0.0018) | beats | -0.0014 (0.0014) | yes                |
| 25  | laplace | 0.3682 | 0.3888 | 0.3183 | 0.3084 | +0.0498 (0.0024) | beats | +0.0598 (0.0020) | beats | -0.0206 (0.0016) | no (below)         |
| 25  | cont10  | 0.3896 | 0.3840 | 0.2950 | 0.3465 | +0.0946 (0.0024) | beats | +0.0431 (0.0017) | beats | +0.0055 (0.0014) | no (above)         |
| 25  | cont5   | 0.4561 | 0.4517 | 0.3963 | 0.4346 | +0.0598 (0.0020) | beats | +0.0215 (0.0014) | beats | +0.0044 (0.0011) | no (above)         |
| 50  | chi2(5) | 0.7850 | 0.7281 | 0.8033 | 0.8923 | -0.0182 (0.0027) | loses | -0.1072 (0.0024) | loses | +0.0569 (0.0018) | no (above)         |
| 50  | t3      | 0.7025 | 0.7249 | 0.6032 | 0.6411 | +0.0993 (0.0024) | beats | +0.0614 (0.0019) | beats | -0.0224 (0.0015) | no (below)         |
| 50  | t5      | 0.4198 | 0.4355 | 0.3009 | 0.3579 | +0.1190 (0.0027) | beats | +0.0620 (0.0020) | beats | -0.0157 (0.0018) | no (below)         |
| 50  | laplace | 0.6128 | 0.6550 | 0.5474 | 0.5328 | +0.0655 (0.0025) | beats | +0.0800 (0.0022) | beats | -0.0422 (0.0018) | no (below)         |
| 50  | cont10  | 0.6125 | 0.6113 | 0.4641 | 0.5695 | +0.1484 (0.0028) | beats | +0.0430 (0.0017) | beats | +0.0012 (0.0016) | yes                |
| 50  | cont5   | 0.6761 | 0.6677 | 0.5875 | 0.6598 | +0.0886 (0.0022) | beats | +0.0164 (0.0012) | beats | +0.0084 (0.0013) | no (above)         |
| 100 | chi2(5) | 0.9822 | 0.9322 | 0.9877 | 0.9982 | -0.0056 (0.0010) | loses | -0.0161 (0.0009) | loses | +0.0500 (0.0016) | no (above)         |
| 100 | t3      | 0.9181 | 0.9344 | 0.8492 | 0.8756 | +0.0689 (0.0019) | beats | +0.0425 (0.0015) | beats | -0.0163 (0.0011) | no (below)         |
| 100 | t5      | 0.6463 | 0.6827 | 0.4798 | 0.5613 | +0.1664 (0.0031) | beats | +0.0850 (0.0023) | beats | -0.0364 (0.0019) | no (below)         |
| 100 | laplace | 0.8779 | 0.9122 | 0.8285 | 0.7993 | +0.0494 (0.0020) | beats | +0.0786 (0.0021) | beats | -0.0343 (0.0014) | no (below)         |
| 100 | cont10  | 0.8304 | 0.8351 | 0.6779 | 0.7992 | +0.1526 (0.0028) | beats | +0.0312 (0.0015) | beats | -0.0047 (0.0014) | no (below)         |
| 100 | cont5   | 0.8809 | 0.8776 | 0.8014 | 0.8752 | +0.0795 (0.0021) | beats | +0.0057 (0.0010) | beats | +0.0033 (0.0011) | no (above)         |

## Answer to the direction (seed 92101)

1. **Chi-square(5) vs AD:** beats at n=25 (+1.9 points), loses at n=50 (-1.8) and n=100 (-0.6).
   **Vs Shapiro-Wilk:** loses at every n (-6.3, -10.7, -1.6 points). The |b1| partner closes
   roughly half of S2's skew gap (S2 alone is 3 to 16 points behind SW) but does not tie SW anywhere.
2. **Heavy tails and contamination vs AD and SW:** the combination beats both on all 15 cells, every n.
3. **Stays within 2 paired SE of plain S2?** Mostly no. On t3, t5, Laplace the combination gives up
   0.6 to 4.2 points of S2's power (all beyond 2 SE except t5 at n=25); the cost grows with n
   (Laplace: -2.1, -4.2, -3.4 points). On contamination it is a tie or a small gain (within
   +0.8 points) except cont10 at n=100 (-0.5, beyond 2 SE). So the "within two paired SE" condition
   of the direction fails on 13 of 15 heavy-tail and contamination cells, though the losses are
   small relative to the gains over AD and SW.

Net: an exact-size min-p combination of S2 with |b1| is a strict improvement over S2 on skew and
still dominates AD and SW off-skew, but it is not a free lunch: it costs 1 to 4 points on heavy
tails and still loses to Shapiro-Wilk on chi-square(5) at every n. The null correlation between S2
and |b1| (0.49 to 0.76) is far from weak, which is why the gain on skew is only partial.

## What remains for stuff 3

Same seed, swap the partner to W (Shapiro-Wilk) as rule 1 allows, so the loss to SW on
chi-square(5) can be checked against a partner that is itself skew-optimal. Printed raw output
of this run is reproduced from the script exactly; no cell was edited by hand.
