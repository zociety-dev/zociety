# Cycle 90: c=2 capped AD sum vs plain Anderson-Darling vs Shapiro-Wilk (seed 90101)

Script: `stuff/s2-vs-ad-vs-sw-seed90101.py` (run with `uv run --with numpy --with scipy python ...`, 26 s).

## Definitions (rule 1)

For a sample x_1..x_n, let z_(1) <= ... <= z_(n) be the order statistics of the
sample-standardized values (x - mean)/sd, sd with n-1. The Anderson-Darling term is

    t_i = -((2i-1)/n) * [ ln Phi(z_(i)) + ln(1 - Phi(z_(n+1-i))) ],  i = 1..n.

The three competing statistics:

- **S2** (capped AD sum, c=2): S2 = sum_i log(1 + 2 t_i) / 2. Reject for large S2.
- **A2** (plain Anderson-Darling): A2 = sum_i t_i - n. Reject for large A2.
- **W** (Shapiro-Wilk, scipy.stats.shapiro): reject for small W.

Each statistic gets its own normal-calibrated 5% critical value: the 95th
percentile of S2 and A2 and the 5th percentile of W over the same 20000
N(0,1) samples per n. All three tests are then applied to the same simulated
samples under every law, so differences are paired. The paired Monte Carlo SE
is sd(d_j)/sqrt(20000) where d_j is the difference of the per-sample 0/1
rejection indicators.

Seed 90101 (numpy default_rng), 20000 sims per (n, law), n in 25, 50, 100.
Laws: normal, t(3), t(5), 0.9 N(0,1) + 0.1 N(0,9) (per-observation mixture),
chi-square(5).

## Results

| n | law | rej S2 | rej A2 | rej W | S2-A2 | SE | S2 vs A2 | S2-W | SE | S2 vs W |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | normal | 0.0500 | 0.0500 | 0.0500 | +0.0000 | 0.0014 | size | +0.0000 | 0.0013 | size |
| 25 | t(3) | 0.4655 | 0.3756 | 0.4001 | +0.0899 | 0.0022 | win | +0.0654 | 0.0019 | win |
| 25 | t(5) | 0.2628 | 0.1885 | 0.2193 | +0.0743 | 0.0021 | win | +0.0436 | 0.0018 | win |
| 25 | 0.9N(0,1)+0.1N(0,9) | 0.3868 | 0.2945 | 0.3471 | +0.0922 | 0.0022 | win | +0.0398 | 0.0017 | win |
| 25 | chi2(5) | 0.4767 | 0.4717 | 0.5523 | +0.0050 | 0.0025 | tie | -0.0756 | 0.0021 | loss |
| 50 | normal | 0.0500 | 0.0500 | 0.0500 | +0.0000 | 0.0016 | size | +0.0000 | 0.0015 | size |
| 50 | t(3) | 0.7259 | 0.6050 | 0.6381 | +0.1208 | 0.0024 | win | +0.0877 | 0.0022 | win |
| 50 | t(5) | 0.4399 | 0.3049 | 0.3579 | +0.1351 | 0.0026 | win | +0.0820 | 0.0023 | win |
| 50 | 0.9N(0,1)+0.1N(0,9) | 0.6004 | 0.4582 | 0.5551 | +0.1422 | 0.0026 | win | +0.0453 | 0.0020 | win |
| 50 | chi2(5) | 0.7301 | 0.8068 | 0.8900 | -0.0767 | 0.0025 | loss | -0.1598 | 0.0026 | loss |
| 100 | normal | 0.0500 | 0.0500 | 0.0500 | +0.0000 | 0.0017 | size | +0.0000 | 0.0017 | size |
| 100 | t(3) | 0.9353 | 0.8482 | 0.8772 | +0.0871 | 0.0020 | win | +0.0581 | 0.0017 | win |
| 100 | t(5) | 0.6815 | 0.4794 | 0.5643 | +0.2020 | 0.0029 | win | +0.1172 | 0.0026 | win |
| 100 | 0.9N(0,1)+0.1N(0,9) | 0.8373 | 0.6778 | 0.8012 | +0.1595 | 0.0026 | win | +0.0362 | 0.0019 | win |
| 100 | chi2(5) | 0.9298 | 0.9849 | 0.9973 | -0.0550 | 0.0017 | loss | -0.0674 | 0.0018 | loss |

"win" = S2 minus competitor exceeds +2 SE; "tie" = within 2 SE; "loss" = below -2 SE.
Normal rows are size checks: all three tests sit at exactly 0.0500 by construction
(critical values are quantiles of these same samples), so the difference is 0.

## Classification per n and law (rule 2)

- **t(3)**: S2 beats A2 and beats W at n=25, 50, 100 (41, 50, 44 SE over A2; 34, 40, 34 SE over W).
- **t(5)**: S2 beats A2 and beats W at n=25, 50, 100 (35, 52, 70 SE over A2; 24, 36, 45 SE over W).
- **0.9 N(0,1) + 0.1 N(0,9)**: S2 beats A2 and beats W at n=25, 50, 100 (42, 55, 61 SE over A2; 23, 23, 19 SE over W).
- **chi-square(5)**: S2 ties A2 at n=25 (+2.0 SE, inside the 2 SE band), loses to A2 at n=50 (-31 SE) and n=100 (-33 SE); S2 loses to W at every n (-36, -61, -37 SE).

## Overall verdict

S2 loses most to A2 at chi-square(5), n=100 (-0.055, -33 SE; n=50 is nearly as bad at -0.077, -31 SE), and loses most to W at chi-square(5), n=50 (-0.160, -61 SE). It loses nowhere else: on every symmetric heavy-tailed or contaminated law it wins over both competitors by 19 to 70 SE. The cap at c=2 buys its heavy-tail power by damping the few extreme t_i that a one-sided skewed tail produces, which is exactly the signal A2 and W use to detect chi-square(5).

**One sentence:** The c=2 capped AD sum is worth using over plain AD and over Shapiro-Wilk only when the alternative is symmetric heavy tails or contamination, where it wins by 4 to 20 points of power at every n; it is not worth using as a general-purpose normality test, because under the skewed chi-square(5) law it loses 5 to 8 points to plain AD at n >= 50 and 7 to 16 points to Shapiro-Wilk at every n.
