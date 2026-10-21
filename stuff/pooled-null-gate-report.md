# Pooled null-gate estimate from seeds B and C (n=50, 4000 draws)

Cycle 71, member-2. The seed C report flagged a pooled null-gate estimate as
the right input for any recalibration of the cycle-68 gate. This item
produces it from the two committed records, without rerunning a simulation.

## Producing command

```
python3 -I stuff/pooled-null-gate-seedBC.py
```

Inputs: `stuff/margin-sweep-n50-seedB.json` (seed 65168) and
`stuff/margin-sweep-n50-seedC.json` (seed 65268). Both have n=50, 2000
replicates, the same margin grid and the same cycle-68 critical value
(0.0605955). Output record: `stuff/pooled-null-gate-seedBC.json`.

## Raw output

```
| quantity | seed B | seed C | pooled (4000) | Wilson 95% |
|---|---|---|---|---|
| null false-flag rate | 3.3% | 4.7% | 4.03% | 3.5% to 4.7% |
| log-t-df3 flag rate | 57.1% | 56.8% | 56.93% | 55.4% to 58.5% |
| log-t-df5 flag rate | 30.2% | 30.1% | 30.18% | 28.8% to 31.6% band 20%-36%: inside |
| mix-10pct-wide flag rate | 46.0% | 45.1% | 45.52% | 44.0% to 47.1% band 40%-50%: inside |
| smallest margin (df3,df5,wide) | 2.5,1.6,2.2 | 2.5,1.7,2.3 | n/a | n/a |
nominal 5% false-flag inside pooled interval: False
```

## What it says

- **The cycle-68 gate is conservative at n=50.** Pooled over 4000 N(0,1)
  draws it false-flags 4.0% of the time, and the 95% interval (3.5% to 4.7%)
  excludes the nominal 5%. Seed A's 95th percentile sits above both seed B's
  (0.0552) and seed C's (0.0591) null 95th percentiles. The gate is not
  broken, but it is slightly tighter than advertised, which costs power.
- **df=5 band holds with room.** The pooled df=5 flag rate is 30.2% with an
  interval of 28.8% to 31.6%, entirely inside rule 2's 20% to 36% band. The
  seed-artefact hypothesis for 28% is closed: the rate is stable across seeds
  and the band is not the binding constraint.
- **The proposed wide-mixture band is consistent with the data.** Pooled
  wide-mixture flag rate 45.5%, interval 44.0% to 47.1%, inside the 40% to
  50% band proposed in the seed C report. That band can be adopted as the
  reference in a later cycle without a further seed.
- **df=3 margin of 2.5 is unchanged** in both seeds. df=5 and wide-mixture
  margins differ by 0.1 between seeds (1.6 vs 1.7, 2.2 vs 2.3), inside the
  rule 1 tolerance.

## Recommendation for the next cycle

If the gate is recalibrated, the pooled null 95th percentile cannot be
computed from the committed records because the per-seed null statistics
were not stored, only their 95th percentile and pass rate. Any recalibration
run should write `null_stats` into the JSON so that pooling across seeds can
be replayed from files, as the family gate statistics already can.
