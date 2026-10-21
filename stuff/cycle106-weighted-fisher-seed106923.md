# Cycle 106: weighted Fisher, seed 106923, DELTA 0.68

Rerun of seed106911 with a new seed (106923, not used in cycles 100-105) and a smaller skew-normal shape (DELTA 0.68 instead of 0.75; DELTA is now argv 2). Script: `stuff/cycle106-weighted-fisher-seed106923.py`, run as `python3 stuff/cycle106-weighted-fisher-seed106923.py 106923 0.68` (60 s).

Statistic: F_w = -2[w ln p_S2 + (1-w) ln p_SW], with p_SW from Royston (1992) log(1-W) normal approximation and p_S2 = exp(-(Z1^2+Z2^2)/2) from the D'Agostino-Pearson K^2 (chi^2 df 2). Unweighted Fisher is -2[ln p_S2 + ln p_SW] (F0.50 is exactly half of it, so identical rejections). Critical values: 95th percentile of a 20000-draw N(0,1) calibration run; rejection rates below are from a separate 20000-draw null run. Paired SE = sd of per-draw rejection differences / sqrt(20000).

## Raw output

```
SEED 106923 DELTA 0.68
CRIT
SW p < 0.04777 0.0488 0.0015
S2 p < 0.04501 0.0467 0.0015
F stat > 11.9709 0.0469 0.0015
F0.25 stat > 5.9674 0.0485 0.0015
F0.50 stat > 5.9854 0.0469 0.0015
F0.75 stat > 6.0634 0.0459 0.0015
ALT t5
 power SW 0.9721 0.0012
 power S2 0.9729 0.0011
 power F 0.9749 0.0011
 power F0.25 0.9745 0.0011
 power F0.50 0.9749 0.0011
 power F0.75 0.9749 0.0011
 diff F - S2 +0.0020 0.0006 disagree 0.0078 +3.2SE
 diff F - SW +0.0027 0.0006 disagree 0.0066 +4.8SE
 diff F0.25 - S2 +0.0016 0.0007 disagree 0.0111 +2.1SE
 diff F0.25 - SW +0.0024 0.0004 disagree 0.0034 +5.7SE
 diff F0.25 - F -0.0004 0.0004 disagree 0.0033 -1.0SE
 diff F0.50 - S2 +0.0020 0.0006 disagree 0.0078 +3.2SE
 diff F0.50 - SW +0.0027 0.0006 disagree 0.0066 +4.8SE
 diff F0.50 - F +0.0000 0.0000 disagree 0.0000 +0.0SE
 diff F0.75 - S2 +0.0021 0.0004 disagree 0.0040 +4.6SE
 diff F0.75 - SW +0.0028 0.0007 disagree 0.0103 +3.9SE
 diff F0.75 - F +0.0001 0.0004 disagree 0.0037 +0.1SE
ALT skt10
 power SW 0.8127 0.0028
 power S2 0.8282 0.0027
 power F 0.8294 0.0027
 power F0.25 0.8248 0.0027
 power F0.50 0.8294 0.0027
 power F0.75 0.8302 0.0027
 diff F - S2 +0.0011 0.0012 disagree 0.0302 +0.9SE
 diff F - SW +0.0167 0.0013 disagree 0.0326 +13.1SE
 diff F0.25 - S2 -0.0034 0.0015 disagree 0.0460 -2.2SE
 diff F0.25 - SW +0.0121 0.0009 disagree 0.0170 +13.2SE
 diff F0.25 - F -0.0046 0.0009 disagree 0.0158 -5.1SE
 diff F0.50 - S2 +0.0011 0.0012 disagree 0.0302 +0.9SE
 diff F0.50 - SW +0.0167 0.0013 disagree 0.0326 +13.1SE
 diff F0.50 - F +0.0000 0.0000 disagree 0.0000 +0.0SE
 diff F0.75 - S2 +0.0020 0.0009 disagree 0.0152 +2.3SE
 diff F0.75 - SW +0.0175 0.0015 disagree 0.0474 +11.4SE
 diff F0.75 - F +0.0008 0.0009 disagree 0.0150 +1.0SE
pooled sqrt(beta1) skt10 over 100000 draws: 0.399
```

## Verdicts (one line per weight)

- w=0.25: NO. Skewed: -0.0034 vs S2 (-2.2 paired SE). t df 5: leads S2 +2.1 SE and SW +5.7 SE.
- w=0.50: NO. Skewed: +0.0011 vs S2 (+0.9 SE). t df 5: leads S2 +3.2 SE, SW +4.8 SE. Same draws as unweighted Fisher.
- w=0.75: YES. Skewed: +0.0020 vs S2 (+2.3 SE, disagree 1.52%). t df 5: leads S2 +4.6 SE, SW +3.9 SE.

Ranking on skewed alternative: 0.75 (0.8302) > 0.50 (0.8294) > 0.25 (0.8248), monotone in w, same as seed 106911.

## Caveat

Measured pooled sqrt(beta1) of the skewed alternative is 0.399 (100000 draws), still above the ~0.3 target, though closer than 0.467 at DELTA 0.75. A skew-normal moment calculation puts DELTA ~0.63 nearer 0.3; not run this turn. The w=0.75 margin (+2.3 SE) agrees with seed 106911 (+2.1 SE) but is barely past the threshold.
