# Cycle 88, member-1: third seed, both per-term scales, paired SEs on the t(3) gain

Author: member-1. Seed 2026102111 (fresh; numpy default_rng; member-2 used 2026102188, member-3 used 2026102103). 20000 sims per n. Script: stuff/c88_member1_third_seed.py (run with `uv run --with numpy --with scipy python stuff/c88_member1_third_seed.py`; about 2 s). This is the third independent replicate of the cycle 88 direction, so the three-seed agreement can be read off directly.

## Per-term scales (defined before any table)

Let x_1..x_n be the sample. Standardize by the sample's own mean and SD (ddof=1): z_j = (x_j - xbar) / s. Let z_(1) <= ... <= z_(n) be the order statistics and Phi the standard normal CDF.

- **AD scale.** t_i = -((2i-1)/n) * [ln Phi(z_(i)) + ln(1 - Phi(z_(n+1-i)))], i = 1..n. The uncapped sum is sum_i t_i = A^2 + n, the Anderson-Darling statistic shifted by n, so c=0 is exactly the AD test on standardized data. Every t_i > 0.
- **x^2 scale.** t_i = z_i^2 on the same standardized sample (unordered; the sum is permutation invariant). The uncapped sum is sum_i z_i^2 = n-1 identically, so c=0 on this scale is a constant and has no power at all.

For each scale the statistic is G_c = sum_i log(1 + c t_i) / c for c in 1, 5, 20, 40, and G_0 = sum_i t_i. Rejection is one-sided, G_c > crit_c, with crit_c the 95th percentile of G_c under the normal law from the same 20000 normal sims at that n (normal-calibrated 5% size). Laws: normal, t(3), t(5), and the mixture 0.9 N(0,1) + 0.1 N(0,9) drawn as z scaled by 3 with probability 0.1. The same 20000 draws per (n, law) are used for every c, so the t(3) gain over c=0 is paired: d_s = 1[reject_c] - 1[reject_0] per sim, gain = mean(d), paired SE = sd(d)/sqrt(20000).

## Which (scale, c) pairs gain t(3) power over c=0 by more than two paired SE at every n

- **AD, c=1: YES.** Gains +0.073, +0.114, +0.076 at n = 25, 50, 100; SEs 0.0020-0.0023, so 36, 50 and 40 SE.
- **AD, c=5: YES.** Gains +0.064, +0.116, +0.075; 28, 46 and 38 SE.
- **AD, c=20: YES.** Gains +0.018, +0.065, +0.051; SEs 0.0024, 0.0026, 0.0020, so 7.3, 25 and 26 SE. The n=25 gain is the smallest of any clearing pair.
- **AD, c=40: no.** Gain -0.005 at n=25 (SE 0.0026, below zero by 1.8 SE); +0.025 and +0.027 at n = 50 and 100 clear, but the every-n criterion fails.
- **x^2, c in 1, 5, 20, 40: none.** The c=0 reference is the constant n-1, so its "power" (0.012-0.035 across laws) is floating-point tie noise around the constant, not a test. Every capped x^2 statistic has t(3) power 0.000-0.002, far below the 5% size, so the paired gains are negative (-0.011 to -0.035) at every n. No x^2 pair clears.

## Verdict on cycle 86's c=20 gain

**Recovered under the AD scale only.** AD c=20 beats c=0 by more than seven paired SE at every n (+0.018, +0.065, +0.051). It is not the best cap: c=1 and c=5 beat c=20 at every n by 0.025-0.055, and c=40 has already lost the gain at n=25. **Not recovered under the x^2 scale**: there c=0 is degenerate and every cap drives t(3) power below size, because the cap is concave on terms forced to sum to n-1, so heavy tails shrink G_c instead of growing it. The sign of cycle 86's result is decided entirely by the per-term scale, as the cycle 87 learning said.

## Three-seed agreement

AD c=20 t(3) gains across the three cycle 88 seeds: member-2 (+0.024, +0.063, +0.055), member-3 (within about one SE of member-2 per its own note), member-1 (+0.018, +0.065, +0.051). The n=25 difference between member-2 and this run is 0.0065 against a combined SE of about 0.0034, about 1.9 SE; n=50 and n=100 agree within one SE. The verdict table below is identical across all three seeds: AD c in 1, 5, 20 clear at every n, AD c=40 fails at n=25, no x^2 pair clears. Seed luck is ruled out for the sign and for the ranking c=1 ~ c=5 > c=20 > c=40 under AD.

## Also visible in the rows

- AD c=0 power under t(5) and the mixture is 0.20/0.30 (n=25), 0.30/0.45 (n=50), 0.49/0.68 (n=100); c=5 lifts these to 0.25/0.38, 0.44/0.62, 0.69/0.85, so the cap helps on every heavy-tailed law, not only t(3). c=20 gives less lift than c=5 everywhere except mix at n=100 (0.852 vs 0.850, within noise).
- Under the normal law every AD and x^2 capped row shows power 0.0500 by construction (calibration on the same sims).

## Full rows: one per (scale, c, n, law)

Power is the normal-calibrated 5% rejection rate. The gain and paired SE columns are filled for t(3) only; c=0 rows carry gain 0 by definition.

| scale | c | n | law | power | t3 gain vs c=0 | paired SE |
|---|---|---|---|---|---|---|
| ad | 0 | 25 | normal | 0.0500 |  |  |
| ad | 0 | 25 | t3 | 0.3832 | +0.0000 | 0.0000 |
| ad | 0 | 25 | t5 | 0.1965 |  |  |
| ad | 0 | 25 | mix | 0.2959 |  |  |
| ad | 1 | 25 | normal | 0.0500 |  |  |
| ad | 1 | 25 | t3 | 0.4558 | +0.0726 | 0.0020 |
| ad | 1 | 25 | t5 | 0.2525 |  |  |
| ad | 1 | 25 | mix | 0.3674 |  |  |
| ad | 5 | 25 | normal | 0.0500 |  |  |
| ad | 5 | 25 | t3 | 0.4470 | +0.0638 | 0.0023 |
| ad | 5 | 25 | t5 | 0.2541 |  |  |
| ad | 5 | 25 | mix | 0.3815 |  |  |
| ad | 20 | 25 | normal | 0.0500 |  |  |
| ad | 20 | 25 | t3 | 0.4007 | +0.0175 | 0.0024 |
| ad | 20 | 25 | t5 | 0.2304 |  |  |
| ad | 20 | 25 | mix | 0.3562 |  |  |
| ad | 40 | 25 | normal | 0.0500 |  |  |
| ad | 40 | 25 | t3 | 0.3785 | -0.0047 | 0.0026 |
| ad | 40 | 25 | t5 | 0.2194 |  |  |
| ad | 40 | 25 | mix | 0.3384 |  |  |
| ad | 0 | 50 | normal | 0.0500 |  |  |
| ad | 0 | 50 | t3 | 0.5968 | +0.0000 | 0.0000 |
| ad | 0 | 50 | t5 | 0.2983 |  |  |
| ad | 0 | 50 | mix | 0.4539 |  |  |
| ad | 1 | 50 | normal | 0.0500 |  |  |
| ad | 1 | 50 | t3 | 0.7110 | +0.1143 | 0.0023 |
| ad | 1 | 50 | t5 | 0.4285 |  |  |
| ad | 1 | 50 | mix | 0.5841 |  |  |
| ad | 5 | 50 | normal | 0.0500 |  |  |
| ad | 5 | 50 | t3 | 0.7126 | +0.1158 | 0.0025 |
| ad | 5 | 50 | t5 | 0.4419 |  |  |
| ad | 5 | 50 | mix | 0.6176 |  |  |
| ad | 20 | 50 | normal | 0.0500 |  |  |
| ad | 20 | 50 | t3 | 0.6618 | +0.0650 | 0.0026 |
| ad | 20 | 50 | t5 | 0.4057 |  |  |
| ad | 20 | 50 | mix | 0.6064 |  |  |
| ad | 40 | 50 | normal | 0.0500 |  |  |
| ad | 40 | 50 | t3 | 0.6221 | +0.0254 | 0.0027 |
| ad | 40 | 50 | t5 | 0.3756 |  |  |
| ad | 40 | 50 | mix | 0.5826 |  |  |
| ad | 0 | 100 | normal | 0.0500 |  |  |
| ad | 0 | 100 | t3 | 0.8596 | +0.0000 | 0.0000 |
| ad | 0 | 100 | t5 | 0.4865 |  |  |
| ad | 0 | 100 | mix | 0.6796 |  |  |
| ad | 1 | 100 | normal | 0.0500 |  |  |
| ad | 1 | 100 | t3 | 0.9351 | +0.0755 | 0.0019 |
| ad | 1 | 100 | t5 | 0.6698 |  |  |
| ad | 1 | 100 | mix | 0.8168 |  |  |
| ad | 5 | 100 | normal | 0.0500 |  |  |
| ad | 5 | 100 | t3 | 0.9348 | +0.0752 | 0.0020 |
| ad | 5 | 100 | t5 | 0.6870 |  |  |
| ad | 5 | 100 | mix | 0.8498 |  |  |
| ad | 20 | 100 | normal | 0.0500 |  |  |
| ad | 20 | 100 | t3 | 0.9106 | +0.0511 | 0.0020 |
| ad | 20 | 100 | t5 | 0.6472 |  |  |
| ad | 20 | 100 | mix | 0.8520 |  |  |
| ad | 40 | 100 | normal | 0.0500 |  |  |
| ad | 40 | 100 | t3 | 0.8868 | +0.0272 | 0.0021 |
| ad | 40 | 100 | t5 | 0.6089 |  |  |
| ad | 40 | 100 | mix | 0.8391 |  |  |
| x2 | 0 | 25 | normal | 0.0080 |  |  |
| x2 | 0 | 25 | t3 | 0.0106 | +0.0000 | 0.0000 |
| x2 | 0 | 25 | t5 | 0.0103 |  |  |
| x2 | 0 | 25 | mix | 0.0101 |  |  |
| x2 | 1 | 25 | normal | 0.0500 |  |  |
| x2 | 1 | 25 | t3 | 0.0064 | -0.0042 | 0.0009 |
| x2 | 1 | 25 | t5 | 0.0146 |  |  |
| x2 | 1 | 25 | mix | 0.0184 |  |  |
| x2 | 5 | 25 | normal | 0.0500 |  |  |
| x2 | 5 | 25 | t3 | 0.0069 | -0.0037 | 0.0009 |
| x2 | 5 | 25 | t5 | 0.0158 |  |  |
| x2 | 5 | 25 | mix | 0.0186 |  |  |
| x2 | 20 | 25 | normal | 0.0500 |  |  |
| x2 | 20 | 25 | t3 | 0.0069 | -0.0036 | 0.0009 |
| x2 | 20 | 25 | t5 | 0.0164 |  |  |
| x2 | 20 | 25 | mix | 0.0200 |  |  |
| x2 | 40 | 25 | normal | 0.0500 |  |  |
| x2 | 40 | 25 | t3 | 0.0071 | -0.0034 | 0.0009 |
| x2 | 40 | 25 | t5 | 0.0169 |  |  |
| x2 | 40 | 25 | mix | 0.0204 |  |  |
| x2 | 0 | 50 | normal | 0.0150 |  |  |
| x2 | 0 | 50 | t3 | 0.0190 | +0.0000 | 0.0000 |
| x2 | 0 | 50 | t5 | 0.0183 |  |  |
| x2 | 0 | 50 | mix | 0.0185 |  |  |
| x2 | 1 | 50 | normal | 0.0500 |  |  |
| x2 | 1 | 50 | t3 | 0.0007 | -0.0183 | 0.0010 |
| x2 | 1 | 50 | t5 | 0.0056 |  |  |
| x2 | 1 | 50 | mix | 0.0072 |  |  |
| x2 | 5 | 50 | normal | 0.0500 |  |  |
| x2 | 5 | 50 | t3 | 0.0009 | -0.0181 | 0.0010 |
| x2 | 5 | 50 | t5 | 0.0063 |  |  |
| x2 | 5 | 50 | mix | 0.0078 |  |  |
| x2 | 20 | 50 | normal | 0.0500 |  |  |
| x2 | 20 | 50 | t3 | 0.0013 | -0.0177 | 0.0010 |
| x2 | 20 | 50 | t5 | 0.0062 |  |  |
| x2 | 20 | 50 | mix | 0.0086 |  |  |
| x2 | 40 | 50 | normal | 0.0500 |  |  |
| x2 | 40 | 50 | t3 | 0.0014 | -0.0175 | 0.0010 |
| x2 | 40 | 50 | t5 | 0.0063 |  |  |
| x2 | 40 | 50 | mix | 0.0088 |  |  |
| x2 | 0 | 100 | normal | 0.0268 |  |  |
| x2 | 0 | 100 | t3 | 0.0347 | +0.0000 | 0.0000 |
| x2 | 0 | 100 | t5 | 0.0356 |  |  |
| x2 | 0 | 100 | mix | 0.0350 |  |  |
| x2 | 1 | 100 | normal | 0.0500 |  |  |
| x2 | 1 | 100 | t3 | 0.0000 | -0.0347 | 0.0013 |
| x2 | 1 | 100 | t5 | 0.0005 |  |  |
| x2 | 1 | 100 | mix | 0.0014 |  |  |
| x2 | 5 | 100 | normal | 0.0500 |  |  |
| x2 | 5 | 100 | t3 | 0.0000 | -0.0347 | 0.0013 |
| x2 | 5 | 100 | t5 | 0.0008 |  |  |
| x2 | 5 | 100 | mix | 0.0019 |  |  |
| x2 | 20 | 100 | normal | 0.0500 |  |  |
| x2 | 20 | 100 | t3 | 0.0000 | -0.0347 | 0.0013 |
| x2 | 20 | 100 | t5 | 0.0013 |  |  |
| x2 | 20 | 100 | mix | 0.0021 |  |  |
| x2 | 40 | 100 | normal | 0.0500 |  |  |
| x2 | 40 | 100 | t3 | 0.0001 | -0.0346 | 0.0013 |
| x2 | 40 | 100 | t5 | 0.0015 |  |  |
| x2 | 40 | 100 | mix | 0.0023 |  |  |

| scale | c | clears 2 SE at n=25,50,100 | every n |
|---|---|---|---|
| ad | 1 | yes, yes, yes | YES |
| ad | 5 | yes, yes, yes | YES |
| ad | 20 | yes, yes, yes | YES |
| ad | 40 | no, yes, yes | no |
| x2 | 1 | no, no, no | no |
| x2 | 5 | no, no, no | no |
| x2 | 20 | no, no, no | no |
| x2 | 40 | no, no, no | no |
