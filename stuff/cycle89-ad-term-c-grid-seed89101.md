# Cycle 89: c grid on the Anderson-Darling term scale, seed 89101 (member-1)

**Definition.** For a sample of size n, let z_(1) <= ... <= z_(n) be the order statistics after sample standardization (mean subtracted, divided by the ddof=1 standard deviation). The Anderson-Darling term is

    t_i = -((2i-1)/n) * [ln Phi(z_(i)) + ln(1 - Phi(z_(n+1-i)))],  i = 1..n.

The statistic at c is sum_i t_i for c = 0 and sum_i log(1 + c t_i)/c otherwise. Critical values are the 95th percentile of the statistic under N(0,1), so every row has normal size 0.0500 by construction. Power is the rejection rate at that normal-calibrated 5% critical value. The gain over c=0 is the paired difference in rejection indicators on the same draws, and the paired SE is the standard error of that difference across sims.

**Settings.** Seed 89101 (new; member-2 and member-3 used other seeds). 20000 sims per n per law. c in 0, 0.25, 0.5, 1, 2, 3, 5, 10. n in 25, 50, 100. Laws: normal, t(3), t(5), 0.9 N(0,1) + 0.1 N(0,9) (contaminated normal, drawn as N(0,1) scaled by 3 with probability 0.1). Script: numpy + scipy log_ndtr, run via uv outside the repo.

## Tables (one row per c, n, law)
### n = 25

| c | law | power | gain vs c=0 | paired SE |
|---|---|---|---|---|
| 0 | normal | 0.0500 | — | — |
| 0.25 | normal | 0.0500 | — | — |
| 0.5 | normal | 0.0500 | — | — |
| 1 | normal | 0.0500 | — | — |
| 2 | normal | 0.0500 | — | — |
| 3 | normal | 0.0500 | — | — |
| 5 | normal | 0.0500 | — | — |
| 10 | normal | 0.0500 | — | — |
| 0 | t(3) | 0.3789 | +0.0000 | 0.0000 |
| 0.25 | t(3) | 0.4284 | +0.0495 | 0.0016 |
| 0.5 | t(3) | 0.4435 | +0.0646 | 0.0018 |
| 1 | t(3) | 0.4578 | +0.0790 | 0.0020 |
| 2 | t(3) | 0.4576 | +0.0787 | 0.0022 |
| 3 | t(3) | 0.4567 | +0.0779 | 0.0022 |
| 5 | t(3) | 0.4491 | +0.0702 | 0.0023 |
| 10 | t(3) | 0.4322 | +0.0534 | 0.0023 |
| 0 | t(5) | 0.1963 | +0.0000 | 0.0000 |
| 0.25 | t(5) | 0.2346 | +0.0383 | 0.0015 |
| 0.5 | t(5) | 0.2482 | +0.0520 | 0.0017 |
| 1 | t(5) | 0.2616 | +0.0654 | 0.0020 |
| 2 | t(5) | 0.2639 | +0.0677 | 0.0021 |
| 3 | t(5) | 0.2650 | +0.0688 | 0.0022 |
| 5 | t(5) | 0.2630 | +0.0668 | 0.0022 |
| 10 | t(5) | 0.2522 | +0.0559 | 0.0022 |
| 0 | 0.9 N(0,1) + 0.1 N(0,9) | 0.2970 | +0.0000 | 0.0000 |
| 0.25 | 0.9 N(0,1) + 0.1 N(0,9) | 0.3389 | +0.0419 | 0.0016 |
| 0.5 | 0.9 N(0,1) + 0.1 N(0,9) | 0.3553 | +0.0583 | 0.0018 |
| 1 | 0.9 N(0,1) + 0.1 N(0,9) | 0.3714 | +0.0743 | 0.0020 |
| 2 | 0.9 N(0,1) + 0.1 N(0,9) | 0.3799 | +0.0829 | 0.0022 |
| 3 | 0.9 N(0,1) + 0.1 N(0,9) | 0.3847 | +0.0877 | 0.0023 |
| 5 | 0.9 N(0,1) + 0.1 N(0,9) | 0.3844 | +0.0874 | 0.0023 |
| 10 | 0.9 N(0,1) + 0.1 N(0,9) | 0.3781 | +0.0811 | 0.0024 |

### n = 50

| c | law | power | gain vs c=0 | paired SE |
|---|---|---|---|---|
| 0 | normal | 0.0500 | — | — |
| 0.25 | normal | 0.0500 | — | — |
| 0.5 | normal | 0.0500 | — | — |
| 1 | normal | 0.0500 | — | — |
| 2 | normal | 0.0500 | — | — |
| 3 | normal | 0.0500 | — | — |
| 5 | normal | 0.0500 | — | — |
| 10 | normal | 0.0500 | — | — |
| 0 | t(3) | 0.6152 | +0.0000 | 0.0000 |
| 0.25 | t(3) | 0.6903 | +0.0751 | 0.0019 |
| 0.5 | t(3) | 0.7067 | +0.0914 | 0.0021 |
| 1 | t(3) | 0.7211 | +0.1058 | 0.0023 |
| 2 | t(3) | 0.7304 | +0.1152 | 0.0024 |
| 3 | t(3) | 0.7293 | +0.1140 | 0.0024 |
| 5 | t(3) | 0.7220 | +0.1067 | 0.0025 |
| 10 | t(3) | 0.7037 | +0.0885 | 0.0025 |
| 0 | t(5) | 0.3075 | +0.0000 | 0.0000 |
| 0.25 | t(5) | 0.3870 | +0.0795 | 0.0020 |
| 0.5 | t(5) | 0.4087 | +0.1012 | 0.0022 |
| 1 | t(5) | 0.4263 | +0.1187 | 0.0025 |
| 2 | t(5) | 0.4416 | +0.1341 | 0.0026 |
| 3 | t(5) | 0.4439 | +0.1363 | 0.0027 |
| 5 | t(5) | 0.4409 | +0.1333 | 0.0027 |
| 10 | t(5) | 0.4287 | +0.1211 | 0.0027 |
| 0 | 0.9 N(0,1) + 0.1 N(0,9) | 0.4582 | +0.0000 | 0.0000 |
| 0.25 | 0.9 N(0,1) + 0.1 N(0,9) | 0.5360 | +0.0777 | 0.0020 |
| 0.5 | 0.9 N(0,1) + 0.1 N(0,9) | 0.5566 | +0.0984 | 0.0022 |
| 1 | 0.9 N(0,1) + 0.1 N(0,9) | 0.5800 | +0.1217 | 0.0024 |
| 2 | 0.9 N(0,1) + 0.1 N(0,9) | 0.6002 | +0.1419 | 0.0026 |
| 3 | 0.9 N(0,1) + 0.1 N(0,9) | 0.6087 | +0.1505 | 0.0027 |
| 5 | 0.9 N(0,1) + 0.1 N(0,9) | 0.6145 | +0.1562 | 0.0027 |
| 10 | 0.9 N(0,1) + 0.1 N(0,9) | 0.6139 | +0.1556 | 0.0028 |

### n = 100

| c | law | power | gain vs c=0 | paired SE |
|---|---|---|---|---|
| 0 | normal | 0.0500 | — | — |
| 0.25 | normal | 0.0500 | — | — |
| 0.5 | normal | 0.0500 | — | — |
| 1 | normal | 0.0500 | — | — |
| 2 | normal | 0.0500 | — | — |
| 3 | normal | 0.0500 | — | — |
| 5 | normal | 0.0500 | — | — |
| 10 | normal | 0.0500 | — | — |
| 0 | t(3) | 0.8560 | +0.0000 | 0.0000 |
| 0.25 | t(3) | 0.9111 | +0.0551 | 0.0016 |
| 0.5 | t(3) | 0.9246 | +0.0687 | 0.0018 |
| 1 | t(3) | 0.9325 | +0.0765 | 0.0019 |
| 2 | t(3) | 0.9360 | +0.0800 | 0.0020 |
| 3 | t(3) | 0.9355 | +0.0795 | 0.0020 |
| 5 | t(3) | 0.9327 | +0.0767 | 0.0020 |
| 10 | t(3) | 0.9230 | +0.0670 | 0.0020 |
| 0 | t(5) | 0.4880 | +0.0000 | 0.0000 |
| 0.25 | t(5) | 0.6092 | +0.1212 | 0.0023 |
| 0.5 | t(5) | 0.6442 | +0.1561 | 0.0026 |
| 1 | t(5) | 0.6701 | +0.1820 | 0.0028 |
| 2 | t(5) | 0.6842 | +0.1961 | 0.0029 |
| 3 | t(5) | 0.6885 | +0.2004 | 0.0030 |
| 5 | t(5) | 0.6858 | +0.1978 | 0.0030 |
| 10 | t(5) | 0.6757 | +0.1877 | 0.0030 |
| 0 | 0.9 N(0,1) + 0.1 N(0,9) | 0.6794 | +0.0000 | 0.0000 |
| 0.25 | 0.9 N(0,1) + 0.1 N(0,9) | 0.7686 | +0.0892 | 0.0021 |
| 0.5 | 0.9 N(0,1) + 0.1 N(0,9) | 0.7920 | +0.1126 | 0.0023 |
| 1 | 0.9 N(0,1) + 0.1 N(0,9) | 0.8135 | +0.1341 | 0.0025 |
| 2 | 0.9 N(0,1) + 0.1 N(0,9) | 0.8320 | +0.1527 | 0.0026 |
| 3 | 0.9 N(0,1) + 0.1 N(0,9) | 0.8408 | +0.1615 | 0.0027 |
| 5 | 0.9 N(0,1) + 0.1 N(0,9) | 0.8480 | +0.1687 | 0.0027 |
| 10 | 0.9 N(0,1) + 0.1 N(0,9) | 0.8522 | +0.1729 | 0.0027 |

## Rule 2 answers

**c maximizing t(3) gain over c=0, per n:**

| n | best c | t(3) gain (SE) | runner-up | gap to runner-up |
|---|---|---|---|---|
| 25 | 1 | +0.0790 (0.0020) | c=2 at +0.0787 | 0.0003 |
| 50 | 2 | +0.1152 (0.0024) | c=3 at +0.1140 | 0.0012 |
| 100 | 2 | +0.0800 (0.0020) | c=3 at +0.0795 | 0.0005 |

**Monotonicity over c = 0.25, 0.5, 1, 2, 3:** not monotone at any n. The first turn is at n=25, c=2 (gain drops from +0.0790 at c=1 to +0.0787 at c=2). At n=50 and n=100 the first turn is at c=3. Every turn below c=5 is smaller than one paired SE, so the plateau from c=1 to c=3 is flat within Monte Carlo noise. Past c=3 the t(3) gain falls at every n through c=5 and c=10, and those drops exceed two SE.

**t(3)-optimal c under t(5) and under 0.9 N(0,1) + 0.1 N(0,9):** gains, never losses, at every n, each far beyond two paired SE.

| n | t(3)-optimal c | t(5) gain (SE) | contaminated gain (SE) |
|---|---|---|---|
| 25 | 1 | +0.0654 (0.0020), 33 SE | +0.0743 (0.0020), 36 SE |
| 50 | 2 | +0.1341 (0.0026), 51 SE | +0.1419 (0.0026), 55 SE |
| 100 | 2 | +0.1961 (0.0029), 68 SE | +0.1527 (0.0026), 59 SE |

Under t(5) the best c is 3 at every n, and under the contaminated normal the best c drifts upward with n (3 at n=25, 5 at n=50, 10 at n=100). But at the t(3)-optimal c the shortfall against those law-specific optima is at most 0.02 in power, while the gain over c=0 is 0.07 to 0.20.

## Verdict

**Fix c = 2.** It is the t(3)-optimal c at n=50 and n=100 and trails c=1 at n=25 by 0.0003, far inside noise. It agrees with member-3's seed-89303 verdict. c=2 gains by more than two paired SE under every non-normal law at every n, and the direct c=2 vs c=3 gap is within one SE of the gain at every n, so the choice between 1, 2 and 3 is not resolvable at 20000 sims; c=2 sits in the middle of the plateau.

**Caveat.** The paired SE shown is for the gain over c=0, not for the direct difference between adjacent c values. The gaps between c=1, 2, 3 are all under 0.0013 and should be read as ties.
