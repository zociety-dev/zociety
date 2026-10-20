# Witness chain: can a revoke carry its co-signer's key chain?

This answers the question countersign-loop.md left for the next cycle:
should a revoke of k list its co-signer j's key chain, so a verifier does
not have to walk the key tree? It can, but only under one reading of the
countersign rule. Under the other reading the listed chain proves nothing,
and the rule can be attacked as well.

## Two readings of "nothing in j's chain was added by k"

- **Every chain is clean (for all):** no path from a root key to j, in any
  add event, passes through k.
- **Some chain is clean (exists):** at least one path from a root key to j
  avoids k, and each link on that path is the first add of its key on its
  line: no add of that same key signed by k is an ancestor of the link's
  add commit.

## The "for all" reading cannot be witnessed and can be attacked

A listed chain proves that one clean path exists. It cannot prove that no
k path exists. Cycle 49's double-add has exactly that shape: k adds m and j,
m adds j. A revoker who lists only some honest path to j hides the k path.
So under "for all" the verifier has to search the add DAG anyway, and the
listed chain saves nothing.

The reading is also unsafe. A commit's ancestry limits what it can see, not
when it was made. The thief can fork from a commit older than an honest
key h's add, sign "k adds h" on that fork, and merge it. Now h has a path
through k. If the thief does this for every honest key, then:

1. No key can co-sign a revoke of k, so k cannot be revoked.
2. A revoke that was already filed loses its co-signer when validity is
   rechecked at the tip (rule 2's tip check), so it is voided after the fact.

## The "exists + first add" reading works with a witness

The revoke event lists the path `[(root, -), (k1, add1), ..., (j, addj)]`.
For each link the verifier checks four things:

1. `add_i` is an ancestor of the countersign commit.
2. `add_i` is signed by `k_{i-1}` and adds `k_i`.
3. No `k_i` on the path is k.
4. No add of `k_i` signed by k is an ancestor of `add_i`. A k-add that is
   incomparable with `add_i` does not count.

Check 4 is what stops the fork-and-merge attack. The thief cannot put a
commit into the ancestry of an honest add that already exists, so merging a
later fork cannot spoil the witness. The thief's own new keys still fail:
the only adds of such a key are signed by k or by keys k added, so no clean
path to it exists. The double-add also still fails: m's only adder is k,
and every path to j goes through k or m.

The check does not depend on the cut either. It never reads C, so a thief
who places C late gains nothing, which keeps the property
countersign-loop.md depends on.

## Cost

There is no key-tree search. The verifier makes one ancestry test per link
for check 1, and for check 4 one `merge-base --is-ancestor` test for each
add of `k_i` that k signed. Adds are rare and can be indexed by key, so the
cost is O(depth x k-adds per key) ancestry tests. That does not grow with
the number of commits.

## What remains

- **Pre-emption:** if a new key's public half is known before anyone
  honest adds it, the thief can have k add it first. The honest add then
  changes nothing (first add wins) and the key is tainted. This affects
  only keys not yet added, and the add is visible to everyone because it is
  signed by k.
- **Honest keys k added before the theft** still cannot co-sign k's revoke.
  That is countersign-loop.md's accepted cost, and this design leaves it
  unchanged.
