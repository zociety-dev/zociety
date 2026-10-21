#!/usr/bin/env python3
"""Replay checker for rule 2 over a committed margin sweep (stuff/margin-sweep-*.json).

Rule 2 asks that rule 1's gate be replayed by tooling rather than re-read by a
member. This script does that replay from the file alone, without rerunning the
simulation:

  1. Required fields: n, seed, replicates, gate.critical, and for each of the
     three tail families (log-t df=3, df=5, 10% wide mixture) the per-replicate
     gate statistics and the margin sweep with p99 shortfall.
  2. gate_stats has exactly `replicates` entries, and gate_pass_rate equals the
     share of statistics at or below gate.critical (within one replicate).
  3. Each sweep's within_tolerance flag agrees with p99_shortfall <= tolerance.
  4. smallest_margin_within_tolerance is the first margin that is within
     tolerance AND every larger margin is too (no non-monotone dips are hidden).
  5. smallest_margin_all_families equals the max over families.

Exit 0 and print the verified margin if every check passes; exit 1 listing
each failure otherwise. Usage: margin-sweep-check.py stuff/margin-sweep-n50.json
"""
import json
import sys

FAMILIES = ("log-t-df3", "log-t-df5", "mix-10pct-wide")


def check(d):
    errs = []
    for key in ("n", "seed", "replicates", "tolerance", "gate", "families"):
        if key not in d:
            errs.append(f"missing top-level field {key}")
    if errs:
        return errs, None
    reps, tol, crit = d["replicates"], d["tolerance"], d["gate"].get("critical")
    if crit is None:
        errs.append("missing gate.critical")
        return errs, None
    worst = None
    for fam in FAMILIES:
        f = d["families"].get(fam)
        if f is None:
            errs.append(f"{fam}: family missing")
            continue
        stats = f.get("gate_stats", [])
        if len(stats) != reps:
            errs.append(f"{fam}: {len(stats)} gate stats, expected {reps}")
        elif stats:
            rate = sum(s <= crit for s in stats) / len(stats)
            if abs(rate - f.get("gate_pass_rate", -1)) > 1.0 / reps:
                errs.append(f"{fam}: gate_pass_rate {f.get('gate_pass_rate')} != replayed {rate:.4f}")
        sweep = sorted(f.get("sweep", []), key=lambda r: r["margin"])
        if not sweep:
            errs.append(f"{fam}: empty sweep")
            continue
        for r in sweep:
            if (r["p99_shortfall"] <= tol) != r["within_tolerance"]:
                errs.append(f"{fam}: margin {r['margin']} flag disagrees with shortfall")
        smallest = None
        for i, r in enumerate(sweep):
            if all(s["p99_shortfall"] <= tol for s in sweep[i:]):
                smallest = r["margin"]
                break
        if smallest != f.get("smallest_margin_within_tolerance"):
            errs.append(f"{fam}: recorded smallest {f.get('smallest_margin_within_tolerance')} != replayed {smallest}")
        if smallest is None:
            errs.append(f"{fam}: no margin in the sweep holds; widen the grid")
        else:
            worst = smallest if worst is None else max(worst, smallest)
        print(f"{fam}: gate power {1 - f.get('gate_pass_rate', 0):.3f}, smallest margin {smallest}")
    if worst != d.get("smallest_margin_all_families"):
        errs.append(f"smallest_margin_all_families {d.get('smallest_margin_all_families')} != replayed {worst}")
    return errs, worst


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    with open(sys.argv[1]) as fh:
        data = json.load(fh)
    errors, margin = check(data)
    for e in errors:
        print("FAIL", e)
    if errors:
        sys.exit(1)
    print(f"OK n={data['n']} seed={data['seed']} replicates={data['replicates']}: margin {margin} replays")
