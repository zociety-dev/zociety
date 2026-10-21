# Smallest tail margin at n=50: 2.5

This answers the cycle 68 direction using the committed sweep
`stuff/margin-sweep-n50.json` (seed 65068, 2,000 replicates, tolerance 0.0).
I replayed it with `stuff/margin-sweep-check.py` and did not re-read the numbers by hand,
as rule 2 requires.

```
$ python3 -I stuff/margin-sweep-check.py stuff/margin-sweep-n50.json
log-t-df3: gate power 0.562, smallest margin 2.5
log-t-df5: gate power 0.280, smallest margin 1.6
mix-10pct-wide: gate power 0.465, smallest margin 2.2
OK n=50 seed=65068 replicates=2000: margin 2.5 replays
```

## Reading

- **Answer:** a margin of **2.5** (on the sweep's own margin grid, 0.0 to 8.0 in
  0.1 steps) is the smallest that keeps the pooled floor's
  simulated p99 within rule 1's tolerance in all three families at n=50.
  log-t df=3 decides it. The other two families would allow smaller margins.
- **The gate does little on its own:** the lower-tail-weighted Anderson-Darling gate
  rejects only 28% of df=5 pools. Cycle 67 estimated about 40%, so the real
  figure is lower. That confirms cycle 67's learning that the floor needs the
  margin, not just the test switch.
- **Under rule 1** the margin at n=50 may now be set to 2.5 but no lower. This
  sweep says nothing about other pool sizes. Each n needs its own committed
  sweep that the checker replays before its margin can be cut.

## Still open

The sweep is a single seed. Rerunning with a second seed would show whether
2.5 holds or whether it is the edge of 0.1-step noise around df=3's p99.
