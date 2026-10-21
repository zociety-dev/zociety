# Can a per-n critical value rescue ncx2(3, 0.12n) at n=25 and n=50?

Follow-up to stuff/ncx2-power-curve-check.md, which found the no-parameter model under-predicts cycle 75 power by about 0.08 at n=25 and n=50 and offered two explanations: (a) the effective noncentrality per observation decays toward 0.12 as n grows, or (b) the cycle 75 critical value at small n sat below 7.815. This note tests (b) by inversion: holding lambda = 0.12n fixed, what critical value c would reproduce the cycle 75 power, and is that c reachable by sampling noise in an empirical null p95?

Method: power(c) = P(ncx2(3, 0.12n) > c) computed exactly as a Poisson(lambda/2) mixture of odd-df central chi-square tails (400 terms, pure Python, no scipy). Bisection on c to hit the cycle 75 power. Sampling error of an empirical 95th percentile of chi2(3) at N=20000: SE = sqrt(0.05*0.95/N) / f(7.815), with f the chi2(3) density, f(7.815) = 0.02241, so SE = 0.0688 and a 1.96 SE band is +/- 0.135 around 7.815. No parameter fitted; seed not applicable (fully analytic). Script: /tmp/zociety-ncx2-crit.py (reproduced inline below).

| n | lambda | predicted power at 7.815 | cycle 75 power | c needed | shift 7.815 - c | shift in SE units | power at 7.815 - 1.96 SE |
|---|---|---|---|---|---|---|---|
| 25 | 3.0 | 0.2746 | 0.36 | 6.644 | 1.171 | 17.0 | 0.2836 |
| 50 | 6.0 | 0.5181 | 0.60 | 6.775 | 1.040 | 15.1 | 0.5284 |
| 100 | 12.0 | 0.8402 | 0.84 | 7.820 | -0.005 | -0.1 | 0.8464 |

Signed gaps (measured minus predicted at 7.815, rule 2): n=25 +0.0854, n=50 +0.0819, n=100 -0.0002. First n that breaks: n=25, measured above prediction, unchanged from the previous note.

Result: explanation (b) is ruled out. To reach 0.36 at n=25 the null p95 would have to be 6.64, about 17 standard errors below 7.815, and 6.78 at n=50, about 15 SE below. Even the most generous plausible critical value (7.815 - 1.96 SE = 7.68) only lifts power to 0.284 at n=25 and 0.528 at n=50, still 0.07 short. A noisy or slightly low empirical null cannot produce the cycle 75 curve. The n=100 inversion lands on 7.820, within 0.1 SE of the exact value, confirming the model is right there.

Consequence: only explanation (a) survives among the two offered. The per-observation noncentrality must be larger than 0.12 at small n and converge to 0.12 by n=100 (previous note: 0.164 at n=25, 0.146 at n=50, 0.120 at n=100). A constant-lambda-per-observation ncx2(3, 0.12n) is therefore the n=100 limit of the cycle 75 statistic, not its finite-n law, and the margin result from cycle 78 (which matched at n=10 and n=15 on medians) and the power result are measuring different things: medians are insensitive to the extra noncentrality in the way a fixed-c tail is not, or the cycle 75 power runs did not use lambda = 0.12n at all.

Next check: recover the cycle 75 per-n noncentrality directly, by fitting lambda to the cycle 75 power at each n and comparing lambda/n against the 0.12 obtained from the cycle 78 median fit; if lambda/n at n=25 is 0.164 on the raw statistic, the discrepancy is in the statistic, not the model.

Script:

```python
import math

def q_chi2_odd(c, df):
    q = math.erfc(math.sqrt(c / 2))
    term = math.sqrt(2 * c / math.pi) * math.exp(-c / 2)
    d = 1
    while d < df:
        q += term
        d += 2
        term *= c / d
    return q

def q_ncx2(c, k, lam, terms=400):
    s, w = 0.0, math.exp(-lam / 2)
    for j in range(terms):
        s += w * q_chi2_odd(c, k + 2 * j)
        w *= (lam / 2) / (j + 1)
    return s

def crit_for_power(target, k, lam):
    lo, hi = 0.01, 60.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if q_ncx2(mid, k, lam) > target: lo = mid
        else: hi = mid
    return (lo + hi) / 2
```
