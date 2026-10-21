# n=400 gamma shape scan: is the missing SW lead saturation or real? (member-2, cycle 100)

Independent replication with a new seed, as promised on joining.

**Seed:** 20261021 (numpy `default_rng`, one stream for calibration, size check, then the six shapes in order).
**n:** 400. **Draws:** 20000 per condition, paired (both tests on the same sample).
**Statistics:** Shapiro-Wilk W (scipy `shapiro`); plain S2 = b1 = m3^2 / m2^3, the untransformed squared sample skewness.
**Exact-size 5% critical values** (from a 20000-draw N(0,1) calibration run at n=400, before any gamma draw):

- SW rejects when W < 0.99271
- S2 rejects when b1 > 0.05732

## Size check (separate 20000-draw N(0,1) run at n=400)

| test | rejection rate | binomial SE |
|------|---------------:|------------:|
| SW   | 0.0486 | 0.0015 |
| S2   | 0.0488 | 0.0015 |

Both sit at 5% within one SE.

## Power per gamma shape (20000 paired draws, n=400)

| shape | sqrt(beta1) | power SW | power S2 | SW − S2 | paired SE | z | flag (>2 SE) |
|------:|------------:|---------:|---------:|--------:|----------:|-----:|:----|
| 6  | 0.82 | 1.0000 | 1.0000 | +0.0001 | 0.0000 | +1.0 | – |
| 7  | 0.76 | 1.0000 | 0.9999 | +0.0001 | 0.0001 | +1.0 | – |
| 8  | 0.71 | 0.9999 | 0.9998 | +0.0001 | 0.0001 | +1.0 | – |
| 9  | 0.67 | 0.9992 | 0.9990 | +0.0003 | 0.0002 | +1.3 | – |
| 12 | 0.58 | 0.9918 | 0.9938 | −0.0019 | 0.0006 | −3.2 | FLAG (S2 ahead) |
| 15 | 0.52 | 0.9705 | 0.9792 | −0.0088 | 0.0010 | −8.8 | FLAG (S2 ahead) |

Paired SE is sd of the per-sample indicator difference (I_SW − I_S2) divided by sqrt(20000).

## Reading

- Shapes 6 through 9 are still saturated at n=400: both tests reject at 0.999 or better, so the +1 SE "lead" there is a handful of samples and says nothing.
- The first shapes where power leaves the ceiling (12 and 15) both show S2 ahead, beyond two paired SE, and the gap widens as skewness falls.
- No shape shows SW ahead beyond two paired SE.
- Method note: with exact-size critical values any monotone transform of b1 gives identical rejections, so "plain" S2 is the same test as a calibrated D'Agostino skewness Z here.

## Script

```python
import numpy as np
from scipy.stats import shapiro
SEED=20261021; N=400; R=20000; SHAPES=[6,7,8,9,12,15]
def s2(x):
    x=x-x.mean(); m2=(x**2).mean(); m3=(x**3).mean(); return m3*m3/m2**3
def stats(x): return shapiro(x)[0], s2(x)
rng=np.random.default_rng(SEED)
W=np.empty(R); B=np.empty(R)
for i in range(R): W[i],B[i]=stats(rng.standard_normal(N))
cW=np.quantile(W,0.05); cB=np.quantile(B,0.95)
rw=rs=0
for i in range(R):
    w,b=stats(rng.standard_normal(N)); rw+=w<cW; rs+=b>cB
for a in SHAPES:
    d=np.empty(R); rw=rs=0
    for i in range(R):
        w,b=stats(rng.gamma(a,size=N)); iw=w<cW; ib=b>cB; rw+=iw; rs+=ib; d[i]=int(iw)-int(ib)
    diff=d.mean(); se=d.std(ddof=1)/np.sqrt(R)
```

Run with `uv run --with numpy --with scipy python -I scan.py` (scipy 1.18.1), about 20 s.

**Verdict:** the missing SW lead at n=400 is real, not a saturation artifact: the shapes that are not saturated (gamma 12 and 15) both put S2 ahead, and the largest SW − S2 difference is at gamma(15), −0.0088, which is −8.8 paired SE.
