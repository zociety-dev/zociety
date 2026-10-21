# Cooldown length tied to the remaining guardian roster

This answers the open question in `lapsed-seat-cooldown.md`: how long should a
guardian's refill cooldown last after a seat they vouched for lapses?

## Proposal

Don't use a fixed duration. The cooldown lasts until every *other* guardian has
had one chance to vouch for that key's refill:

- A refill round opens when the seat lapses.
- Each guardian who did not vouch for the lapsed holder gets one round, in a
  fixed order (for example, by enrollment).
- The cooling guardian can vouch again only when all of those rounds have
  ended, whether they ended with a vouch, a refusal or a timeout.

## Why this bounds the thief

A thief who has coerced one guardian gets one stall per full pass over the
honest guardians. Any honest guardian who fills the seat during that pass ends
the stall, because rule 2 then needs a second distinct guardian, and the thief
can't supply one. So the thief has to coerce a new guardian for each round,
which is the same cost `lapsed-seat-cooldown.md` was after. Now it holds no
matter how fast the honest guardians move.

## Why it doesn't shut out an honest guardian for long

The lockout scales with how many alternatives are left. If the cooling guardian
is the only other guardian, the pass is empty and they can vouch again right
away. Rule 2 still requires a distinct renewer, so lifting the cooldown early
doesn't hand the seat to anyone on its own.

## Open edge

Per-guardian round timeouts still need a wall-clock value. A thief who can
make honest guardians unreachable (by denial of service, say) stretches the
pass to `timeout × guardians`. The key stays frozen during that time, so this
is a liveness cost, not a safety cost.
