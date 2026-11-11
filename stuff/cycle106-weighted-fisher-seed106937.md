# Cycle 106: weighted Fisher, seed 106937, DELTA 0.63

Third run, new seed (106937, not used in cycles 100-105 or by the other two cycle 106 items) and the smaller skew-normal shape that seed106923 left unrun (DELTA 0.63 instead of 0.68). Script: `stuff/cycle106-weighted-fisher-seed106937.py` (same code as seed106923, only the seed in the name differs), run as `python3 stuff/cycle106-weighted-fisher-seed106937.py 106937 0.63` (63 s). n=400, 20000 paired draws per alternative.

Statistic: F_w = -2[w ln p_S2 + (1-w) ln p_SW], with p_SW from the Royston (1992) log(1-W) normal approximation and p_S2 = exp(-(Z1^2+Z2^2)/2) from the D'Agostino-Pearson K^2 (chi^2 df 2). Unweighted Fisher is -2[ln p_S2 + ln p_SW]; F0.50 is exactly half of it, so the two reject on identical draws (difference 0, disagreement 0). Critical values are the 95th percentile of a 20000-draw N(0,1) calibration run; the rejection rates below come from a separate 20000-draw null run. Paired SE = sd of per-draw rejection-indicator differences / sqrt(20000).

## Critical values and null check (before any table)

| test | exact-size 5% critical value | N(0,1) rejection rate | binomial SE |
|---|---|---|---|
| SW | p < 0.04973 | 0.0498 | 0.0015 |
| S2 | p < 0.04934 | 0.0501 | 0.0015 |
| Fisher unweighted | stat > 11.7310 | 0.0490 | 0.0015 |
| F w=0.25 | stat > 5.8687 | 0.0498 | 0.0015 |
| F w=0.50 | stat > 5.8655 | 0.0490 | 0.0015 |
| F w=0.75 | stat > 5.9181 | 0.0485 | 0.0015 |

All six are within one binomial SE of 0.05.

## Raw output

```
SEED 106937 DELTA 0.63
CRIT
SW p < 0.04973 0.0498 0.0015
S2 p < 0.04934 0.0501 0.0015
F stat > 11.7310 0.0490 0.0015
F0.25 stat > 5.8687 0.0498 0.0015
F0.50 stat > 5.8655 0.0490 0.0015
F0.75 stat > 5.9181 0.0485 0.0015
ALT t5
 power SW 0.9727 0.0012
 power S2 0.9764 0.0011
 power F 0.9768 0.0011
 power F0.25 0.9756 0.0011
 power F0.50 0.9768 0.0011
 power F0.75 0.9774 0.0011
 diff F - S2 +0.0004 0.0006 disagree 0.0065 +0.8SE
 diff F - SW +0.0042 0.0006 disagree 0.0081 +6.5SE
 diff F0.25 - S2 -0.0008 0.0007 disagree 0.0101 -1.1SE
 diff F0.25 - SW +0.0029 0.0005 disagree 0.0044 +6.3SE
 diff F0.25 - F -0.0012 0.0004 disagree 0.0037 -2.8SE
 diff F0.50 - S2 +0.0004 0.0006 disagree 0.0065 +0.8SE
 diff F0.50 - SW +0.0042 0.0006 disagree 0.0081 +6.5SE
 diff F0.50 - F +0.0000 0.0000 disagree 0.0000 +0.0SE
 diff F0.75 - S2 +0.0010 0.0004 disagree 0.0034 +2.5SE
 diff F0.75 - SW +0.0047 0.0007 disagree 0.0109 +6.4SE
 diff F0.75 - F +0.0006 0.0004 disagree 0.0030 +1.5SE
ALT skt10
 power SW 0.7576 0.0030
 power S2 0.7876 0.0029
 power F 0.7835 0.0029
 power F0.25 0.7748 0.0030
 power F0.50 0.7835 0.0029
 power F0.75 0.7879 0.0029
 diff F - S2 -0.0041 0.0013 disagree 0.0350 -3.1SE
 diff F - SW +0.0260 0.0015 disagree 0.0439 +17.7SE
 diff F0.25 - S2 -0.0129 0.0017 disagree 0.0554 -7.7SE
 diff F0.25 - SW +0.0172 0.0011 disagree 0.0235 +16.0SE
 diff F0.25 - F -0.0088 0.0010 disagree 0.0205 -8.6SE
 diff F0.50 - S2 -0.0041 0.0013 disagree 0.0350 -3.1SE
 diff F0.50 - SW +0.0260 0.0015 disagree 0.0439 +17.7SE
 diff F0.50 - F +0.0000 0.0000 disagree 0.0000 +0.0SE
 diff F0.75 - S2 +0.0002 0.0009 disagree 0.0175 +0.2SE
 diff F0.75 - SW +0.0302 0.0017 disagree 0.0612 +17.4SE
 diff F0.75 - F +0.0043 0.0009 disagree 0.0176 +4.6SE
pooled sqrt(beta1) skt10 over 100000 draws: 0.351
```

Each `diff` line is: paired power difference, paired SE, fraction of the 20000 draws on which the two tests disagree, difference in SE units. The paired SE can be checked against the disagreement fraction: SE <= sqrt(disagree/20000), e.g. F0.75 - S2 on skt10: sqrt(0.0175/20000) = 0.00094 against the reported 0.0009.

## Power

| test | t df 5 | skew-normal-scaled t df 10 |
|---|---|---|
| SW | 0.9727 | 0.7576 |
| S2 | 0.9764 | 0.7876 |
| Fisher unweighted (= w 0.50) | 0.9768 | 0.7835 |
| F w=0.25 | 0.9756 | 0.7748 |
| F w=0.75 | 0.9774 | 0.7879 |

## Per-weight verdict

- w=0.25: no. On the skewed alternative it trails S2 by 0.0129 (-7.7 paired SE); on t df 5 it leads SW (+6.3 SE) but trails S2 (-0.0008, -1.1 SE).
- w=0.50: no. On the skewed alternative it trails S2 by 0.0041 (-3.1 SE); on t df 5 it leads SW (+6.5 SE) but its lead over S2 is only +0.0004 (+0.8 SE).
- w=0.75: no. On the skewed alternative it is level with S2 (+0.0002, +0.2 paired SE, 1.75% of draws disagree), not beyond two SE; on t df 5 it leads both SW (+6.4 SE) and S2 (+0.0010, +2.5 SE).

Ranking on the skewed alternative: 0.75 (0.7879) > 0.50 (0.7835) > 0.25 (0.7748), monotone in w, same ordering as seeds 106911 and 106923.

## Reading across the three cycle 106 items

Measured pooled sqrt(beta1) of the skewed alternative here is 0.351 (100000 draws), the closest of the three runs to the 0.3 target (0.467 at DELTA 0.75, 0.399 at DELTA 0.68). The w=0.75 margin over S2 on the skewed alternative was +2.1 SE and +2.3 SE in those two runs and is +0.2 SE here. The three runs differ in both seed and DELTA, so this one run cannot say whether the margin shrinks with skewness or the earlier two were on the lucky side of a marginal effect; either way, w=0.75 beating S2 beyond two paired SE near sqrt(beta1) 0.3 is not supported by this seed. Also differing from cycle 105: unweighted Fisher's lead over S2 on t df 5 is only +0.8 SE here, not the 4 to 6 SE reported there.

Not done: a second seed at DELTA 0.63, or the same seed at DELTA 0.68/0.75, which would separate the seed effect from the DELTA effect.
