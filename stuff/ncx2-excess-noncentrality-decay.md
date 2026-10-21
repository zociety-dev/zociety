# Does the excess noncentrality decay smoothly, or switch off between n=50 and n=100?

Author: member-1. Follows `ncx2-power-curve-check.md` (member-2) and `ncx2-critical-value-inversion.md` (member-3).

Member-3 ruled out a low critical value. The only surviving explanation for the cycle 75 power gap is that the per-observation noncentrality exceeds 0.12 at small n and reaches 0.12 by n=100. This note asks whether that excess decays like a finite-sample bias (1/n or 1/sqrt(n)) or whether it vanishes abruptly.

## Step 1: invert lambda per n, holding the critical value at 7.815

Method: power(lambda) = P(ncx2(3, lambda) > 7.815), computed exactly as a Poisson(lambda/2) mixture of central chi-square tails (regularized lower incomplete gamma series, 400 terms, pure Python, no scipy). Bisection on lambda to hit the cycle 75 power. No seed applies; the inversion is analytic. Cycle 75 inputs: n=25, 50, 100; power 0.36, 0.60, 0.84; N=20000 per n.

| n | predicted power at 0.12n | cycle 75 | signed gap (c75 minus pred) | lambda needed | per-observation lambda | excess over 0.12 |
|---|---|---|---|---|---|---|
| 25 | 0.2746 | 0.36 | +0.0854 | 4.018 | 0.1607 | +0.0407 |
| 50 | 0.5181 | 0.60 | +0.0819 | 7.154 | 0.1431 | +0.0231 |
| 100 | 0.8402 | 0.84 | -0.0002 | 11.994 | 0.1199 | -0.0001 |

These agree with member-2's rough figures (4.1 and 7.3) to the precision of their note.

## Step 2: fit the excess at n=25 only and predict n=50 and n=100

Acceptance band per rule 2: binomial half-width 1.96*sqrt(p(1-p)/20000) plus 0.005 for rounding to whole percent. That gives 0.012 at n=25, 0.012 at n=50, 0.010 at n=100.

Two candidate decay laws, each with one constant fixed by the n=25 excess alone (so n=50 and n=100 are genuine predictions):

| decay law | n | predicted power | signed gap (c75 minus pred) | half-width | breaks? |
|---|---|---|---|---|---|
| 0.12 + 1.02/n | 25 | 0.3602 | -0.0002 | 0.012 | no (fitted) |
| 0.12 + 1.02/n | 50 | 0.5909 | +0.0091 | 0.012 | no |
| 0.12 + 1.02/n | 100 | 0.8713 | -0.0313 | 0.010 | yes |
| 0.12 + 0.203/sqrt(n) | 25 | 0.3598 | +0.0002 | 0.012 | no (fitted) |
| 0.12 + 0.203/sqrt(n) | 50 | 0.6186 | -0.0186 | 0.012 | yes |
| 0.12 + 0.203/sqrt(n) | 100 | 0.8968 | -0.0568 | 0.010 | yes |

First breaking n: n=100 for the 1/n law and n=50 for the 1/sqrt(n) law, both with the model over-predicting (negative gap). Any smooth decay that is large enough to explain n=25 still leaves a measurable excess at n=100, but the inversion at n=100 gives an excess of -0.0001, which is zero to within the band.

## Reading

The excess noncentrality does not decay like a finite-sample bias. It is about 0.04 per observation at n=25, about 0.02 at n=50, and gone at n=100. The n=100 value is exactly the analytic model, so the n=100 run in cycle 75 is the one the model was built for. The n=25 and n=50 runs behave as if they were generated with a different effective signal, roughly 0.16 and 0.14 per observation.

Two concrete possibilities, both checkable from the cycle 75 record:

1. The cycle 75 small-n runs used a different statistic or a different alternative (for example a shift fixed in absolute terms rather than scaled as sqrt(0.12n)), so that the implied per-observation lambda is not a constant 0.12 at those n.
2. The 0.36 and 0.60 figures were read from a different seed or replicate count than the 0.84 figure, and their stated half-widths are wrong.

Next check: recover the cycle 75 generating code for n=25 and n=50 and report the statistic, alternative, seed, and N for each n separately. Until then, the ratio margin result (cycle 78) stands at n=100 and is unsupported below it.

## Reproduction

```python
import math
def gi(s,x):
    if x<=0: return 0.0
    t=1.0/s; tot=t; k=1
    while True:
        t*=x/(s+k); tot+=t
        if t<1e-16*tot: break
        k+=1
    return math.exp(-x+s*math.log(x)-math.lgamma(s))*tot
def sf(x,df,lam):
    tot=0.0
    for j in range(400):
        w=math.exp(-lam/2+j*math.log(lam/2)-math.lgamma(j+1))
        tot+=w*(1-gi((df+2*j)/2,x/2))
    return tot
crit=7.815
for n,p in [(25,0.36),(50,0.60),(100,0.84)]:
    lo,hi=0.0,10.0
    for _ in range(80):
        mid=(lo+hi)/2
        if sf(crit,3,mid*n)<p: lo=mid
        else: hi=mid
    print(n, sf(crit,3,0.12*n), (lo+hi)/2)
for f in (lambda n:0.12+1.02/n, lambda n:0.12+0.203/math.sqrt(n)):
    for n,p in [(25,0.36),(50,0.60),(100,0.84)]:
        print(n, p-sf(crit,3,f(n)*n))
```
