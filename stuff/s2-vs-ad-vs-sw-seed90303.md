# Cycle 90 replication: c=2 capped AD sum vs plain Anderson-Darling vs Shapiro-Wilk (seed 90303)

Script: `stuff/s2-vs-ad-vs-sw-seed90303.py` (run with `uv run --with numpy --with scipy python ...`, 26 s).

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

Seed 90303 (numpy default_rng), 20000 sims per (n, law), n in 25, 50, 100.
Laws: normal, t(3), t(5), 0.9 N(0,1) + 0.1 N(0,9) (per-observation mixture),
chi-square(5).

## Results

| n | law | rej S2 | rej A2 | rej W | S2-A2 | SE | S2 vs A2 | S2-W | SE | S2 vs W |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | normal | 0.0500 | 0.0500 | 0.0500 | +0.0000 | 0.0014 | size | +0.0000 | 0.0013 | size |
| 25 | t(3) | 0.4587 | 0.3875 | 0.4053 | +0.0712 | 0.0021 | win | +0.0534 | 0.0018 | win |
| 25 | t(5) | 0.2545 | 0.1935 | 0.2188 | +0.0611 | 0.0021 | win | +0.0357 | 0.0017 | win |
| 25 | 0.9N(0,1)+0.1N(0,9) | 0.3784 | 0.2982 | 0.3448 | +0.0802 | 0.0022 | win | +0.0335 | 0.0017 | win |
| 25 | chi2(5) | 0.4672 | 0.4736 | 0.5534 | -0.0063 | 0.0025 | loss | -0.0862 | 0.0021 | loss |
| 50 | normal | 0.0500 | 0.0500 | 0.0500 | +0.0000 | 0.0016 | size | +0.0000 | 0.0015 | size |
| 50 | t(3) | 0.7300 | 0.6093 | 0.6390 | +0.1207 | 0.0024 | win | +0.0910 | 0.0022 | win |
| 50 | t(5) | 0.4487 | 0.3100 | 0.3621 | +0.1388 | 0.0027 | win | +0.0866 | 0.0023 | win |
| 50 | 0.9N(0,1)+0.1N(0,9) | 0.6079 | 0.4675 | 0.5614 | +0.1404 | 0.0026 | win | +0.0465 | 0.0021 | win |
| 50 | chi2(5) | 0.7246 | 0.8071 | 0.8873 | -0.0825 | 0.0025 | loss | -0.1628 | 0.0026 | loss |
| 100 | normal | 0.0500 | 0.0500 | 0.0500 | +0.0000 | 0.0017 | size | +0.0000 | 0.0017 | size |
| 100 | t(3) | 0.9368 | 0.8547 | 0.8794 | +0.0822 | 0.0020 | win | +0.0575 | 0.0017 | win |
| 100 | t(5) | 0.6762 | 0.4830 | 0.5589 | +0.1931 | 0.0029 | win | +0.1172 | 0.0026 | win |
| 100 | 0.9N(0,1)+0.1N(0,9) | 0.8353 | 0.6843 | 0.8013 | +0.1510 | 0.0026 | win | +0.0340 | 0.0019 | win |
| 100 | chi2(5) | 0.9283 | 0.9856 | 0.9979 | -0.0573 | 0.0017 | loss | -0.0697 | 0.0018 | loss |

Calls: win = S2 ahead by more than two paired SE, tie = within two SE,
loss = behind by more than two SE; "size" rows are the calibration sample.

## Per-cell verdicts (rule 2)

- t(3), t(5), contaminated normal: S2 beats A2 at every n (+0.061 to +0.193,
  28 to 67 SE) and beats W at every n (+0.034 to +0.117, 18 to 45 SE).
- chi-square(5) vs A2: loss at n=25 (-0.0063, -2.5 SE, only just past the
  two-SE line; seed 90101 called this cell a tie), loss at n=50 (-0.0825,
  -33.0 SE) and n=100 (-0.0573, -34.1 SE).
- chi-square(5) vs W: loss at every n: n=25 -0.0862 (-41 SE), n=50 -0.1628
  (-62.3 SE), n=100 -0.0697 (-38.7 SE).

## Overall verdict

S2 loses anywhere only under chi-square(5). Against A2 the largest drop in
power is at n=50 (-0.083), the largest in SE units at n=100 (-34.1 SE).
Against W the worst cell is chi-square(5) at n=50 (-0.163, -62.3 SE). This
matches seed 90101 cell for cell except chi-square(5) n=25 vs A2, which moves
from tie to a marginal loss, so the sign of that cell is not settled and its
size is under 0.01 either way.

**Sentence for the heap-death learning:** The c=2 capped AD sum is worth
using over both plain AD and Shapiro-Wilk for symmetric heavy-tailed or
scale-contaminated alternatives, where it gains 3 to 19 points of power at
n=25-100, but it is not worth using as a general omnibus test because it
loses to plain AD by up to 8 points and to Shapiro-Wilk by up to 16 points
under chi-square(5).
