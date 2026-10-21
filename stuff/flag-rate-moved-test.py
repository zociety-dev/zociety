#!/usr/bin/env python3
"""Rule 2 step-and-interval test for the null false-flag rate, from stored draws.

Rule 2: a margin or flag rate counts as moved only if (a) the change exceeds
one step and (b) the new value's 95% interval excludes the old value, both
computed from the per-draw rows rule 1 requires, never from point values.

Old value: the cycle 68 point claim of a 4.0% null false-flag rate at n=50.
New values: the flag rate against the fixed cycle 68 critical at each n,
recomputed from stuff/null-draws.csv (rule 1 record), seeds pooled and
per seed. The 95% interval is a percentile bootstrap over the stored draw
rows (2000 resamples, fixed seed), not a binomial formula on a point value.

Step: the reporting resolution of the old claim, 0.1 percentage point
(4.0% was stated to one decimal). This is an assumption and is printed.

Usage: python3 -I stuff/flag-rate-moved-test.py < stuff/null-draws.csv
"""
import csv, random, sys

OLD_RATE = 0.040
STEP = 0.001
CRIT_C68 = 0.06059550007392117
BOOT = 2000
BOOT_SEED = 65074

rows = {}
for r in csv.DictReader(sys.stdin):
    key = (int(r["n"]), int(r["seed"]))
    rows.setdefault(key, []).append(float(r["stat"]) > CRIT_C68)

groups = {}
for (n, seed), flags in sorted(rows.items()):
    groups.setdefault(n, {})[seed] = flags
    groups[n].setdefault("pooled", []).extend(flags)

rng = random.Random(BOOT_SEED)


def boot_ci(flags):
    k = len(flags)
    rates = []
    for _ in range(BOOT):
        rates.append(sum(flags[rng.randrange(k)] for _ in range(k)) / k)
    rates.sort()
    return rates[int(0.025 * BOOT)], rates[int(0.975 * BOOT) - 1]


print(f"old value {OLD_RATE:.3f}, step {STEP:.3f}, critical {CRIT_C68:.6f}, "
      f"bootstrap {BOOT} resamples seed {BOOT_SEED}")
print("n,seed,draws,rate,boot_lo,boot_hi,exceeds_step,interval_excludes_old,moved")
for n in sorted(groups):
    seeds = sorted(s for s in groups[n] if s != "pooled")
    for seed in ["pooled"] + seeds:
        flags = groups[n][seed]
        rate = sum(flags) / len(flags)
        lo, hi = boot_ci(flags)
        a = abs(rate - OLD_RATE) > STEP
        b = OLD_RATE < lo or OLD_RATE > hi
        print(f"{n},{seed},{len(flags)},{rate:.4f},{lo:.4f},{hi:.4f},"
              f"{int(a)},{int(b)},{int(a and b)}")
