# Cycle 94, stuff 1 (member-2): is SW's skew advantage general? SW vs plain AD vs plain S2, exact 5% size, 20000 paired sims per n, seed 94201

One `default_rng(94201)` stream consumed in order n=25, 50, 100; per n the laws normal, chi2(2),
chi2(10), lognormal(0, 0.5), beta(2, 5). All three tests are scored on the same draws in every cell.
Runner: `stuff/cycle94_skew_general.py`
(`uv run --with numpy --with scipy python stuff/cycle94_skew_general.py`), wall clock 25 s.
No cell edited by hand; the tables below are the script's output.

## Definitions

z = sample-standardized order statistics (sample mean, n-1 sd, sorted ascending), i = 1..n.
Plain AD term t_i = -((2i-1)/n) [ln Phi(z_(i)) + ln(1 - Phi(z_(n+1-i)))].
**A2** = sum t_i - n (plain AD, reject large); **S2** = sum log(1 + 2 t_i)/2 (plain S2, c = 2, reject large);
**W** = Shapiro-Wilk (scipy.stats.shapiro, reject small).
Each 5% critical value is the empirical 95% (W: 5%) quantile of that statistic's 20000 null values,
so every power row is at matched exact size. MC SE of a null rate at 0.05 is 0.0015.

## Seed and exact-size 5% critical values (rule 2, before any power table): seed 94201, 20000 N(0,1) draws per n

| n | W 5% crit | W null rate | A2 5% crit | A2 null rate | S2 5% crit | S2 null rate |
|---|---|---|---|---|---|---|
| 25 | 0.9194 | 0.0500 | 0.7281 | 0.0500 | 13.3943 | 0.0500 |
| 50 | 0.9543 | 0.0500 | 0.7359 | 0.0500 | 26.5074 | 0.0500 |
| 100 | 0.9747 | 0.0500 | 0.7505 | 0.0500 | 52.7086 | 0.0500 |

## Power at exact 5% size (rule 1), 20000 paired draws per cell

Gap = SW minus other; paired SE = sd of the per-draw rejection-indicator difference / sqrt(20000).
Verdict: beats if gap > 2 SE, loses if gap < -2 SE, else tie (within two paired SE).

| n | law | SW | AD | S2 | SW-AD (SE) | vs AD | SW-S2 (SE) | vs S2 |
|---|---|---|---|---|---|---|---|---|
| 25 | chi2_2 | 0.9230 | 0.8753 | 0.8341 | +0.0476 (0.0015) | beats | +0.0888 (0.0020) | beats |
| 25 | chi2_10 | 0.3056 | 0.2550 | 0.2702 | +0.0507 (0.0020) | beats | +0.0354 (0.0018) | beats |
| 25 | lognormal_0_0.5 | 0.6380 | 0.5726 | 0.5876 | +0.0653 (0.0020) | beats | +0.0504 (0.0019) | beats |
| 25 | beta_2_5 | 0.2245 | 0.1923 | 0.1467 | +0.0322 (0.0018) | beats | +0.0778 (0.0021) | beats |
| 50 | chi2_2 | 0.9991 | 0.9961 | 0.9809 | +0.0030 (0.0004) | beats | +0.0182 (0.0009) | beats |
| 50 | chi2_10 | 0.5917 | 0.4854 | 0.4420 | +0.1063 (0.0025) | beats | +0.1497 (0.0026) | beats |
| 50 | lognormal_0_0.5 | 0.9254 | 0.8765 | 0.8344 | +0.0490 (0.0016) | beats | +0.0910 (0.0020) | beats |
| 50 | beta_2_5 | 0.5050 | 0.4013 | 0.2147 | +0.1036 (0.0024) | beats | +0.2903 (0.0032) | beats |
| 100 | chi2_2 | 1.0000 | 1.0000 | 0.9999 | +0.0000 (0.0000) | tie | +0.0001 (0.0001) | tie |
| 100 | chi2_10 | 0.9068 | 0.8068 | 0.6747 | +0.1000 (0.0022) | beats | +0.2321 (0.0030) | beats |
| 100 | lognormal_0_0.5 | 0.9986 | 0.9932 | 0.9758 | +0.0054 (0.0005) | beats | +0.0228 (0.0011) | beats |
| 100 | beta_2_5 | 0.9009 | 0.7570 | 0.3235 | +0.1440 (0.0025) | beats | +0.5774 (0.0035) | beats |

## Reading the table

1. **The advantage is general, not chi-square(5)-specific.** SW beats both plain AD and plain S2 by
   more than two paired SE in 22 of the 24 comparisons, across strong skew (chi2(2)), mild skew
   (chi2(10)), log-normal and the bounded beta(2, 5).
2. **The gap over S2 grows with n on the mild-skew laws.** SW minus S2 goes from +0.035 to +0.150 to
   +0.232 on chi2(10) and from +0.078 to +0.290 to +0.577 on beta(2, 5). S2's log compression of the
   AD terms damps exactly the moderate one-sided deviations that skew produces, so its skew power
   stalls while SW's climbs.
3. **The only non-beats cells are saturation ties.** At chi2(2), n=100 all three tests reject on
   essentially every draw (SW 1.0000, AD 1.0000, S2 0.9999), so the gaps are 0.0000 and 0.0001 with
   paired SE 0.0000 and 0.0001. SW-AD is identical on all 20000 draws (SE undefined, reported as
   0.0000); SW-S2 is +1.4 SE. These are ceiling effects, not evidence of parity in finite power.
4. **SW never loses.** No cell at any n has SW below AD or S2 by more than two paired SE.

## Answer to the direction (seed 94201)

SW does not win every skew cell at every n: it wins 22 of 24 and ties 2, both at chi-square(2),
n=100, where SW minus AD is +0.0000 (0 paired SE, all draws reject under both) and SW minus S2 is
+0.0001 (+1.4 paired SE) because every test is at the power ceiling; SW loses nowhere.
