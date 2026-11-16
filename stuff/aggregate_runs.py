#!/usr/bin/env python3
"""Aggregate per-run tau_int(|M|) results into per-L mean +- run-to-run SE,
and check cycle 111 rule 1 requirements.

Input (stdin or file), one run per line, '#' comments allowed:
    L  seed  warmup_sweeps  sweeps  tau_int

Output: one line per L: "L mean_tau SE n_runs" (suitable as fit input),
plus rule-1 checks on stderr:
  - L=256 has >= 10 runs
  - L=128 runs have >= 1.0M sweeps
  - every run is >= 1000 tau_int long (sweeps / tau_int >= 1000)
  - seeds are unique (new, independent seeds)
Exit status 1 if any check fails.
"""
import math
import sys
from collections import defaultdict


def main(argv):
    src = open(argv[1]) if len(argv) > 1 else sys.stdin
    runs = defaultdict(list)
    seeds = set()
    problems = []
    for n, line in enumerate(src, 1):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        L, seed, warm, sweeps, tau = line.split()[:5]
        L, warm, sweeps, tau = int(L), int(warm), int(float(sweeps)), float(tau)
        if seed in seeds:
            problems.append(f"line {n}: seed {seed} reused")
        seeds.add(seed)
        if sweeps / tau < 1000:
            problems.append(f"line {n}: L={L} run is {sweeps / tau:.0f} tau_int (<1000)")
        if L == 128 and sweeps < 1_000_000:
            problems.append(f"line {n}: L=128 run has {sweeps} sweeps (<1.0M)")
        runs[L].append(tau)

    print("# L mean_tau_int SE n_runs")
    for L in sorted(runs):
        t = runs[L]
        m = sum(t) / len(t)
        se = (math.sqrt(sum((x - m) ** 2 for x in t) / (len(t) - 1) / len(t))
              if len(t) > 1 else float("nan"))
        print(f"{L} {m:.4f} {se:.4f} {len(t)}")

    if len(runs.get(256, [])) < 10:
        problems.append(f"L=256 has {len(runs.get(256, []))} runs (<10)")
    for p in problems:
        print("FAIL:", p, file=sys.stderr)
    if not problems:
        print("rule 1 checks: all pass", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
