#!/usr/bin/env python3
"""df=3 margin at n=25, 50, 100 under rule 2's step-and-interval moved test.

Rule 1 gives us stored per-draw NULL statistics (stuff/null-draws.csv). The
margin also needs ALTERNATIVE draws, so this script generates t(df=3) draws
with the same gate statistic, same seeds and same draw count, stores them one
row per draw (stuff/df3-draws.csv), and then evaluates the margin from stored
rows only, never from point values.

Definition used (stated because the cycle 71 point value 2.5 came with none
that survives in stuff/): margin(n, seed) = median gate statistic under t(3)
divided by the null 95th percentile at that n from null-draws.csv. A margin of
1.0 means the typical heavy-tailed sample sits exactly on the null critical;
2.5 means it sits two and a half criticals out.

Rule 2 moved test against the old value 2.5 with step 0.1:
  (a) |new - old| > step, and
  (b) the 95% bootstrap interval of the new margin excludes old.
Bootstrap: 2000 paired resamples; each resample redraws the t(3) rows and the
null rows with replacement and recomputes median/p95. Seed 65075.

Output (stdout, CSV): n,seed,draws,margin,boot_lo,boot_hi,exceeds_step,
interval_excludes_old,moved  for each seed and pooled.
Side effect: writes stuff/df3-draws.csv (n,seed,draw,stat).
Pure python, no third-party deps.
Usage: python3 -I stuff/df3-margin-moved-test.py > stuff/df3-margin-moved-test.csv
"""
import csv, math, os, random, sys

NS = (25, 50, 100)
SEEDS = (65068, 65069)
REPS = 2000
OLD_MARGIN = 2.5
STEP = 0.1
BOOT = 2000
BOOT_SEED = 65075
HERE = os.path.dirname(os.path.abspath(__file__))
NULL_CSV = os.path.join(HERE, "null-draws.csv")
ALT_CSV = os.path.join(HERE, "df3-draws.csv")


def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def lower_tail_ad(xs):
    m = sum(xs) / len(xs)
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))
    z = sorted((x - m) / sd for x in xs)
    n = len(z)
    s = 0.0
    for i, v in enumerate(z, start=1):
        f = min(max(phi(v), 1e-12), 1 - 1e-12)
        fn = (i - 0.5) / n
        s += (fn - f) ** 2 / f
    return s / n * n ** 0.5


def pct(vals, p):
    v = sorted(vals)
    k = max(0, min(len(v) - 1, math.ceil(p * len(v)) - 1))
    return v[k]


def t3(rng):
    g = rng.gauss(0, 1)
    chi = sum(rng.gauss(0, 1) ** 2 for _ in range(3))
    return g / math.sqrt(chi / 3.0)


def load_null():
    null = {}
    with open(NULL_CSV, newline="") as fh:
        for row in csv.DictReader(fh):
            null.setdefault((int(row["n"]), int(row["seed"])), []).append(float(row["stat"]))
    return null


def gen_alt():
    alt = {}
    with open(ALT_CSV, "w") as out:
        out.write("n,seed,draw,stat\n")
        for n in NS:
            for seed in SEEDS:
                rng = random.Random(seed + 1000)
                stats = []
                for d in range(REPS):
                    s = lower_tail_ad([t3(rng) for _ in range(n)])
                    stats.append(s)
                    out.write(f"{n},{seed},{d},{s:.6f}\n")
                alt[(n, seed)] = stats
    return alt


def margin(alt_stats, null_stats):
    return pct(alt_stats, 0.5) / pct(null_stats, 0.95)


def boot_interval(alt_stats, null_stats, rng):
    vals = []
    na, nn = len(alt_stats), len(null_stats)
    for _ in range(BOOT):
        a = [alt_stats[rng.randrange(na)] for _ in range(na)]
        b = [null_stats[rng.randrange(nn)] for _ in range(nn)]
        vals.append(margin(a, b))
    return pct(vals, 0.025), pct(vals, 0.975)


def main():
    null = load_null()
    alt = gen_alt()
    rng = random.Random(BOOT_SEED)
    sys.stdout.write(f"old value {OLD_MARGIN}, step {STEP}, margin = median t(3) stat / null p95, "
                     f"bootstrap {BOOT} paired resamples seed {BOOT_SEED}\n")
    sys.stdout.write("n,seed,draws,margin,boot_lo,boot_hi,exceeds_step,interval_excludes_old,moved\n")
    for n in NS:
        cases = [("pooled", sum((alt[(n, s)] for s in SEEDS), []), sum((null[(n, s)] for s in SEEDS), []))]
        cases += [(str(s), alt[(n, s)], null[(n, s)]) for s in SEEDS]
        for label, a, b in cases:
            m = margin(a, b)
            lo, hi = boot_interval(a, b, rng)
            ex_step = int(abs(m - OLD_MARGIN) > STEP)
            ex_int = int(OLD_MARGIN < lo or OLD_MARGIN > hi)
            sys.stdout.write(f"{n},{label},{len(a)},{m:.3f},{lo:.3f},{hi:.3f},{ex_step},{ex_int},{ex_step and ex_int}\n")


if __name__ == "__main__":
    main()
