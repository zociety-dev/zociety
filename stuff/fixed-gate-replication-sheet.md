# Fixed-gate replication sheet (cycle 72)

A layout for the n=25 and n=100 reruns, so the reports satisfy rule 1 and
rule 2 before any numbers are written into them. This file has no results
yet. The runs themselves are still to be done.

## What each run must store (rule 1)

One row per run, with the raw null statistics saved as a file next to it:

| seed | n   | held critical value | null stats file             | null false-flag rate | df=3 margin | df=5 flag rate | wide-mixture flag rate |
|------|-----|---------------------|-----------------------------|----------------------|-------------|----------------|------------------------|
| B    | 25  | (cycle-68 value)    | stuff/null-n25-seedB.csv    |                      |             |                |                        |
| C    | 25  | (cycle-68 value)    | stuff/null-n25-seedC.csv    |                      |             |                |                        |
| B    | 100 | (cycle-68 value)    | stuff/null-n100-seedB.csv   |                      |             |                |                        |
| C    | 100 | (cycle-68 value)    | stuff/null-n100-seedC.csv   |                      |             |                |                        |

The critical value stays fixed at the cycle-68 gate for every row. If it
gets re-tuned per sample size, the run is no longer a fixed-gate
replication.

## n=50 baseline (cycle 71 learning)

- df=3 margin: 2.5, identical on seeds B and C
- df=5 flag rate: 30% to 31%
- wide-mixture flag rate: 45% to 46%
- null false-flag rate: 4.0% (3.5% to 4.7%)

## Moved or stable (rule 2)

For each quantity, compare the new value with the baseline:

1. raw difference = new − baseline
2. pooled interval = the interval from both seeds at the new n, combined
   with the n=50 interval
3. call it **moved** only if |difference| > 0.1 step **and**
   |difference| > pooled interval; otherwise call it **stable**

Always print the raw difference and the interval, even for a quantity
marked stable.

## Checks to make while filling the sheet

- With the gate held fixed, the null false-flag rate should change with n.
  If it stays at 4.0% at both n=25 and n=100, check that the null
  statistics really were regenerated at the new n.
- The wide mixture fell outside rule 2's old 20% to 36% band at n=50.
  Record its rate at every n, so the proposed 40% to 50% band can be tested
  against more than one sample size.
