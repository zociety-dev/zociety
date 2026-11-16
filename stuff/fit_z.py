#!/usr/bin/env python3
"""Weighted straight power-law fit tau_int = A * L^z for cycle 111 (rule 2).

Input (stdin or file): one line per L: "L mean_tau_int run_to_run_SE".
Lines starting with '#' are ignored. Fit is restricted to Lmin..Lmax
(default 64..256) as a weighted linear fit of ln tau vs ln L, with
sigma_ln = SE/mean.

Reports z +- SE, chi2/dof, and distance from 2.17 and from the cycle-110
L=32..128 fit (2.084 +- 0.032) in combined SE.

Optional: --l128-check NEW_MEAN NEW_SE OLD_MEAN OLD_SE prints the gap between
the rerun L=128 mean tau_int and cycle 110's value in combined SE, flagging
any gap above 2 SE.

This script performs no simulation. It needs per-L data from
stuff/ising_tau_int.c runs (>=10 L=256 runs, five L=128 reruns at >=1.0M
sweeps); none were available when it was written.
"""
import math
import sys


def fit(points):
    sw = sx = sy = sxx = sxy = 0.0
    for L, m, se in points:
        x, y = math.log(L), math.log(m)
        w = 1.0 / (se / m) ** 2
        sw += w; sx += w * x; sy += w * y; sxx += w * x * x; sxy += w * x * y
    d = sw * sxx - sx * sx
    z = (sw * sxy - sx * sy) / d
    a = (sxx * sy - sx * sxy) / d
    se_z = math.sqrt(sw / d)
    chi2 = sum(((math.log(m) - a - z * math.log(L)) / (se / m)) ** 2
               for L, m, se in points)
    dof = len(points) - 2
    return z, se_z, chi2, dof


def main(argv):
    lmin, lmax, path, check = 64, 256, None, None
    i = 0
    while i < len(argv):
        if argv[i] == "--lmin":
            lmin = int(argv[i + 1]); i += 2
        elif argv[i] == "--lmax":
            lmax = int(argv[i + 1]); i += 2
        elif argv[i] == "--l128-check":
            check = [float(v) for v in argv[i + 1:i + 5]]; i += 5
        else:
            path = argv[i]; i += 1
    src = open(path) if path else sys.stdin
    pts = []
    for line in src:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        L, m, se = line.split()[:3]
        if lmin <= int(L) <= lmax:
            pts.append((int(L), float(m), float(se)))
    if len(pts) < 2:
        sys.exit("need at least 2 L values in range")
    z, se_z, chi2, dof = fit(pts)
    print(f"L={lmin}..{lmax} n={len(pts)}  z = {z:.4f} +- {se_z:.4f}")
    print(f"chi2/dof = {chi2:.3f}/{dof}" + (f" = {chi2/dof:.3f}" if dof > 0 else " (no dof)"))
    print(f"distance from 2.17: {(z - 2.17) / se_z:+.2f} SE")
    comb = math.hypot(se_z, 0.032)
    print(f"distance from 2.084+-0.032: {(z - 2.084) / comb:+.2f} combined SE")
    if check:
        nm, ns, om, os_ = check
        g = (nm - om) / math.hypot(ns, os_)
        flag = "  FLAG >2 SE" if abs(g) > 2 else ""
        print(f"L=128 rerun vs cycle 110: {g:+.2f} combined SE{flag}")


if __name__ == "__main__":
    main(sys.argv[1:])
