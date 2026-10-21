# Co-signer floor with vouched replenishment: a worked trace

Applies rule 1 (floor + vouched replenishment) and rule 2 (renewal by a distinct guardian).

## Setup

- Unfreeze needs 2 of 3 co-signers: A (honest), B (honest), T (stolen by the thief).
- Guardians: G1, G2, G3.
- The thief rotates the key; A contests. Both replacement keys draw zero guardian vouches.

## Trace

1. **Tie at zero vouches.** Both A and T are revoked. Only B remains, and unfreezing needs 2.
2. **Floor holds (rule 1).** With 1 left, below the floor of 2, the key stays frozen. Revoking A and T does not hand the key back to the old set, so the thief has nothing to restart.
3. **Replenishment (rule 1).** Seat candidates C and T' (the thief's new identity) apply.
   - G2 vouches for C, so C is seated.
   - T' gets no vouch and is refused. The floor never seats anyone with zero vouches.
4. **Unfreeze.** B and C sign, and the key is released to the vouched replacement key.
5. **Renewal (rule 2).** Suppose G1 vouched for the key that was revoked. Then C's seat lapses unless G2 or G3 renews C's vouch. If one guardian was coerced, the thief still can't keep a seat alive alone.

## What the thief can still do

- **Coerce two distinct guardians.** That costs two compromises, compared with zero before rule 1.
- **Stall.** While the set is below the floor, the key stays frozen, so the thief can deny service but cannot spend.

## Open question

Should a seat that lapses under rule 2 reopen replenishment immediately, or wait a cooldown? Without a cooldown, a thief holding one guardian can churn seats.
