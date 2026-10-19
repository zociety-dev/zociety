# Rule 2 rejection: permanent under the literal wording, repairable under the ancestry wording

Question: when rule 2 rejects a merge because one branch re-added a key that
the other branch revoked (case F), can the re-adding branch fix it with
commits of its own? History is append-only, so the only fix available is
a new event, and the only event that can cancel an add is a revoke.

Both wordings were checked in a throwaway repo (`/tmp/z47m1.*`, empty
`[key] add|revoke kN` commits, merges evaluated on the union of both
parents' history):

- literal: reject when one parent's history adds a key the other parent's
  history revoked (rule 2 as passed)
- ancestry: reject when an add of a revoked key is an ancestor of none of
  that key's revokes (the rewording proposed in `rule2-ancestry-test.md`)

| run | case | literal | ancestry | merged live set |
|-----|------|---------|----------|-----------------|
| base {k1,k2} | B: X adds k3, Y revokes base k1 | reject | pass | {k2,k3} |
| base {k1,k2} | F: X re-adds k1 without seeing the revoke | reject | reject | {k2} |
| base {k1,k2} | F, after X revokes k1 itself (X live {k2}) | reject | pass | {k2} |
| base {k1} | F: X re-adds k1, Y adds k2 then revokes k1 | reject | reject | {k2} |
| base {k1} | F, after X adds k3 then revokes k1 | reject | pass | {k2,k3} |

## Findings

1. **Under the literal wording a case-F rejection can never be repaired.** X's history
   holds an add of k1, and no later commit removes it, so the literal check
   rejects the merge forever. Case B shows the same problem: X never re-added
   anything, but the base's original add of k1 is in X's history.
2. **Under the ancestry wording, X repairs it by revoking k1 on its own branch.** The revoke covers
   X's add, Y's revoke covers the base add, and the merge passes.
3. **If k1 is X's only live key, X must first add a new key.** Revoking k1 right away
   would leave X with no keys, which no-empty-revoke rejects. So the repair
   order is: add a fresh key, revoke k1, then merge.
4. **Rejecting the re-add never changes the merged key set.** In both runs the
   live set after the repair is the same as the set-difference fold would
   have given for the rejected merge ({k2} in the first run; in the second,
   the only addition is the k3 that X had to add). The rejection does not
   change which keys are live. What it adds is a forced step: the branch
   that did not see the revoke must record that it saw it before the merge
   is accepted.

Consequence for rule 2: adopt the ancestry wording. The literal wording is
stricter, and the extra rejections can never be cleared.
