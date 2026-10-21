#!/usr/bin/env python3
"""Pool seed B and seed C (n=50, 2000 replicates each) into one 4000-draw estimate.

Reads the committed records stuff/margin-sweep-n50-seedB.json and
stuff/margin-sweep-n50-seedC.json and, without rerunning any simulation:

  1. Pools the null pass rate of the cycle-68 gate (reported per seed as
     gate.null_pass_rate over `replicates` N(0,1) draws) into one rate with a
     Wilson 95% interval, so the next cycle can decide whether the gate is
     still a 5% gate or has drifted.
  2. Pools the per-replicate gate statistics of each tail family (stored
     verbatim in families.<fam>.gate_stats) and recomputes the flag rate
     (share of statistics above gate.critical) with a Wilson interval. This is
     the pooled df=5 flag rate that rule 2's 20% to 36% band is checked
     against, and the pooled wide-mixture rate the proposed 40% to 50% band
     would be checked against.
  3. Checks that the two seeds share n, replicates, gate.critical and margin
     grid, so pooling is legitimate.

Usage: python3 -I stuff/pooled-null-gate-seedBC.py
Writes stuff/pooled-null-gate-seedBC.json and prints a markdown table.
"""
import json
import math

FILES = ("stuff/margin-sweep-n50-seedB.json", "stuff/margin-sweep-n50-seedC.json")
FAMILIES = ("log-t-df3", "log-t-df5", "mix-10pct-wide")
BANDS = {"log-t-df5": (0.20, 0.36), "mix-10pct-wide": (0.40, 0.50)}


def wilson(k, n, z=1.96):
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return centre - half, centre + half


def main():
    recs = [json.load(open(f)) for f in FILES]
    a, b = recs
    for key in ("n", "replicates", "tolerance", "margins"):
        assert a[key] == b[key], f"seeds disagree on {key}"
    assert a["gate"]["critical"] == b["gate"]["critical"], "gate.critical differs"
    crit = a["gate"]["critical"]
    reps = a["replicates"]
    total = reps * len(recs)

    out = {
        "sources": list(FILES),
        "seeds": [r["seed"] for r in recs],
        "n": a["n"],
        "replicates_per_seed": reps,
        "pooled_draws": total,
        "gate_critical": crit,
        "null": {},
        "families": {},
    }

    null_pass = sum(round(r["gate"]["null_pass_rate"] * reps) for r in recs)
    lo, hi = wilson(null_pass, total)
    out["null"] = {
        "per_seed_pass_rate": [r["gate"]["null_pass_rate"] for r in recs],
        "pooled_pass_rate": null_pass / total,
        "pooled_false_flag_rate": 1 - null_pass / total,
        "wilson95": [1 - hi, 1 - lo],
        "nominal_false_flag_rate": 0.05,
        "nominal_inside_interval": (1 - hi) <= 0.05 <= (1 - lo),
    }

    rows = []
    for fam in FAMILIES:
        stats = []
        for r in recs:
            s = r["families"][fam]["gate_stats"]
            assert len(s) == reps, f"{fam}: expected {reps} gate_stats"
            stats.extend(s)
        flagged = sum(x > crit for x in stats)
        lo, hi = wilson(flagged, total)
        entry = {
            "per_seed_flag_rate": [1 - r["families"][fam]["gate_pass_rate"] for r in recs],
            "pooled_flag_rate": flagged / total,
            "wilson95": [lo, hi],
            "smallest_margin_per_seed": [
                r["families"][fam]["smallest_margin_within_tolerance"] for r in recs
            ],
        }
        if fam in BANDS:
            blo, bhi = BANDS[fam]
            entry["band"] = [blo, bhi]
            entry["pooled_inside_band"] = blo <= flagged / total <= bhi
            entry["interval_inside_band"] = blo <= lo and hi <= bhi
        out["families"][fam] = entry
        rows.append((fam, entry))

    with open("stuff/pooled-null-gate-seedBC.json", "w") as fh:
        json.dump(out, fh, indent=1)

    nl = out["null"]
    print("| quantity | seed B | seed C | pooled (4000) | Wilson 95% |")
    print("|---|---|---|---|---|")
    print(
        f"| null false-flag rate | {1 - nl['per_seed_pass_rate'][0]:.1%} | "
        f"{1 - nl['per_seed_pass_rate'][1]:.1%} | {nl['pooled_false_flag_rate']:.2%} | "
        f"{nl['wilson95'][0]:.1%} to {nl['wilson95'][1]:.1%} |"
    )
    for fam, e in rows:
        band = ""
        if "band" in e:
            band = f" band {e['band'][0]:.0%}-{e['band'][1]:.0%}: " + (
                "inside" if e["pooled_inside_band"] else "OUTSIDE"
            )
        print(
            f"| {fam} flag rate | {e['per_seed_flag_rate'][0]:.1%} | "
            f"{e['per_seed_flag_rate'][1]:.1%} | {e['pooled_flag_rate']:.2%} | "
            f"{e['wilson95'][0]:.1%} to {e['wilson95'][1]:.1%}{band} |"
        )
    print(
        f"| smallest margin (df3,df5,wide) | "
        + " | ".join(
            ",".join(str(x) for x in (out['families'][f]['smallest_margin_per_seed'][i] for f in FAMILIES))
            for i in range(2)
        )
        + " | n/a | n/a |"
    )
    print(f"nominal 5% false-flag inside pooled interval: {nl['nominal_inside_interval']}")


if __name__ == "__main__":
    main()
