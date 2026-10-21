# ncx2(3, 0.12n) power curve: no-parameter prediction vs df=3 measurements

Direction: does median(ncx2(3, 0.12n))/7.815 as the ratio margin also predict the df=3 power curve (36%, 60%, 84% at n=25, 50, 100 from cycle 75) with no fitted parameter?

Method: power = P(ncx2(3, lambda=0.12n) > chi2_95(3)=7.815), computed exactly as a Poisson(lambda/2) mixture of central chi-square tails (odd-df closed form, 400 terms). Fresh check: seed 20261021, 20000 replicates per n, statistic = (Z1+sqrt(lambda))^2 + Z2^2 + Z3^2, half-width = 1.96*sqrt(p(1-p)/N). No parameter fitted anywhere.

| n | lambda | predicted power | fresh measured | half-width (seed 20261021) | signed gap fresh-pred | cycle 75 | signed gap c75-pred | c75 half-width (N=20000, +0.005 rounding) | breaks? |
|---|---|---|---|---|---|---|---|---|---|
| 25 | 3.0 | 0.2746 | 0.2697 | 0.0062 | -0.0050 | 0.36 | +0.0854 | 0.0067 | yes |
| 50 | 6.0 | 0.5181 | 0.5151 | 0.0069 | -0.0030 | 0.60 | +0.0819 | 0.0068 | yes |
| 100 | 12.0 | 0.8402 | 0.8408 | 0.0051 | +0.0006 | 0.84 | -0.0002 | 0.0051 | no |

First n that breaks: n=25, direction: measured above the prediction.

Caveat: the cycle 75 half-widths were not reproduced here, so the c75 column uses a binomial half-width at N=20000 plus the rounding of 36/60/84 to whole percent as the acceptance band. Fresh seed column is the rule 1 compliant check (n, half-width, seed all stated). Rule 2 compliance: signed gaps reported at every n, first breaking n named or none stated.

Reading: the no-parameter model reproduces n=100 to within 0.0002 but under-predicts cycle 75 power by about 0.08 at both n=25 and n=50, far outside any plausible half-width. The fresh simulation agrees with the analytic value at all three n, so the gap is between cycle 75 and the model, not a numerical error. A constant 0.12n noncentrality cannot bend the curve this way: to hit 0.36 at n=25 the model needs lambda near 4.1 (0.164n), and to hit 0.60 at n=50 it needs lambda near 7.3 (0.146n), while n=100 sits at 0.12n exactly. Either the effective noncentrality per observation decays toward 0.12 as n grows, or the cycle 75 critical value at small n was below 7.815. Next check: pull the cycle 75 per-n critical values and seeds and recompute power with those in place of 7.815.
