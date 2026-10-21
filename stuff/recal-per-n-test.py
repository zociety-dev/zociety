#!/usr/bin/env python3
"""Per-n recalibrated gate (rule 1) under rule 2's step-and-interval test.

Reads cycle 74's stored per-draw rows (null-draws.csv, df3-draws.csv, both
seeds pooled per rule 1). For each n in 25, 50, 100 the critical value is that
n's own pooled null p95, never the held n=50 value 0.060596.

Per n it reports, with 95% bootstrap intervals (2000 paired resamples,
seed 65076, resampling null and df=3 rows with replacement and recomputing
the critical from the resampled null rows):
  null_rate  : null false-flag rate at the per-n critical (5% by construction
               on the full rows; the bootstrap shows its sampling spread)
  df3_rate   : df=3 flag rate (power) at the per-n critical
  margin     : median df=3 stat / per-n null p95
  margin_held: same margin at the held n=50 critical, for contrast only

Rule 2 moved test, applied per quantity to the recalibrated values:
  step1 = v50 - v25, step2 = v100 - v50; moved iff sign(step1) == sign(step2)
  and |step1| > halfwidth of the wider of the n=25 / n=50 intervals and
  |step2| > halfwidth of the wider of the n=50 / n=100 intervals.
Pure python. Usage: python3 -I stuff/recal-per-n-test.py > stuff/recal-per-n-test.csv
"""
import csv, os, random, sys

NS = (25, 50, 100)
HELD = 0.060596
BOOT = 2000
BOOT_SEED = 65076
HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    out = {n: [] for n in NS}
    with open(os.path.join(HERE, name)) as f:
        for r in csv.DictReader(f):
            out[int(r["n"])].append(float(r["stat"]))
    return out


def pct(vals, p):
    v = sorted(vals)
    k = (len(v) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def stats(null, alt):
    crit = pct(null, 0.95)
    return {
        "null_rate": sum(x > crit for x in null) / len(null),
        "df3_rate": sum(x > crit for x in alt) / len(alt),
        "margin": pct(alt, 0.5) / crit,
        "margin_held": pct(alt, 0.5) / HELD,
        "crit": crit,
    }


null, alt = load("null-draws.csv"), load("df3-draws.csv")
rng = random.Random(BOOT_SEED)
res = {}
for n in NS:
    point = stats(null[n], alt[n])
    boots = {k: [] for k in point}
    for _ in range(BOOT):
        bn = rng.choices(null[n], k=len(null[n]))
        ba = rng.choices(alt[n], k=len(alt[n]))
        for k, v in stats(bn, ba).items():
            boots[k].append(v)
    res[n] = {k: (point[k], pct(boots[k], 0.025), pct(boots[k], 0.975)) for k in point}

w = csv.writer(sys.stdout)
w.writerow(["quantity", "n", "draws", "crit", "value", "boot_lo", "boot_hi"])
for q in ("null_rate", "df3_rate", "margin", "margin_held"):
    for n in NS:
        v, lo, hi = res[n][q]
        w.writerow([q, n, len(null[n]), f"{res[n]['crit'][0]:.6f}", f"{v:.4f}", f"{lo:.4f}", f"{hi:.4f}"])
w.writerow([])
w.writerow(["quantity", "step_25_50", "step_50_100", "same_sign", "hw_25_50", "hw_50_100", "step1_exceeds", "step2_exceeds", "moved"])
for q in ("null_rate", "df3_rate", "margin", "margin_held"):
    v = {n: res[n][q][0] for n in NS}
    hw = {n: (res[n][q][2] - res[n][q][1]) / 2 for n in NS}
    s1, s2 = v[50] - v[25], v[100] - v[50]
    same = (s1 > 0) == (s2 > 0) and s1 != 0 and s2 != 0
    h1, h2 = max(hw[25], hw[50]), max(hw[50], hw[100])
    e1, e2 = abs(s1) > h1, abs(s2) > h2
    w.writerow([q, f"{s1:.4f}", f"{s2:.4f}", int(same), f"{h1:.4f}", f"{h2:.4f}", int(e1), int(e2), int(same and e1 and e2)])
