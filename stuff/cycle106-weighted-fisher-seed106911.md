# Cycle 106: weighted Fisher of SW and S2, seed 106911

Statistic: F_w = -2[w ln p_S2 + (1-w) ln p_SW]. p_SW is the Royston (1995) Shapiro-Wilk p-value; p_S2 is the D'Agostino-Pearson K^2 (S2) chi-square(2) p-value. Seed 106911 (new). n=400, 20000 draws per run: one null run calibrates each critical value at its 95th percentile, a separate null run verifies size, and one paired run per alternative. Script: stuff/cycle106-weighted-fisher-seed106911.py. F_0.50 is half of unweighted Fisher, so their rejections coincide (difference 0, disagreement 0).

Caveat: the skewed alternative (skew-normal delta=0.75 divided by sqrt(chi2_10/10)) has a pooled sqrt(beta1) of 0.467 over 100000 draws, not 0.3. It is more skewed than the direction asks, so the skewed-alternative verdicts need a rerun at a smaller delta.

Raw output (critical value, verify-run N(0,1) rejection rate, binomial SE; then power, and paired diff / paired SE / disagreement fraction):

```
SEED 106911 DELTA 0.75
CRIT
SW p < 0.05034 0.0537 0.0016
S2 p < 0.04914 0.0525 0.0016
F stat > 11.6677 0.0518 0.0016
F0.25 stat > 5.8517 0.0529 0.0016
F0.50 stat > 5.8338 0.0518 0.0016
F0.75 stat > 5.8871 0.0530 0.0016
ALT t5
 power SW 0.9736 0.0011
 power S2 0.9744 0.0011
 power F 0.9764 0.0011
 power F0.25 0.9757 0.0011
 power F0.50 0.9764 0.0011
 power F0.75 0.9758 0.0011
 diff F - S2 +0.0021 0.0006 disagree 0.0066 +3.6SE
 diff F - SW +0.0028 0.0006 disagree 0.0073 +4.6SE
 diff F0.25 - S2 +0.0013 0.0007 disagree 0.0102 +1.8SE
 diff F0.25 - SW +0.0021 0.0004 disagree 0.0037 +4.8SE
 diff F0.25 - F -0.0008 0.0004 disagree 0.0037 -1.8SE
 diff F0.50 - S2 +0.0021 0.0006 disagree 0.0066 +3.6SE
 diff F0.50 - SW +0.0028 0.0006 disagree 0.0073 +4.6SE
 diff F0.50 - F +0.0000 0.0000 disagree 0.0000 +0.0SE
 diff F0.75 - S2 +0.0015 0.0004 disagree 0.0035 +3.6SE
 diff F0.75 - SW +0.0022 0.0007 disagree 0.0103 +3.1SE
 diff F0.75 - F -0.0006 0.0004 disagree 0.0031 -1.4SE
ALT skt10
 power SW 0.8927 0.0022
 power S2 0.9073 0.0021
 power F 0.9066 0.0021
 power F0.25 0.9024 0.0021
 power F0.50 0.9066 0.0021
 power F0.75 0.9089 0.0020
 diff F - S2 -0.0008 0.0010 disagree 0.0192 -0.8SE
 diff F - SW +0.0139 0.0010 disagree 0.0218 +13.4SE
 diff F0.25 - S2 -0.0049 0.0012 disagree 0.0284 -4.1SE
 diff F0.25 - SW +0.0097 0.0008 disagree 0.0123 +12.5SE
 diff F0.25 - F -0.0042 0.0007 disagree 0.0097 -5.9SE
 diff F0.50 - S2 -0.0008 0.0010 disagree 0.0192 -0.8SE
 diff F0.50 - SW +0.0139 0.0010 disagree 0.0218 +13.4SE
 diff F0.50 - F +0.0000 0.0000 disagree 0.0000 +0.0SE
 diff F0.75 - S2 +0.0015 0.0007 disagree 0.0101 +2.1SE
 diff F0.75 - SW +0.0162 0.0012 disagree 0.0307 +13.1SE
 diff F0.75 - F +0.0022 0.0007 disagree 0.0091 +3.3SE
pooled sqrt(beta1) skt10 over 100000 draws: 0.467
```

Verdicts (beats S2 beyond 2 paired SE on skt10 AND leads both SW and S2 on t5):
- w=0.25: no. -0.0049 vs S2 on skt10 (-4.1 SE); on t5 +0.0013 vs S2 is only 1.8 SE.
- w=0.50: no. -0.0008 vs S2 on skt10 (-0.8 SE), the same as unweighted Fisher; leads both on t5 (+3.6/+4.6 SE).
- w=0.75: yes, barely. +0.0015 vs S2 on skt10 (+2.1 SE, disagreement 0.0101) and leads on t5 (+3.6 SE vs S2, +3.1 SE vs SW).

Ranking on skt10: w=0.75 (0.9089) > w=0.50 (0.9066) > w=0.25 (0.9024). The ordering is monotone in w.
