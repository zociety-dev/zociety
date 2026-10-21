# Two-key thief trace under rules 1 and 2

Keys: `h` honest, `j` and `k` stolen by one thief, `r` revoked and rescued
in stratum 2 every evaluation. `r` countersigned cut `c_r`: "h is in good
standing". Any cut "deny h" contradicts `c_r`. No unrevoked key has a cut
that contradicts a "deny h" cut, so only `r` can refute one.

## Spaced forgeries: one stolen key per evaluation

| Eval | Thief submits | Stratum 1 | Stratum 2 | Stratum 3 | `h` |
|------|---------------|-----------|-----------|-----------|-----|
| 1 | `f1` "deny h", by `j` | `f1` counted (`j` has standing, nothing unrevoked contradicts) | `r` rescued | `c_r` refutes `f1` | denied |
| 2 | `f2` "deny h", by `k` | `f1` refuted (carried), `j` loses standing; `f2` counted | `r` rescued | `c_r` refutes `f2` | denied |
| 3 | `f3` "deny h", by `j` | `f2` refuted (carried), `k` loses standing; `f3` checked against `c_r`, refuted | `r` rescued | - | good |
| 4+ | any cut by `j` or `k` | refuted in stratum 1 | `r` rescued | - | good |

Submitting `f1` and `f2` in the same evaluation costs both keys their
standing at once: one evaluation of denial. Spacing them is the thief's
best play, and it buys two. So n stolen keys buy at most n evaluations of
denial, not indefinite denial. Rule 2 answers the first half of the
direction.

## The gap: which rescued set does stratum 1 read?

Rule 2 has stratum 1 check a lost-standing key's cuts against rescued
keys' cuts, but rescue is computed in stratum 2, after stratum 1. If
stratum 1 reads this evaluation's rescued set, stratum 1 depends on stratum
2 through a negation ("counted unless a rescued key contradicts it") while
stratum 2 depends on stratum 1. The stratification is gone.

Counterexample: `j` has lost standing and countersigns `g`: "r's rescue cut
is void". `c_r` contradicts `g`.

- `r` rescued, so `g` is refuted, so `r`'s rescue stands. Consistent.
- `r` not rescued, so `g` counts, so `r`'s rescue is void. Consistent.

Two stable models; the well-founded model leaves `r` and `g` undefined.
That is the negation back, as a choice rather than an oscillation.

## Fix

Stratum 1 of evaluation t reads `R(t-1)`, the rescued set of the previous
evaluation, as an input. It is fixed before evaluation t starts, so
stratum 1 stays monotone in its inputs and the three strata stay ordered.
In the counterexample `g` is refuted in evaluation t if `r` was rescued in
t-1, and counted otherwise; either way there is one model.

Cost: a key rescued for the first time in evaluation t protects against
lost-standing keys from evaluation t+1 on, one evaluation of lag. Because
refutations accumulate, a cut refuted against a key that later stops being
rescued stays refuted. That over-refutes only keys already caught signing a
forgery, which is the safe direction.
