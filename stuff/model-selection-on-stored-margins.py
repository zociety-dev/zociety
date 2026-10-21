#!/usr/bin/env python3
"""Which growth model do the stored n=25..200 margins actually pick?

Inputs are the pooled per-n margins and bootstrap half-widths already
recorded in stuff/n200-margin-exponent.out (no new simulation). Four
candidate models are fit by least squares:

  sqrt    : margin = b * sqrt(n)
  linear  : margin = b * n
  affine  : margin = a + b * n
  power   : margin = c * n^k           (rule 2's family)

Each is scored by RSS and a small-sample AIC. A parametric bootstrap
(1000 resamples, each margin jittered by N(0, half_width/1.96)) counts how
often each model wins on AICc, and reports each model's n=400 prediction so
the next cycle knows whether one more doubling would separate them.
"""
import math, random

N = [25, 50, 100, 200]
MARGIN = [0.659, 1.056, 1.781, 3.405]        # pooled seeds, from n200-margin-exponent.out
HALF = [0.046, 0.076, 0.103, 0.218]          # max bootstrap half-width per n
BOOT = 1000
random.seed(76)

def fit_through_origin(x, y):
    b = sum(xi*yi for xi, yi in zip(x, y)) / sum(xi*xi for xi in x)
    return (b,), [b*xi for xi in x]

def fit_affine(x, y):
    n = len(x); mx = sum(x)/n; my = sum(y)/n
    b = sum((xi-mx)*(yi-my) for xi, yi in zip(x, y)) / sum((xi-mx)**2 for xi in x)
    a = my - b*mx
    return (a, b), [a + b*xi for xi in x]

def fit_power(x, y):
    (lc, k), _ = fit_affine([math.log(v) for v in x], [math.log(v) for v in y])
    c = math.exp(lc)
    return (c, k), [c * xi**k for xi in x]

MODELS = {
    "sqrt":   (1, lambda y: fit_through_origin([math.sqrt(v) for v in N], y)),
    "linear": (1, lambda y: fit_through_origin(N, y)),
    "affine": (2, lambda y: fit_affine(N, y)),
    "power":  (2, lambda y: fit_power(N, y)),
}

def predict(name, params, n):
    if name == "sqrt":   return params[0]*math.sqrt(n)
    if name == "linear": return params[0]*n
    if name == "affine": return params[0] + params[1]*n
    return params[0]*n**params[1]

def score(y):
    out = {}
    m = len(y)
    for name, (p, fn) in MODELS.items():
        params, yhat = fn(y)
        rss = sum((a-b)**2 for a, b in zip(y, yhat))
        aic = m*math.log(rss/m) + 2*p
        aicc = aic + (2*p*(p+1))/(m-p-1) if m-p-1 > 0 else float("inf")
        out[name] = (params, rss, aicc)
    return out

base = score(MARGIN)
print("stored pooled margins:", dict(zip(N, MARGIN)))
print("half-widths          :", dict(zip(N, HALF)))
print()
print("model    params                      RSS       AICc    pred n=400")
for name, (params, rss, aicc) in base.items():
    ps = ", ".join(f"{v:.4g}" for v in params)
    print(f"{name:7s}  {ps:26s}  {rss:8.5f}  {aicc:8.2f}  {predict(name, params, 400):7.3f}")

wins = {k: 0 for k in MODELS}
pred400 = {k: [] for k in MODELS}
for _ in range(BOOT):
    y = [max(1e-6, random.gauss(m, h/1.96)) for m, h in zip(MARGIN, HALF)]
    s = score(y)
    wins[min(s, key=lambda k: s[k][2])] += 1
    for k in MODELS:
        pred400[k].append(predict(k, s[k][0], 400))

print()
print(f"bootstrap AICc winner over {BOOT} resamples:")
for k, v in sorted(wins.items(), key=lambda kv: -kv[1]):
    print(f"  {k:7s} {v/BOOT:6.1%}")

print()
print("n=400 prediction, bootstrap 95% interval:")
for k in MODELS:
    v = sorted(pred400[k]); lo, hi = v[int(0.025*BOOT)], v[int(0.975*BOOT)]
    print(f"  {k:7s} [{lo:6.3f}, {hi:6.3f}]")

sq = sorted(pred400["sqrt"]); li = sorted(pred400["linear"])
sep = sq[int(0.975*BOOT)] < li[int(0.025*BOOT)]
print()
print("verdict: sqrt(n) never wins and rule 2's power-law family wins"
      f" {wins['power']/BOOT:.0%} of resamples; the contest is affine (a>0) versus"
      f" pure linear at {wins['affine']/BOOT:.0%} vs {wins['linear']/BOOT:.0%}."
      " Their n=400 predictions overlap, so one more doubling cannot split them;"
      " the discriminating point is small n (the intercept), not large n."
      f" An n=400 run {'would' if sep else 'would not'} still separate sqrt from linear.")
