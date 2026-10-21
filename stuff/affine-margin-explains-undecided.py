#!/usr/bin/env python3
"""Cycle 76, member-3: why the exponent fit is 'undecided' - the margin is affine in n.

Companion to stuff/n200-margin-exponent.py (member-2), which found a pooled
log-log slope of 0.786 [0.742, 0.840]: covers neither 0.5 nor 1.0, so rule 2
returns 'undecided'. This file checks the analytic reason.

Under the df=3 protocol each contrast is a standardized mean shifted by
DELTA*sqrt(n), so the alternative stat is non-central chi-square with 3 df and
noncentrality lambda = 3 * n * DELTA**2. Its mean is 3 + lambda, so

    margin(n) ~ (3 + 3*DELTA**2 * n) / chi2_95(df=3)

is AFFINE in n, not a power law. A power law fit to an affine curve gives a
slope strictly between 0 and 1 that rises toward 1 as n grows: 'undecided' is
the correct answer to a question posed with the wrong family.

This script
  1. computes the analytic affine prediction at n=25, 50, 100, 200;
  2. fits the observed pooled margins (from n200-margin-exponent.out) to
     a + b*n by least squares and reports the residuals;
  3. reports the local log-log slopes between adjacent n for both the
     observed and the affine curve, showing they climb toward 1.

Pure python. Run: python3 -I stuff/affine-margin-explains-undecided.py
"""
import math

NS = [25, 50, 100, 200]
DELTA = 0.2
CHI2_95_DF3 = 7.8147  # null p95 of chi-square(3); the stored null p95 sits here

# pooled (seed-averaged) margins from stuff/n200-margin-exponent.out
OBS = {25: (0.666 + 0.653) / 2,
       50: (1.042 + 1.071) / 2,
       100: (1.793 + 1.770) / 2,
       200: (3.319 + 3.491) / 2}


def affine_pred(n):
    lam = 3 * n * DELTA ** 2
    return (3 + lam) / CHI2_95_DF3


def lsq(xs, ys):
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    return my - b * mx, b


def local_slopes(curve):
    out = []
    for n0, n1 in zip(NS, NS[1:]):
        out.append((n0, n1, math.log(curve[n1] / curve[n0]) / math.log(n1 / n0)))
    return out


def main():
    print(f"DELTA={DELTA} chi2_95(df=3)={CHI2_95_DF3}")
    print("\nanalytic affine prediction vs observed pooled margin")
    pred = {n: affine_pred(n) for n in NS}
    for n in NS:
        print(f"  n={n:3d}: predicted={pred[n]:.3f} observed={OBS[n]:.3f} "
              f"ratio={OBS[n] / pred[n]:.3f}")
    print("  (observed sits below the mean-based prediction because the median "
          "of a noncentral chi-square is below its mean; the gap shrinks with n)")

    a, b = lsq(NS, [OBS[n] for n in NS])
    print(f"\nleast-squares affine fit to observed: margin = {a:.3f} + {b:.5f} * n")
    print(f"  analytic slope 3*DELTA^2/chi2_95 = {3 * DELTA ** 2 / CHI2_95_DF3:.5f}")
    ss_res = sum((OBS[n] - (a + b * n)) ** 2 for n in NS)
    my = sum(OBS.values()) / len(OBS)
    ss_tot = sum((OBS[n] - my) ** 2 for n in NS)
    print(f"  residuals: " + " ".join(f"{OBS[n] - (a + b * n):+.3f}" for n in NS))
    print(f"  R^2 = {1 - ss_res / ss_tot:.4f}")

    la, lb = lsq([math.log(n) for n in NS], [math.log(OBS[n]) for n in NS])
    print(f"\npower-law fit to observed (rule 2 family): slope = {lb:.3f}")

    print("\nlocal log-log slopes between adjacent n")
    for (n0, n1, so), (_, _, sp) in zip(local_slopes(OBS), local_slopes(pred)):
        print(f"  {n0:3d}->{n1:3d}: observed={so:.3f} affine={sp:.3f}")
    print("  both climb toward 1: an affine curve has no single exponent, "
          "so rule 2's sqrt(n)-vs-n question is undecided by construction.")

    print("\nverdict: margin is affine in n (a + b*n with a>0); the fitted "
          "exponent 0.79 is the power-law shadow of that line over 25..200, "
          "not evidence of a growth rate between sqrt(n) and n.")


if __name__ == "__main__":
    main()
