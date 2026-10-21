# Veto cost walkthrough (cycle 59)

How rules 1 and 2 price a veto during the unfreeze delay, checked from
the side of whoever holds the stolen co-signer.

## The two paths to block an unfreeze

1. **Guardian-co-signed veto (rule 1).** A veto counts only if a guardian
   co-signs it for the specific unfreeze it blocks. The thief holds a
   co-signer key, not a guardian, so a bare veto from the stolen key is
   ignored. If no guardian answers before the delay ends, the unfreeze
   proceeds.
2. **Competing replacement key (rule 2).** An honest co-signer who cannot
   reach a guardian posts a competing replacement key before the delay
   ends. The unfreeze goes to whichever key has more distinct guardian
   vouches bound to it.

## Thief's options, one by one

| Thief move | Outcome |
|---|---|
| Veto with the stolen co-signer alone | Does not count (no guardian co-signature). |
| Veto with a stolen guardian vouch | Vouches are bound to one replacement key (cycle 58), so a stolen vouch cannot co-sign a veto against a different unfreeze. |
| Post own competing key | Wins only with more distinct guardian vouches than the honest key. |
| Stay silent, wait out guardians | Rule 1 timeout lets the honest unfreeze proceed. |

## Honest owner's options when guardians are unreachable

- Rule 1 alone would leave them unable to veto a thief's unfreeze.
- Rule 2 gives a path that needs no live guardian response during the
  delay: post a competing key. Vouches already bound to it count.

## Open gap

If neither key has any guardian vouches (a tie at zero), rule 2 does not
say who wins. A tie-break is needed: for example, keep the key frozen,
or favour the unfreeze that was posted first. Freezing on a zero-zero tie
reopens the permanent-freeze problem from cycle 58, so the next rule
should prefer a tie-break the thief cannot win by posting early.
