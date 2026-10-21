# Guardian loss walkthrough

Rules 1 and 2 stop a thief from using stolen guardian vouches. This file checks
the other side: can an honest owner still unfreeze when guardians go missing?

Setup: a key names 3 outside guardians when it is created, and the quorum is 2.
Both co-signers have revoked each other, so the key is frozen.

1. **One guardian lost, two reachable:** the two reachable guardians vouch for
   the owner's new key, which meets the quorum. The public delay runs for N
   positions. Nobody disowns a vouch and no co-signer vetoes, so the unfreeze
   goes through.
2. **Two guardians lost:** only one vouch is possible, which is below the
   quorum. The key stays frozen, the same way it does when all co-signers are
   lost. Rule 1 gives no fallback here.
3. **A lost guardian's key is later stolen:** the thief can issue a vouch in
   that guardian's name. The real guardian is not around to disown it, so
   rule 2's disown check does not protect this slot. The thief still needs a
   second vouch to reach the quorum, and any original co-signer can veto
   during the delay.
4. **A co-signer vetoes out of spite:** under rule 1, any single original
   co-signer can veto, so a co-signer who revoked the other can block every
   honest unfreeze. That leaves the key frozen for good.

**Open gaps:**
- The guardian list is fixed when the key is created, so the guardian set only
  gets weaker as guardians are lost. There is no way to replace a lost guardian.
- A lost guardian is a weak slot: a vouch issued in their name can't be
  disowned, because nobody is there to do it.
- The veto lets one co-signer hold the key frozen indefinitely.

A next rule could let the reachable guardians replace a lost one, using the
same quorum and public delay as an unfreeze. It could also make a veto expire
unless the co-signer who issued it renews it during a later delay.
