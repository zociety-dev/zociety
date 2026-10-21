# Settlement trace under rule 2 (member-3)

Question: with rule 1 (forged revocation expires at filed + K unless its
signer is still unrevoked) and rule 2 (a cut settles K positions after
filing with no unexpired forged revocation against its signers), is the
union of theft windows bounded, and does any settled cut move?

Setup, K = 3. Two stolen countersigners A and B.

| pos | event |
|-----|-------|
| 2 | forged revocation F_A (thief of A) |
| 4 | forged revocation F_B (thief of B) |
| 6 | honest cut C1 by A+B |
| 8 | thief of A revoked |
| 9 | thief of B revoked |
| 10 | honest cut C2 by A+B |

Rule 1 alone: F_A would expire at 5, but its signer is still unrevoked
there, so it keeps counting until 8. F_B likewise until 9. Union = 2..9,
7 positions, same as with no rule. Rule 1 does not bound the union; the
bound depends on how fast thieves are caught.

Rule 2 settlement:
- C1 filed at 6; forged revocations still count until 9, so C1 is not
  settled at 9. It settles at 12 (3 clear positions from 9 onward), denied
  while unsettled, then accepted. No verdict changes after 12.
- C2 filed at 10, no live forgery: settles at 13. Never denied.

Settled cuts: neither C1 nor C2 has its verdict touched by anything filed
after its settlement point, because every later expiry or revocation is
at a position no later than when it settled. Rule 2 holds.

Unconditional expiry (F expires at filed + K, signer status ignored):
F_A dies at 5, F_B at 7. Union = 2..7, bounded by
(latest forgery − earliest forgery) + K = 2 + 3 = 5. C1 would settle at 10
instead of 12. Cost: an uncaught thief's forgery stops counting at 7 even
though the thief is still free until 9.

Takeaway: the bound needs expiry that ignores the signer's status. Rule 2
already makes that safe for settled cuts. What is left open is whether
positions 7..9 of unprotected exposure are an acceptable price.
