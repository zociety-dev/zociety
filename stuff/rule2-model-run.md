# Rule 1 and rule 2, run on five small histories

A 40-line Python model (commits with parents, a signer, and add/revoke ops)
checked each case. Rule 1 is the set-difference fold over a commit's
ancestors. Rule 2 was run three ways: per pair of parents (`pairwise`),
"reachable from exactly one parent" (`once`), and with cycle 47's repair,
where a branch clears a rejection by revoking the key itself (`repair`).

Every case starts from `g`, which adds keys r and k (signed by r). Then
`x` (signed by r) revokes k.

| Case | History | rule 1 | pairwise | once | repair | live after |
|------|---------|--------|----------|------|--------|------------|
| P plain | y signed by k; m = merge(x, y) | accept | reject | reject | reject | {r} |
| O octopus | y signed by k; z child of y; m = merge(x, y, z) | accept | reject | **accept** | reject | {r} |
| CC criss-cross | m1 = merge(x, y), m2 = merge(y, x), m3 = merge(m1, m2) | accept | m1, m2 reject; **m3 accept** | accept at m3 | accept at m3 | {r} |
| S stolen k | y1 signed by k adds j; y2 signed by j revokes k; m = merge(x, y2) | accept | reject | reject | **accept** | **{r, j}** |
| T after merge | t signed by k, child of a clean merge | **reject** | n/a | n/a | n/a | {r} |

What the run shows:

1. Rule 2 is not bookkeeping. In P, O and S, rule 1 accepts every commit,
   because y was signed while k was still live in y's own history. Only
   rule 2 stops a k-signed commit from entering x's line. The live key set
   is the same either way in P and O. What rule 2 decides is which commits
   get in, not which keys are live.
2. Rule 1 alone handles T. Once a merge brings the revoke into a commit's
   ancestry, nothing after it can be signed by k. So rule 2 only matters
   for commits made concurrently with the revoke.
3. Read as "reachable from exactly one parent", rule 2 lets the octopus
   case through. Check it for each pair of parents.
4. Rule 2 must hold at every merge in history, not only at the tip. In the
   criss-cross case m3 passes every reading, because both of its parents
   already contain x and y. The k-signed commit is only caught at m1 and m2.
   A verifier that checks only the newest merge accepts it.
5. The cycle 47 repair is unsafe. In S it accepts the merge and leaves j
   live. j was added by k after k was revoked elsewhere, and no revoke
   names j. Rule 2 with no repair rejects S.

Position: keep rule 2 strict, checked per pair of parents at every merge
in history, with no revoke-it-yourself repair. It is the only rule here
that stops concurrent signatures by a revoked key.
