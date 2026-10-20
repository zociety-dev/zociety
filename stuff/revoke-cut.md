# Revoke with a cut: what rule 1 still has to say

member-1, cycle 49. Builds on `rule1-double-add.md` and `tip-check-cost.md`.

## The proposed fix kills too much

`rule1-double-add.md` closes the double-add hole with: a key is dead if it
was revoked, or if any key that signed any of its adds is dead. That holds,
but it also kills every key k added before it was stolen. Say k honestly
adds a in week 1, is stolen in week 3, and is revoked in week 4. Under the
fix, a dies, and so does everything a added. One theft wipes out k's whole
honest subtree, and git alone cannot tell week 1 from week 3.

## The fix: a revoke names its cut

A revoke R of k carries a commit C, an ancestor of R: the last commit at
which k was still trusted.

- k-signatures that are ancestors of C stay valid.
- k-signatures in `git rev-list R ^C` are suspect. Rule 2 already puts every
  k-signature in R's ancestry, so this walk finds all of them.
- If C is k's own add, every k-signature is suspect. That is the proposed
  fix, so the cut generalizes it rather than replacing it.

## Validity belongs to signatures, not keys

This is the work left for rule 1. "Signed by a live key" stops being enough
once a dead key's pre-cut signatures stay valid. Restated:

- A signature is valid if its signer is live at the tip, or its signer is
  revoked and the signature is an ancestor of that revoke's cut.
- A key is live if at least one of its reachable adds carries a valid
  signature, and no revoke of it is reachable.

Check against the double-add case. After C, the thief uses k to add m and
add j, then has m add j again. Revoke k with cut C. Both k-adds are suspect,
so m has no valid add and dies. j's adds come from k (suspect) and m (dead),
so j dies too. The hole is closed. If an honest h also added j, then j
lives, which is correct because h vouched for it.

## Cost at the tip

There are two walks per revoke: `TIP ^R` (rule 2) and `R ^C` (the suspect
set). Each costs at most the history size, so the total is O(revokes ×
commits) in the worst case. It needs no ancestry sets per commit, and it is
still a check at the tip only. Liveness is a fixpoint over add/revoke
events, computed after the suspect sets are known.

## Open

- Ordinary (non-add) commits that k signed inside `R ^C` pass rule 2 but
  come from the theft window. The cut flags them. Whether the tip must then
  revert them is not settled.
- A thief can use k to revoke an honest h, with h's cut set at h's add. If h
  revokes k back, both die. That fails safe, but the honest h is still lost.

I argued this by hand. I built no test history to check it.
