#!/usr/bin/env python3
"""Cycle 90: capped AD sum S2 (c=2) vs plain Anderson-Darling A2 vs Shapiro-Wilk W.

Run: uv run --with numpy --with scipy python stuff/s2-vs-ad-vs-sw-seed90101.py
Output: markdown rows for stuff/s2-vs-ad-vs-sw-seed90101.md
"""
import sys
import numpy as np
from scipy.stats import norm, shapiro, t as student_t, chi2

SEED = 90101
NSIM = 20000
NS = (25, 50, 100)
rng = np.random.default_rng(SEED)


def ad_terms(x):
    """t_i = -((2i-1)/n) [ln Phi(z_(i)) + ln(1-Phi(z_(n+1-i)))], z sample-standardized."""
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
    s2 = np.sum(np.log1p(2 * t), axis=1) / 2  # capped sum, c=2
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


print(f"seed {SEED}, {NSIM} sims per (n, law); SE = paired Monte Carlo SE of the mean difference of per-sample rejection indicators")
print()
print("| n | law | rej S2 | rej A2 | rej W | S2-A2 | SE | S2 vs A2 | S2-W | SE | S2 vs W |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
worst = []
for n in NS:
    s2n, a2n, wn = stats(draw("normal", n))
    c_s2 = np.quantile(s2n, 0.95)
    c_a2 = np.quantile(a2n, 0.95)
    c_w = np.quantile(wn, 0.05)
    for law in LAWS:
        s2, a2, w = (s2n, a2n, wn) if law == "normal" else stats(draw(law, n))
        r_s2 = (s2 > c_s2).astype(float)
        r_a2 = (a2 > c_a2).astype(float)
        r_w = (w < c_w).astype(float)
        d_a = r_s2 - r_a2
        d_w = r_s2 - r_w
        se_a = d_a.std(ddof=1) / np.sqrt(NSIM)
        se_w = d_w.std(ddof=1) / np.sqrt(NSIM)
        va = verdict(d_a.mean(), se_a) if law != "normal" else "size"
        vw = verdict(d_w.mean(), se_w) if law != "normal" else "size"
        print(f"| {n} | {law} | {r_s2.mean():.4f} | {r_a2.mean():.4f} | {r_w.mean():.4f} | "
              f"{d_a.mean():+.4f} | {se_a:.4f} | {va} | {d_w.mean():+.4f} | {se_w:.4f} | {vw} |")
        if law != "normal":
            worst.append((n, law, d_a.mean(), se_a, d_w.mean(), se_w))
        sys.stdout.flush()

print()
wa = min(worst, key=lambda r: r[2] / r[3])
ww = min(worst, key=lambda r: r[4] / r[5])
print(f"S2 vs A2 worst: n={wa[0]} {wa[1]} diff {wa[2]:+.4f} ({wa[2]/wa[3]:+.1f} SE)")
print(f"S2 vs W worst: n={ww[0]} {ww[1]} diff {ww[4]:+.4f} ({ww[4]/ww[5]:+.1f} SE)")
