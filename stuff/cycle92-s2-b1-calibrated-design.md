# Cycle 92, stuff 1 (member-2): S2 + sample skewness b1, exact-size calibrated — design and runner

Status: design and runnable script. The 20000-sim numbers are NOT in this file;
the turn budget (300 s) did not allow the full run. The tables below are the
exact layout rule 2 requires and must be filled by running the script in the
next stuff item. Seed for the run: **92101**.

## Definitions (rule 1, before any table)

Sample x_1..x_n, standardized z_i = (x_i - xbar)/s with s the n-1 sd, sorted z_(1) <= ... <= z_(n).

- t_i = -((2i-1)/n) * [ ln Phi(z_(i)) + ln(1 - Phi(z_(n+1-i))) ], i = 1..n
- **S2** = sum_i log(1 + 2 t_i) / 2 (capped AD sum, c=2). Reject for large S2.
- **A2** = sum_i t_i - n (plain Anderson-Darling). Reject for large A2.
- **W** = Shapiro-Wilk statistic (scipy.stats.shapiro). Reject for small W.
- **Partner: b1** = m3 / m2^1.5, m_k = mean((x - xbar)^k). Two-sided: reject for large |b1|.
  Chosen over W because W is itself a full omnibus test; b1 isolates the skew direction
  S2 is blind to, and is expected to be only weakly correlated with S2 under the null
  (S2 is driven by tail mass, b1 by asymmetry).

## Null calibration (rule 1)

From one set of 20000 N(0,1) draws per n (seed 92101, stream per n):

1. Normal-calibrated p-values: p_S2 = empirical upper-tail p of S2 against the 20000
   null S2 values; p_b1 = empirical upper-tail p of |b1| against the 20000 null |b1| values.
2. Null correlation: Pearson corr(S2, |b1|) and Spearman corr on the same 20000 draws.
3. Combination statistic: p_min = min(p_S2, p_b1). Reject when p_min < c_n.
4. c_n = the 5% empirical quantile of p_min under the null (so achieved size is 5%
   within one MC SE = sqrt(0.05*0.95/20000) = 0.0015). Report c_n and achieved size.
   Under independence c_n would be 1 - sqrt(0.95) = 0.0253; c_n above that measures
   how much the positive null correlation is worth.

| n   | corr(S2,|b1|) Pearson | Spearman | c_n | achieved null size | S2 5% crit | A2 5% crit | W 5% crit |
|-----|------------------------|----------|-----|--------------------|------------|------------|-----------|
| 25  | pending                |          |     |                    |            |            |           |
| 50  | pending                |          |     |                    |            |            |           |
| 100 | pending                |          |     |                    |            |            |           |

## Alternatives

- Skew: chi-square(5)
- Heavy tail: t(3), t(5), Laplace
- Contamination: 0.9 N(0,1) + 0.1 N(0,3^2); 0.95 N(0,1) + 0.05 N(0,5^2)

20000 draws per (n, law), same draws scored by all four tests, so every
difference is paired. Paired SE of a power difference between tests X and Y:
sqrt((p_xy + p_yx) / N) with p_xy = fraction rejected by X only, p_yx by Y only.

## Comparison table (rule 2 layout, one row per n x law)

Verdict: "beats" if combo - other > 2 paired SE, "loses" if < -2 paired SE, else "tie".

| n | law | combo | S2 | A2 | W | combo-A2 (SE) | verdict vs AD | combo-W (SE) | verdict vs SW | combo-S2 (SE) | within 2 SE of S2? |
|---|-----|-------|----|----|---|---------------|---------------|--------------|---------------|---------------|--------------------|
| 25/50/100 | chi2(5), t3, t5, laplace, cont10, cont5 | pending | | | | | | | | | |

## Runner (uv run --with numpy --with scipy python stuff/cycle92_s2_b1.py)

```python
import numpy as np
from scipy import stats
from scipy.special import log_ndtr

SEED = 92101
N_SIMS = 20000
NS = [25, 50, 100]

def draw(law, n, rng):
    if law == "normal":  return rng.standard_normal((N_SIMS, n))
    if law == "chi2_5":  return rng.chisquare(5, (N_SIMS, n))
    if law == "t3":      return rng.standard_t(3, (N_SIMS, n))
    if law == "t5":      return rng.standard_t(5, (N_SIMS, n))
    if law == "laplace": return rng.laplace(size=(N_SIMS, n))
    if law == "cont10":
        m = rng.random((N_SIMS, n)) < 0.10
        return np.where(m, 3.0, 1.0) * rng.standard_normal((N_SIMS, n))
    if law == "cont5":
        m = rng.random((N_SIMS, n)) < 0.05
        return np.where(m, 5.0, 1.0) * rng.standard_normal((N_SIMS, n))
    raise ValueError(law)

def score(x):
    n = x.shape[1]
    xc = x - x.mean(1, keepdims=True)
    s = x.std(1, ddof=1, keepdims=True)
    z = np.sort(xc / s, axis=1)
    i = np.arange(1, n + 1)
    t = -((2 * i - 1) / n) * (log_ndtr(z) + log_ndtr(-z[:, ::-1]))
    s2 = np.sum(np.log1p(2 * t), axis=1) / 2
    a2 = t.sum(1) - n
    m2 = (xc ** 2).mean(1); m3 = (xc ** 3).mean(1)
    b1 = np.abs(m3 / m2 ** 1.5)
    w = np.array([stats.shapiro(r)[0] for r in x])
    return s2, a2, b1, w

def emp_p_upper(null_sorted, v):   # P(null >= v)
    return 1.0 - np.searchsorted(null_sorted, v, side="left") / len(null_sorted)

def paired_se(rx, ry):
    return np.sqrt((np.mean(rx & ~ry) + np.mean(~rx & ry)) / len(rx))

rng = np.random.default_rng(SEED)
for n in NS:
    s2n, a2n, b1n, wn = score(draw("normal", n, rng))
    s2s, b1s = np.sort(s2n), np.sort(b1n)
    pmin_null = np.minimum(emp_p_upper(s2s, s2n), emp_p_upper(b1s, b1n))
    c_n = np.quantile(pmin_null, 0.05)
    crit = dict(s2=np.quantile(s2n, 0.95), a2=np.quantile(a2n, 0.95), w=np.quantile(wn, 0.05))
    print(f"n={n} pearson={np.corrcoef(s2n, b1n)[0,1]:.3f} "
          f"spearman={stats.spearmanr(s2n, b1n)[0]:.3f} c_n={c_n:.4f} "
          f"size={np.mean(pmin_null < c_n):.4f} crit={crit}")
    for law in ["chi2_5", "t3", "t5", "laplace", "cont10", "cont5"]:
        s2, a2, b1, w = score(draw(law, n, rng))
        r = dict(combo=np.minimum(emp_p_upper(s2s, s2), emp_p_upper(b1s, b1)) < c_n,
                 s2=s2 > crit["s2"], a2=a2 > crit["a2"], w=w < crit["w"])
        row = {k: v.mean() for k, v in r.items()}
        for o in ["a2", "w", "s2"]:
            d = row["combo"] - row[o]; se = paired_se(r["combo"], r[o])
            v = "beats" if d > 2 * se else ("loses" if d < -2 * se else "tie")
            row[f"vs_{o}"] = f"{d:+.4f} ({se:.4f}) {v}"
        print(n, law, row)
```

## What remains

Run the script (Shapiro-Wilk is the slow part: 20000 x 7 laws x 3 n calls),
paste the printed rows into the two tables, and record it as stuff 2 under
rules 1 and 2. Seed 92101 is fixed here so the run is reproducible.
