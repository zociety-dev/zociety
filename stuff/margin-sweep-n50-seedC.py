#!/usr/bin/env python3
"""Seed C: third seed of the n=50 sweep, triggered by rule 2 for the wide mixture (cycle 71). Same gate, same grid, only the seed changes.

Model (stated so the trace can be replayed, not re-read):
  * A pool is n i.i.d. log-values from one tail family.
  * The pooled floor is  mean - (z01 + margin) * sd  on the log scale,
    where z01 = 2.326 is the normal 1% quantile. margin is the tail margin.
  * The floor is correct when it sits at or below the family's true 1% quantile.
    shortfall = floor - true_q01; positive means the floor is too high.
  * Tail-weighted Anderson-Darling gate: the usual AD statistic on standardized
    data against N(0,1), but with only the lower-tail weight 1/F(x) (we only care
    about the lower tail). Gate passes when the statistic is below GATE_CRIT.
    Pools failing the gate are rejected and do not contribute a floor.
  * Simulated p99 at a margin = 99th percentile of shortfall over gate-passing
    replicates. Tolerance (rule 1): p99 <= TOL. Smallest margin is the first
    grid point meeting that.
Pure python, fixed seed, no third-party deps.
"""
import json, math, random, sys

N = 50
REPS = 2000
SEED = 65268          # seed C (seed A 65068, seed B 65168; +100 again avoids both sets of per-family streams)
Z01 = 2.326
TOL = 0.0
GATE_CRIT = 0.06059550007392117   # cycle-68 gate: seed A null 95th percentile, NOT recalibrated
MARGINS = [round(0.1 * k, 1) for k in range(0, 81)]
FAMILIES = ["log-t-df3", "log-t-df5", "mix-10pct-wide"]


def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def t_quantile_01(df):
    # numeric inverse of Student-t CDF at 0.01 via bisection
    def cdf(x):
        # integrate density numerically (Simpson) from x to 0, symmetric
        c = math.gamma((df + 1) / 2) / (math.sqrt(df * math.pi) * math.gamma(df / 2))
        a, b, m = x, 0.0, 4000
        h = (b - a) / m
        s = 0.0
        for i in range(m + 1):
            u = a + i * h
            w = 1 if i in (0, m) else (4 if i % 2 else 2)
            s += w * c * (1 + u * u / df) ** (-(df + 1) / 2)
        return 0.5 - s * h / 3
    lo, hi = -50.0, 0.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if cdf(mid) < 0.01:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def mix_quantile_01():
    def cdf(x):
        return 0.9 * phi(x) + 0.1 * phi(x / 3.0)
    lo, hi = -20.0, 0.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if cdf(mid) < 0.01:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def draw(rng, fam):
    if fam.startswith("log-t"):
        df = int(fam[-1])
        return [rng.gauss(0, 1) / math.sqrt(rng.gammavariate(df / 2, 2 / df)) for _ in range(N)]
    return [rng.gauss(0, 3.0 if rng.random() < 0.1 else 1.0) for _ in range(N)]


def lower_tail_ad(xs):
    m = sum(xs) / len(xs)
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))
    z = sorted((x - m) / sd for x in xs)
    n = len(z)
    s = 0.0
    for i, v in enumerate(z, start=1):
        f = min(max(phi(v), 1e-12), 1 - 1e-12)
        fn = (i - 0.5) / n
        s += (fn - f) ** 2 / f          # lower-tail weight only
    return s / n * n ** 0.5             # scaled so N(0,1) reference ~ O(1)


def pct(vals, p):
    v = sorted(vals)
    k = max(0, min(len(v) - 1, math.ceil(p * len(v)) - 1))
    return v[k]


def main():
    global GATE_CRIT
    out = {"n": N, "replicates": REPS, "seed": SEED, "z01": Z01, "tolerance": TOL,
           "gate": {"kind": "lower-tail-weighted-AD", "critical": GATE_CRIT},
           "margins": MARGINS, "families": {}}
    # calibrate: null pass rate of the gate on N(0,1)
    rng = random.Random(SEED)
    null_stats = [lower_tail_ad([rng.gauss(0, 1) for _ in range(N)]) for _ in range(REPS)]
    out["gate"]["seed_c_null_95th"] = pct(null_stats, 0.95)  # reported only; gate stays at cycle-68 value
    out["gate"]["critical"] = GATE_CRIT
    out["gate"]["null_pass_rate"] = sum(s < GATE_CRIT for s in null_stats) / REPS
    true_q = {"log-t-df3": t_quantile_01(3), "log-t-df5": t_quantile_01(5),
              "mix-10pct-wide": mix_quantile_01()}
    for fam in FAMILIES:
        rng = random.Random(SEED + FAMILIES.index(fam) + 1)
        stats, means, sds = [], [], []
        for _ in range(REPS):
            xs = draw(rng, fam)
            m = sum(xs) / N
            sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (N - 1))
            stats.append(lower_tail_ad(xs)); means.append(m); sds.append(sd)
        passing = [i for i, s in enumerate(stats) if s < GATE_CRIT]
        rows = []
        smallest = None
        for mg in MARGINS:
            short = [(means[i] - (Z01 + mg) * sds[i]) - true_q[fam] for i in passing]
            p99 = pct(short, 0.99) if short else None
            rows.append({"margin": mg, "p99_shortfall": p99,
                         "within_tolerance": (p99 is not None and p99 <= TOL)})
            if smallest is None and p99 is not None and p99 <= TOL:
                smallest = mg
        out["families"][fam] = {
            "true_q01": true_q[fam],
            "gate_pass_rate": len(passing) / REPS,
            "gate_power": 1 - len(passing) / REPS,
            "gate_stats": [round(s, 6) for s in stats],
            "sweep": rows,
            "smallest_margin_within_tolerance": smallest,
        }
    out["smallest_margin_all_families"] = max(
        (f["smallest_margin_within_tolerance"] for f in out["families"].values()
         if f["smallest_margin_within_tolerance"] is not None), default=None)
    json.dump(out, sys.stdout, indent=1)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
