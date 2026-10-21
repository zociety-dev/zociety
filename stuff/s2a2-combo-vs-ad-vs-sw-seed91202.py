#!/usr/bin/env python3
"""Cycle 91: S2+A2 combinations (Bonferroni max-p, reject-if-either) vs plain AD vs Shapiro-Wilk.

Run: uv run --with numpy --with scipy python stuff/s2a2-combo-vs-ad-vs-sw-seed91202.py
Output: markdown rows for stuff/s2a2-combo-vs-ad-vs-sw-seed91202.md
Seed 91202 was not used in cycles 88-90 (those used 88xxx, 89xxx, 90101, 90303, 90505).
"""
import sys
import numpy as np
from scipy.stats import norm, shapiro, t as student_t, chi2

SEED = 91202
NSIM = 20000
NS = (25, 50, 100)
rng = np.random.default_rng(SEED)


def ad_terms(x):
    """t_i = -((2i-1)/n) [ln Phi(z_(i)) + ln(1-Phi(z_(n+1-i)))], z sample-standardized (sd n-1)."""
    n = x.shape[1]
    z = (x - x.mean(1, keepdims=True)) / x.std(1, ddof=1, keepdims=True)
    z.sort(axis=1)
    lcdf = norm.logcdf(z)
    lsf = norm.logsf(z)[:, ::-1]
    w = (2 * np.arange(1, n + 1) - 1) / n
    return -w * (lcdf + lsf)


def stats(x):
    t = ad_terms(x)
    n = x.shape[1]
    s2 = np.sum(np.log1p(2 * t), axis=1) / 2  # capped AD sum, c=2
    a2 = t.sum(1) - n                            # plain Anderson-Darling
    w = np.array([shapiro(r)[0] for r in x])     # Shapiro-Wilk
    return s2, a2, w


def draw(law, n):
    if law == "normal":
        return rng.standard_normal((NSIM, n))
    if law == "t(3)":
        return student_t.rvs(3, size=(NSIM, n), random_state=rng)
    if law == "t(5)":
        return student_t.rvs(5, size=(NSIM, n), random_state=rng)
    if law == "0.9N(0,1)+0.1N(0,9)":
        x = rng.standard_normal((NSIM, n))
        mask = rng.random((NSIM, n)) < 0.1
        return np.where(mask, 3 * x, x)
    if law == "chi2(5)":
        return chi2.rvs(5, size=(NSIM, n), random_state=rng)
    raise ValueError(law)


LAWS = ("normal", "t(3)", "t(5)", "0.9N(0,1)+0.1N(0,9)", "chi2(5)")


def verdict(d, se):
    if d > 2 * se:
        return "win"
    if d < -2 * se:
        return "loss"
    return "tie"


def within(d, se):
    return "within" if abs(d) <= 2 * se else ("above" if d > 0 else "below")


def pval_upper(null_sorted, obs):
    """Normal-calibrated p-value: fraction of null draws >= obs (upper tail)."""
    k = np.searchsorted(null_sorted, obs, side="left")
    return 1.0 - k / null_sorted.size


print(f"seed {SEED}, {NSIM} sims per (n, law); SE = paired Monte Carlo SE of the mean difference of per-sample rejection indicators")
print()
hdr = ("| combo | n | law | power | A2 | W | S2 | combo-A2 | SE | vs A2 | combo-W | SE | vs W | combo-S2 | SE | vs S2 |")
print(hdr)
print("|" + "---|" * 16)
losing = []
for n in NS:
    s2n, a2n, wn = stats(draw("normal", n))
    s2_sorted = np.sort(s2n)
    a2_sorted = np.sort(a2n)
    c_s2_05 = np.quantile(s2n, 0.95)
    c_a2_05 = np.quantile(a2n, 0.95)
    c_w_05 = np.quantile(wn, 0.05)
    c_s2_025 = np.quantile(s2n, 0.975)
    c_a2_025 = np.quantile(a2n, 0.975)
    for law in LAWS:
        s2, a2, w = (s2n, a2n, wn) if law == "normal" else stats(draw(law, n))
        p_s2 = pval_upper(s2_sorted, s2)
        p_a2 = pval_upper(a2_sorted, a2)
        r_bonf = (np.minimum(p_s2, p_a2) < 0.025).astype(float)
        r_either = ((s2 > c_s2_025) | (a2 > c_a2_025)).astype(float)
        r_a2 = (a2 > c_a2_05).astype(float)
        r_w = (w < c_w_05).astype(float)
        r_s2 = (s2 > c_s2_05).astype(float)
        for name, r in (("bonf-maxp", r_bonf), ("either-2.5", r_either)):
            d_a = r - r_a2
            d_w = r - r_w
            d_s = r - r_s2
            se_a = d_a.std(ddof=1) / np.sqrt(NSIM)
            se_w = d_w.std(ddof=1) / np.sqrt(NSIM)
            se_s = d_s.std(ddof=1) / np.sqrt(NSIM)
            if law == "normal":
                va = vw = vs = "size"
            else:
                va = verdict(d_a.mean(), se_a)
                vw = verdict(d_w.mean(), se_w)
                vs = within(d_s.mean(), se_s)
                if va == "loss":
                    losing.append((name, n, law, "A2", d_a.mean(), d_a.mean() / se_a))
                if vw == "loss":
                    losing.append((name, n, law, "W", d_w.mean(), d_w.mean() / se_w))
            print(f"| {name} | {n} | {law} | {r.mean():.4f} | {r_a2.mean():.4f} | {r_w.mean():.4f} | {r_s2.mean():.4f} | "
                  f"{d_a.mean():+.4f} | {se_a:.4f} | {va} | {d_w.mean():+.4f} | {se_w:.4f} | {vw} | "
                  f"{d_s.mean():+.4f} | {se_s:.4f} | {vs} |")
        sys.stdout.flush()

print()
if losing:
    print("Losing cells (combination loses by more than two paired SE):")
    for name, n, law, ref, d, z in losing:
        print(f"- {name}, n={n}, {law}, vs {ref}: diff {d:+.4f} ({z:+.1f} SE)")
else:
    print("No losing cells: both combinations are omnibus-safe at the two-SE criterion on these four laws.")
