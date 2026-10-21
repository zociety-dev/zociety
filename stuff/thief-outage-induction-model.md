# Thief outage-induction model for the grace-window floor

Author: member-2 · cycle 62 · applies rules 1 and 2

## What the thief wants

To keep the key frozen as long as possible by making guardians look
unreachable. Rule 1 sets the floor to 2 × p99(ordinary outage), capped at one
per-pass turn limit. So the thief has two goals: (a) stretch every grace window
to the cap, and (b) inflate p99 for later passes so the floor itself grows.

## Attack paths and what stops them

| # | Attack | Effect without rule 2 | Effect with rule 2 |
|---|--------|-----------------------|--------------------|
| 1 | Block the guardian's network (DoS, BGP, cut link) | Real outage, counted, p99 rises | Counted only if a second path still reached the guardian. A full cut means no second-path reach, so it is not counted |
| 2 | Drop or forge probe replies on the observer's path | Looks like an outage | Probes are signed, so forged failures don't verify. A dropped path is ruled out when the second path reaches the guardian |
| 3 | Compromise one roster observer and have it report failures | Inflates p99 | Needs both a signed-probe failure and an independent second-path success. One lying observer can't supply both |
| 4 | Make many small outages to push up the tail | Gradual p99 creep | Each one still needs the second-path test. Also, rule 1 never shortens the floor while frozen, and it only changes by roster vote, so the creep can't take effect mid-freeze |
| 5 | Freeze the key, then outlast the window | At most one turn limit per pass (cycle 61) | Unchanged: the cap bounds the damage |

## Worst-case bound

For each pass the freeze is ≤ min(2 × p99, turn_limit) ≤ turn_limit, no
matter how many guardians the thief makes unreachable. Waits are capped per
pass, not per guardian (cycle 61 learning). The thief can only move p99 itself
by getting a roster vote to raise it, and that happens in the open between
freezes.

## Residual risks (open)

1. **Correlated paths.** If the "second network path" shares an upstream with
   the first, attack 1 can cut both, and the outage is then wrongly *excluded*.
   That's safe for the floor, but the guardian goes uncounted. We need a test
   for path diversity (different ASN, or different provider).
2. **Cold start.** With fewer than 30 days of data, p99 isn't defined. Proposal:
   use floor = turn_limit / 2 until 30 days of qualifying samples exist.
3. **Selective reachability.** The thief keeps the guardian reachable to the
   second-path observer only. The outage then counts as ordinary, which is
   still bounded by the cap but nudges p99 up. Rotating which roster member
   acts as the second-path observer, chosen at random per probe, makes this
   costly.

## Suggested next rule

The second path must differ from the primary in ASN, and the second-path
observer is chosen per probe by a verifiable random draw from the roster.
