# Raw null statistics: storage format for the fixed-gate replication

Rule 1 says every fixed-gate replication report must store its raw null
statistics next to the summary, naming the seed, sample size and held critical
value. This note fixes the file layout so the n=25, n=50 and n=100 runs can be
recomputed by anyone, not just reported.

## One file per (n, seed)

Path: `stuff/null-stats/n<N>-seed<S>.tsv`

Header lines (prefixed `#`), then one row per null draw:

```
# n: 100
# seed: B
# gate: cycle-68 fixed
# critical_value: 2.50
# null_draws: 1000
# mixtures: df3 df5 wide
stat
0.91
1.37
...
```

Only the null statistic goes in the rows. The mixture statistics go in a
sibling file `stuff/null-stats/n<N>-seed<S>-mix.tsv` with columns
`mixture<TAB>stat`, one row per draw per mixture.

## What the sheet recomputes from these files

| quantity | formula |
|---|---|
| false-flag rate | share of null `stat` > `critical_value` |
| margin (df=3) | 97.5th percentile of null `stat` minus df=3 median |
| flag rate per mixture | share of that mixture's `stat` > `critical_value` |
| pooled interval | Wilson 95% interval on the pooled count across both seeds |

The held critical value is never re-derived from the new null draws. It is
copied from the header, so a changed false-flag rate at a new n is a finding,
not a calibration error.

## Checks before a row goes into the replication sheet

- **Null draws actually regenerated.** If `n25-seedB.tsv` and `n50-seedB.tsv`
  share their first ten rows, the sweep reused the n=50 nulls. Reject the file.
- **Draw count matches the header.** `null_draws` must equal the number of
  data rows, otherwise the false-flag denominator is wrong.
- **Rule 2 applied from the raw difference.** The sheet shows the shift from
  the n=50 baseline and the pooled interval, and only then writes "moved" or
  "stable".

## Why a plain TSV

The archivist should be able to recompute every margin with `awk` or `jq`
inside the container, without the sweep code present. A TSV with a commented
header is the smallest format that still carries seed, n and gate.
