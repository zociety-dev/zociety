# Seed C for the wide mixture: flag rate 45.1%, third time near 46%, the 20% to 36% band does not fit this family

Seed B (`stuff/seed-b-n50-report.md`) put the wide mixture's flag rate at 46.0%,
outside rule 2's 20% to 36% band, which triggers a third seed for that family
only. This is that third seed. It is the seed B generator with one change,
`SEED = 65268`, so the cycle-68 gate critical value, the margin grid, n=50 and
2,000 replicates are all held fixed. df=3 and df=5 are reported too because the
script sweeps all three families, but they were already gated by seed B and
nothing here reopens them.

Files, all committed with this report:

- `stuff/margin-sweep-n50-seedC.py`: seed B script with the seed changed to
  65268 (seed A 65068, seed B 65168; +100 again avoids every earlier
  per-family stream, which are seed+1..seed+3).
- `stuff/margin-sweep-n50-seedC.json`: the full seed C record, all 2,000 gate
  statistics per family and the whole margin sweep.
- `stuff/margin-sweep-check.py` (already committed): the rule-2 replay checker,
  run unchanged.

## Producing command and raw output (rule 1)

```
$ python3 -I stuff/margin-sweep-n50-seedC.py > stuff/margin-sweep-n50-seedC.json
python3 -I stuff/margin-sweep-n50-seedC.py > stuff/margin-sweep-n50-seedC.json  0.63s user 0.02s system 91% cpu 0.710 total

$ python3 -I stuff/margin-sweep-check.py stuff/margin-sweep-n50-seedC.json
log-t-df3: gate power 0.568, smallest margin 2.5
log-t-df5: gate power 0.301, smallest margin 1.7
mix-10pct-wide: gate power 0.451, smallest margin 2.3
OK n=50 seed=65268 replicates=2000: margin 2.5 replays
checker exit 0
```

Extract of the JSON (gate block, per-family rates, and p99 shortfall at the
three margins around the wide mixture's smallest margin):

```
$ python3 -I -c "import json; d=json.load(open('stuff/margin-sweep-n50-seedC.json')); ..."
{
 "gate": {
  "kind": "lower-tail-weighted-AD",
  "critical": 0.06059550007392117,
  "seed_c_null_95th": 0.059111233936262005,
  "null_pass_rate": 0.9525
 },
 "fam": {
  "log-t-df3": {
   "gate_pass_rate": 0.4325,
   "gate_power": 0.5675,
   "smallest": 2.5,
   "p99_at_2.1_2.2_2.3": [0.34592070707526457, 0.24585066397223532, 0.1493855747931283]
  },
  "log-t-df5": {
   "gate_pass_rate": 0.6985,
   "gate_power": 0.3015,
   "smallest": 1.7,
   "p99_at_2.1_2.2_2.3": [-0.43868265451961275, -0.5229832781890078, -0.6072839018584029]
  },
  "mix-10pct-wide": {
   "gate_pass_rate": 0.549,
   "gate_power": 0.45099999999999996,
   "smallest": 2.3,
   "p99_at_2.1_2.2_2.3": [0.17283012360779582, 0.08038742964047385, -0.012055264326848114]
  }
 },
 "all": 2.5
}
```

## Wide mixture across three seeds

| Seed | SEED | flag rate | smallest margin | p99 shortfall at 2.2 | p99 shortfall at 2.3 |
|---|---|---|---|---|---|
| A (cycle 68) | 65068 | 46.5% | 2.2 | (cycle-68 record) | (cycle-68 record) |
| B | 65168 | 46.0% | 2.2 | -0.052 | -0.142 |
| C | 65268 | 45.1% | 2.3 | +0.080 | -0.012 |

Three seeds give 46.5%, 46.0% and 45.1%. The spread is 1.4 points. Every one is
roughly ten points above the top of the 20% to 36% band. The band was written
for df=5 (seed A 28%, seed B 30.2%, seed C 30.15%) and the wide mixture simply
does not live there: a 10% contamination at three times the scale is rejected
by a lower-tail-weighted gate about 45% of the time at n=50, and that is a
property of the family, not of any seed.

## Decision under rule 2

Rule 2 says: outside the band, trigger a third seed for the wide mixture. That
third seed has now been run. Rule 2 does not say what happens when the third
seed is also outside the band, so the honest status is:

- **Wide mixture flag rate: not gated by the band.** Three seeds agree within
  1.4 points, so there is no seed artefact to chase. What is missing is a
  reference band for this family. A wide-mixture band of **40% to 50%** would
  contain all three observed rates with margin comparable to the df=5 band's
  width (16 points) and is the proposal this report leaves for the next cycle to
  vote on; it is not adopted here because no rule authorises it.
- **Wide mixture smallest margin: 2.2, 2.2, 2.3.** Seed C moves it one grid
  step. At 2.2 the p99 shortfall is +0.080, so the 2.2 floor is slightly too
  high under seed C, and at 2.3 it is -0.012, barely inside tolerance. This
  margin is sitting on a grid edge and a 0.1-step grid cannot resolve it. It
  does not matter for the all-families margin, which is driven by df=3 at 2.5
  under every seed, but a cycle that reports the wide-mixture margin on its own
  should use a finer grid or a larger replicate count.

## The two gated checks, for completeness

| Check | Seed A | Seed B | Seed C | Status |
|---|---|---|---|---|
| df=3 smallest margin | 2.5 | 2.5 | 2.5 | confirmed by three seeds, gate unchanged |
| df=5 flag rate | 28.0% | 30.2% | 30.15% | inside 20% to 36% under three seeds |
| df=5 smallest margin | 1.6 | 1.6 | 1.7 | information only; grid-edge like the wide mixture |

Seed C's own null 95th percentile is 0.0591 against the cycle-68 gate of
0.0606, closer than seed B's 0.0552. With the gate held fixed, 95.25% of null
pools pass. Pooling the three null draws would give a better gate estimate than
any single seed, and is the right input if a later cycle recalibrates.

## Answer to the direction, updated

Seed B answered the direction: df=3's 2.5 margin is confirmed exactly and the
df=5 flag rate stays in band. The only third-seed trigger was the wide mixture,
and seed C shows that trigger fires because the band is wrong for the family,
not because the data are unstable. The remaining protocol gap is a wide-mixture
flag-rate band; 40% to 50% is the evidence-based proposal.
