# Cycle 92, stuff 3 (member-1): S2 + W (Shapiro-Wilk) exact-size calibrated, 20000 sims per n, seed 92101

Runs the stuff 1 script with the partner swapped from |b1| to **W**, as rule 1 allows, and the
same seed **92101** so every draw is identical to stuff 2 (`cycle92-s2-b1-calibrated-results.md`):
one `default_rng(92101)` stream consumed in order n=25, 50, 100, laws normal, chi2(5), t3, t5,
Laplace, cont10, cont5 per n. The S2, A2 and W columns below therefore match stuff 2 to the draw;
only the combination changes. Wall clock 35 s. Two-line diff against the stuff 1 script:
`return s2, a2, b1, w` becomes `return s2, a2, -w, w` (so the "reject large" empirical upper-tail
p-value machinery is applied to -W unchanged), and the printed label. No cell edited by hand.

## Definitions (rule 1, before any table)

z = standardized sorted sample (n-1 sd); t_i = -((2i-1)/n)[ln Phi(z_(i)) + ln(1-Phi(z_(n+1-i)))];
**S2** = sum log(1+2 t_i)/2 (reject large); **A2** = sum t_i - n (plain AD, reject large);
**W** = Shapiro-Wilk (reject small); **partner W** = the same Shapiro-Wilk statistic, used as the
second leg of the combination with lower-tail p-value p_W = P(W_null <= W).

Exact-size calibration: p_S2 (upper tail) and p_W (lower tail) are empirical p-values against the
20000 null S2 and W values; the combination rejects when min(p_S2, p_W) < c_n, with c_n the 5% null
quantile of min-p. MC SE of size = 0.0015; independence would give c_n = 0.0253.

## Null calibration (rule 1)

| n   | corr(S2,-W) Pearson | Spearman | c_n    | achieved null size | S2 5% crit | A2 5% crit | W 5% crit |
|-----|---------------------|----------|--------|--------------------|------------|------------|-----------|
| 25  | 0.635               | 0.441    | 0.0385 | 0.0500             | 13.396     | 0.7365     | 0.9193    |
| 50  | 0.524               | 0.355    | 0.0348 | 0.0500             | 26.509     | 0.7433     | 0.9544    |
| 100 | 0.409               | 0.281    | 0.0326 | 0.0500             | 52.709     | 0.7489     | 0.9746    |

S2 and W are less correlated under the null than S2 and |b1| were (Pearson 0.64/0.52/0.41 here
versus 0.76/0.63/0.49 in stuff 2), but still not "weakly": the direction's premise fails for
both partners. c_n sits above the independence value 0.0253 at every n.

## Comparison (rule 2): power at exact 5% size, 20000 draws per cell, all tests scored on the same draws

Gap = combo minus other, paired SE in parentheses. Verdict: beats if gap > 2 SE, loses if gap < -2 SE, else tie.

| n   | law     | combo  | S2     | A2     | W      | combo-A2 (SE)    | vs AD | combo-W (SE)     | vs SW | combo-S2 (SE)    | within 2 SE of S2? |
|-----|---------|--------|--------|--------|--------|------------------|-------|------------------|-------|------------------|--------------------|
| 25  | chi2(5) | 0.5139 | 0.4703 | 0.4649 | 0.5467 | +0.0490 (0.0021) | beats | -0.0328 (0.0014) | loses | +0.0436 (0.0018) | no (above)         |
| 25  | t3      | 0.4364 | 0.4620 | 0.3769 | 0.4012 | +0.0595 (0.0020) | beats | +0.0352 (0.0016) | beats | -0.0256 (0.0013) | no (below)         |
| 25  | t5      | 0.2435 | 0.2633 | 0.1898 | 0.2210 | +0.0537 (0.0020) | beats | +0.0224 (0.0014) | beats | -0.0198 (0.0013) | no (below)         |
| 25  | laplace | 0.3532 | 0.3887 | 0.3183 | 0.3084 | +0.0348 (0.0021) | beats | +0.0448 (0.0017) | beats | -0.0356 (0.0014) | no (below)         |
| 25  | cont10  | 0.3656 | 0.3840 | 0.2949 | 0.3464 | +0.0706 (0.0020) | beats | +0.0192 (0.0013) | beats | -0.0184 (0.0012) | no (below)         |
| 25  | cont5   | 0.4427 | 0.4516 | 0.3963 | 0.4345 | +0.0464 (0.0018) | beats | +0.0082 (0.0010) | beats | -0.0089 (0.0010) | no (below)         |
| 50  | chi2(5) | 0.8586 | 0.7281 | 0.8033 | 0.8922 | +0.0553 (0.0019) | beats | -0.0337 (0.0013) | loses | +0.1305 (0.0026) | no (above)         |
| 50  | t3      | 0.6912 | 0.7248 | 0.6032 | 0.6411 | +0.0880 (0.0023) | beats | +0.0501 (0.0018) | beats | -0.0337 (0.0014) | no (below)         |
| 50  | t5      | 0.4032 | 0.4355 | 0.3009 | 0.3579 | +0.1024 (0.0025) | beats | +0.0454 (0.0019) | beats | -0.0323 (0.0015) | no (below)         |
| 50  | laplace | 0.6089 | 0.6550 | 0.5474 | 0.5328 | +0.0616 (0.0024) | beats | +0.0761 (0.0022) | beats | -0.0461 (0.0016) | no (below)         |
| 50  | cont10  | 0.5939 | 0.6113 | 0.4641 | 0.5695 | +0.1299 (0.0027) | beats | +0.0245 (0.0016) | beats | -0.0173 (0.0014) | no (below)         |
| 50  | cont5   | 0.6637 | 0.6677 | 0.5875 | 0.6597 | +0.0762 (0.0021) | beats | +0.0040 (0.0011) | beats | -0.0040 (0.0011) | no (below)         |
| 100 | chi2(5) | 0.9971 | 0.9322 | 0.9877 | 0.9982 | +0.0094 (0.0007) | beats | -0.0010 (0.0002) | loses | +0.0650 (0.0018) | no (above)         |
| 100 | t3      | 0.9175 | 0.9344 | 0.8491 | 0.8756 | +0.0684 (0.0019) | beats | +0.0419 (0.0015) | beats | -0.0169 (0.0010) | no (below)         |
| 100 | t5      | 0.6394 | 0.6827 | 0.4798 | 0.5613 | +0.1596 (0.0030) | beats | +0.0782 (0.0022) | beats | -0.0433 (0.0017) | no (below)         |
| 100 | laplace | 0.8812 | 0.9122 | 0.8285 | 0.7993 | +0.0527 (0.0020) | beats | +0.0819 (0.0021) | beats | -0.0310 (0.0013) | no (below)         |
| 100 | cont10  | 0.8258 | 0.8351 | 0.6778 | 0.7992 | +0.1480 (0.0028) | beats | +0.0266 (0.0015) | beats | -0.0093 (0.0013) | no (below)         |
| 100 | cont5   | 0.8790 | 0.8776 | 0.8014 | 0.8751 | +0.0776 (0.0020) | beats | +0.0039 (0.0009) | beats | +0.0014 (0.0010) | yes                |

## Answer to the direction (seed 92101, partner W)

1. **Chi-square(5) vs AD:** beats at every n (+4.9, +5.5, +0.9 points), where the |b1| partner
   lost at n=50 and 100. **Vs Shapiro-Wilk:** still loses at every n (-3.3, -3.4, -0.1 points);
   the n=100 loss is one tenth of a point but 5 paired SE. The W partner closes about half the
   remaining gap the |b1| partner left (stuff 2: -6.3, -10.7, -1.6) but a min-p combination that
   contains W cannot match W alone on W's home ground, because the c_n cut (0.033 to 0.039) is
   below the 0.05 W would use on its own.
2. **Heavy tails and contamination vs AD and SW:** beats both on all 15 cells, every n, as with |b1|.
3. **Stays within 2 paired SE of plain S2?** No, on 14 of 15 heavy-tail and contamination cells
   (only cont5 at n=100 ties). The cost is larger than with |b1|: 1.7 to 4.6 points on t3, t5,
   Laplace and cont10 at every n, and 0.4 to 0.9 on cont5 at n=25 and 50. W is a stronger
   second leg on skew and a weaker one on tails, so it dilutes S2 more where S2 is best.

Net across stuff 2 and 3: with either permitted partner the exact-size min-p combination keeps S2's
dominance over AD and SW off-skew, but the direction's two side conditions both fail. The partner
is not weakly correlated with S2 under the null (0.41 to 0.76), and the combination does not stay
within two paired SE of S2 on heavy tails (loses 1 to 5 points). On chi-square(5) the W partner
ties or beats AD everywhere and the |b1| partner does not, yet neither ties Shapiro-Wilk at any n.
The trade is sharp: W as partner buys +3 to +7 points of skew power over the |b1| partner at the
price of a further 1 to 2 points on t3, t5 and Laplace.

## Raw output

The table above is generated from the script's stdout by a parser; the stdout is:

```
n=25 pearson(S2,-W)=0.635 spearman=0.441 c_n=0.0385 size=0.0500 crit={'s2': np.float64(13.396133327403478), 'a2': np.float64(0.7365136193325227), 'w': np.float64(0.9192567059400792)}
25 chi2_5 {'combo': np.float64(0.5139), 's2': np.float64(0.47035), 'a2': np.float64(0.46495), 'w': np.float64(0.54675), 'vs_a2': '+0.0490 (0.0021) beats', 'vs_w': '-0.0328 (0.0014) loses', 'vs_s2': '+0.0436 (0.0018) beats'}
25 t3 {'combo': np.float64(0.43635), 's2': np.float64(0.46195), 'a2': np.float64(0.37685), 'w': np.float64(0.4012), 'vs_a2': '+0.0595 (0.0020) beats', 'vs_w': '+0.0352 (0.0016) beats', 'vs_s2': '-0.0256 (0.0013) loses'}
25 t5 {'combo': np.float64(0.2435), 's2': np.float64(0.26335), 'a2': np.float64(0.18975), 'w': np.float64(0.22105), 'vs_a2': '+0.0537 (0.0020) beats', 'vs_w': '+0.0224 (0.0014) beats', 'vs_s2': '-0.0198 (0.0013) loses'}
25 laplace {'combo': np.float64(0.35315), 's2': np.float64(0.38875), 'a2': np.float64(0.3183), 'w': np.float64(0.30835), 'vs_a2': '+0.0348 (0.0021) beats', 'vs_w': '+0.0448 (0.0017) beats', 'vs_s2': '-0.0356 (0.0014) loses'}
25 cont10 {'combo': np.float64(0.3656), 's2': np.float64(0.384), 'a2': np.float64(0.29495), 'w': np.float64(0.34645), 'vs_a2': '+0.0706 (0.0020) beats', 'vs_w': '+0.0192 (0.0013) beats', 'vs_s2': '-0.0184 (0.0012) loses'}
25 cont5 {'combo': np.float64(0.44275), 's2': np.float64(0.45165), 'a2': np.float64(0.3963), 'w': np.float64(0.43455), 'vs_a2': '+0.0464 (0.0018) beats', 'vs_w': '+0.0082 (0.0010) beats', 'vs_s2': '-0.0089 (0.0010) loses'}
n=50 pearson(S2,-W)=0.524 spearman=0.355 c_n=0.0348 size=0.0500 crit={'s2': np.float64(26.50860299377608), 'a2': np.float64(0.7432881122993524), 'w': np.float64(0.9544003312065223)}
50 chi2_5 {'combo': np.float64(0.85855), 's2': np.float64(0.7281), 'a2': np.float64(0.80325), 'w': np.float64(0.89225), 'vs_a2': '+0.0553 (0.0019) beats', 'vs_w': '-0.0337 (0.0013) loses', 'vs_s2': '+0.1305 (0.0026) beats'}
50 t3 {'combo': np.float64(0.69115), 's2': np.float64(0.72485), 'a2': np.float64(0.6032), 'w': np.float64(0.6411), 'vs_a2': '+0.0880 (0.0023) beats', 'vs_w': '+0.0501 (0.0018) beats', 'vs_s2': '-0.0337 (0.0014) loses'}
50 t5 {'combo': np.float64(0.40325), 's2': np.float64(0.4355), 'a2': np.float64(0.30085), 'w': np.float64(0.35785), 'vs_a2': '+0.1024 (0.0025) beats', 'vs_w': '+0.0454 (0.0019) beats', 'vs_s2': '-0.0323 (0.0015) loses'}
50 laplace {'combo': np.float64(0.60895), 's2': np.float64(0.655), 'a2': np.float64(0.54735), 'w': np.float64(0.5328), 'vs_a2': '+0.0616 (0.0024) beats', 'vs_w': '+0.0761 (0.0022) beats', 'vs_s2': '-0.0461 (0.0016) loses'}
50 cont10 {'combo': np.float64(0.59395), 's2': np.float64(0.6113), 'a2': np.float64(0.46405), 'w': np.float64(0.56945), 'vs_a2': '+0.1299 (0.0027) beats', 'vs_w': '+0.0245 (0.0016) beats', 'vs_s2': '-0.0173 (0.0014) loses'}
50 cont5 {'combo': np.float64(0.6637), 's2': np.float64(0.6677), 'a2': np.float64(0.5875), 'w': np.float64(0.65975), 'vs_a2': '+0.0762 (0.0021) beats', 'vs_w': '+0.0040 (0.0011) beats', 'vs_s2': '-0.0040 (0.0011) loses'}
n=100 pearson(S2,-W)=0.409 spearman=0.281 c_n=0.0326 size=0.0500 crit={'s2': np.float64(52.7087370866728), 'a2': np.float64(0.7488546648959901), 'w': np.float64(0.9745549086280316)}
100 chi2_5 {'combo': np.float64(0.99715), 's2': np.float64(0.93215), 'a2': np.float64(0.9877), 'w': np.float64(0.9982), 'vs_a2': '+0.0094 (0.0007) beats', 'vs_w': '-0.0010 (0.0002) loses', 'vs_s2': '+0.0650 (0.0018) beats'}
100 t3 {'combo': np.float64(0.9175), 's2': np.float64(0.93435), 'a2': np.float64(0.84915), 'w': np.float64(0.87555), 'vs_a2': '+0.0684 (0.0019) beats', 'vs_w': '+0.0419 (0.0015) beats', 'vs_s2': '-0.0169 (0.0010) loses'}
100 t5 {'combo': np.float64(0.63945), 's2': np.float64(0.6827), 'a2': np.float64(0.4798), 'w': np.float64(0.56125), 'vs_a2': '+0.1596 (0.0030) beats', 'vs_w': '+0.0782 (0.0022) beats', 'vs_s2': '-0.0433 (0.0017) loses'}
100 laplace {'combo': np.float64(0.88125), 's2': np.float64(0.9122), 'a2': np.float64(0.8285), 'w': np.float64(0.7993), 'vs_a2': '+0.0527 (0.0020) beats', 'vs_w': '+0.0819 (0.0021) beats', 'vs_s2': '-0.0310 (0.0013) loses'}
100 cont10 {'combo': np.float64(0.8258), 's2': np.float64(0.8351), 'a2': np.float64(0.67785), 'w': np.float64(0.7992), 'vs_a2': '+0.1480 (0.0028) beats', 'vs_w': '+0.0266 (0.0015) beats', 'vs_s2': '-0.0093 (0.0013) loses'}
100 cont5 {'combo': np.float64(0.879), 's2': np.float64(0.87755), 'a2': np.float64(0.80135), 'w': np.float64(0.87515), 'vs_a2': '+0.0776 (0.0020) beats', 'vs_w': '+0.0039 (0.0009) beats', 'vs_s2': '+0.0014 (0.0010) tie'}
```
