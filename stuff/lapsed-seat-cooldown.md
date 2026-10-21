# Lapsed-seat cooldown

Follows `cosigner-floor-replenishment.md`, which ended asking whether a seat
that lapses under rule 2 should wait out a cooldown before it can be refilled.

## The cycling attack

Rule 1 refills a drained co-signer set only with guardian-vouched newcomers.
Rule 2 makes such a seat lapse unless a *different* guardian renews the vouch.
A thief who coerces one guardian can still:

1. get a fresh identity vouched into the open seat,
2. let it lapse when no second guardian renews,
3. coerce the same guardian again for another fresh identity, and repeat.

Each round the key stays frozen (good), but the honest holder cannot finish an
unfreeze either, because the seat is always occupied by a thief-placed holder
that is waiting for a renewal that will never come.

## Proposal: per-guardian cooldown, not per-seat

A cooldown on the *seat* also slows the honest refill. A cooldown on the
*guardian* whose vouch let a lapsed seat in targets the attack directly:

- When a seat lapses, the guardian who vouched it in may not vouch another
  refill for that key until the cooldown ends.
- Any other guardian may vouch a refill immediately.

The thief now needs a newly coerced guardian for every round, so the cost of
stalling grows with each lapse instead of staying flat.

## Traversal

- Honest holder, two cooperative guardians: refill and renewal happen in the
  same window; no seat lapses; the cooldown never fires.
- Thief with one coerced guardian: one stalled round, then that guardian is
  benched and an honest guardian's vouch fills the seat.
- Thief with two coerced guardians: rule 2 is already beaten; the cooldown
  does not help. This is the residual risk and sets the guardian count floor.

## Open question

How long should the bench last? Too short and a single coerced guardian keeps
cycling; too long and an honest guardian who vouched in good faith for a holder
who simply went offline is shut out when the key needs them most.
