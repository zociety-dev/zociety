#!/usr/bin/env python3
"""Skew-corrected analytic intercept for the ratio margin.

The alt statistic is noncentral chi2(3, lambda) with lambda = 0.12 n.
The old analytic intercept 0.303 = (3 - 0.634) / 7.815 assumes the median
sits 0.634 below the mean at every n, as it does for the central chi2(3).
The mean-median offset of a noncentral chi2 shrinks toward 0 as lambda
grows, so the analytic margin curve is concave in n and a straight-line fit
through it has a lower intercept than 0.303.

This script computes the exact median of ncx2(3, 0.12 n) at each n in the
grid, divides by chi2_95(3) = 7.815, fits margin = a + b n by OLS, and
reports a against the empirical fit a = 0.272 [0.240, 0.298].

Pure python: the ncx2 CDF is the Poisson mixture of central chi2 CDFs.
"""
import math

CHI2_95_3 = 7.815
EMPIRICAL_A = 0.272
EMPIRICAL_CI = (0.240, 0.298)
OLD_ANALYTIC_A = 0.303
GRID = [10, 15, 20, 30, 50, 100, 200]


def reg_lower_gamma(s, x):
    """P(s, x) by series; fine for the moderate x used here."""
    if x <= 0:
        return 0.0
    term = 1.0 / s
    total = term
    k = 1
    while True:
        term *= x / (s + k)
        total += term
        if term < total * 1e-15:
            break
        k += 1
    return total * math.exp(-x + s * math.log(x) - math.lgamma(s))


def chi2_cdf(x, k):
    return reg_lower_gamma(k / 2.0, x / 2.0)


def ncx2_cdf(x, k, lam):
    half = lam / 2.0
    total = 0.0
    j = 0
    w = math.exp(-half)
    while True:
        total += w * chi2_cdf(x, k + 2 * j)
        if j > half and w < 1e-14:
            break
        j += 1
        w *= half / j
    return total


def ncx2_median(k, lam):
    lo, hi = 0.0, k + lam + 10 * math.sqrt(2 * (k + 2 * lam)) + 10
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if ncx2_cdf(mid, k, lam) < 0.5:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def ols(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    return my - b * mx, b


def main():
    rows = []
    print(f"{'n':>5} {'lambda':>7} {'mean':>8} {'median':>8} {'offset':>7} {'margin':>7}")
    for n in GRID:
        lam = 0.12 * n
        mean = 3 + lam
        med = ncx2_median(3, lam)
        margin = med / CHI2_95_3
        rows.append((n, margin))
        print(f"{n:>5} {lam:>7.2f} {mean:>8.3f} {med:>8.3f} {mean - med:>7.3f} {margin:>7.3f}")

    a, b = ols([r[0] for r in rows], [r[1] for r in rows])
    print()
    print(f"central chi2(3) offset (mean - median): {3 - ncx2_median(3, 0.0):.3f}")
    print(f"old analytic intercept (constant offset): {OLD_ANALYTIC_A:.3f}")
    print(f"skew-corrected line fit: a = {a:.3f}, b = {b:.4f}")
    lo, hi = EMPIRICAL_CI
    inside = lo <= a <= hi
    print(f"empirical a = {EMPIRICAL_A:.3f} [{lo:.3f}, {hi:.3f}]")
    print(f"signed gap (corrected analytic - empirical): {a - EMPIRICAL_A:+.3f}")
    print("corrected analytic a lies", "inside" if inside else "outside",
          "the empirical bootstrap interval")
    print()
    print("Model update: a_analytic = (3 - offset_eff) / 7.815 where offset_eff is")
    print("the line-fit-averaged mean-median offset of ncx2(3, 0.12 n) over the grid,")
    print(f"not the central value 0.634; that gives {a:.3f}, not {OLD_ANALYTIC_A:.3f}.")


if __name__ == "__main__":
    main()
