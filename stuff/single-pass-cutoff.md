# Single-pass cutoff: rules 1 and 2 resolve in one walk of the log

Question: if rescue restores only cuts a key signed before its revocation by
commit-log position, does each stratum stay monotone and two-valued, and can a
forged revocation move that cutoff earlier?

## The dependency looks circular but isn't

Rule 1 sets a key's cutoff at its first *countersigned* revocation. Rule 2
says a countersignature counts only if the countersigning key has no counted
countersigned revocation *earlier in commit-log order*. So whether K's
revocation counts depends on whether J's revocation counted, which depends on
J's countersigner, and so on.

Every link in that chain points strictly backward in the log. That makes the
dependency well-founded. One forward walk resolves it:

1. Walk events in commit-log order, keeping `cutoff[key]` (unset at the start).
2. For a revocation of K countersigned by J (J ≠ K): it counts iff
   `cutoff[J]` is still unset at this position. If it counts and `cutoff[K]` is
   unset, set `cutoff[K]` to this position.
3. Uncountersigned revocations are recorded and change nothing (rule 1).
4. Once set, `cutoff[K]` is never touched again.

## Consequences

- **Two-valued and monotone per key:** a cut by K is restored iff its position
  is before `cutoff[K]`. Every cut falls on one side or the other, and the
  restored set is a prefix of K's cuts.
- **Stable:** a later event cannot move an earlier cutoff. Step 4 never
  rewrites, and step 2 only reads state from earlier positions. This is the
  property the retroactive-voiding fix in `countersigner-race.md` would give up.
- **Forgery can still move the cutoff earlier,** but only if the forgery lands
  while its countersigner J is still uncut. Once J has a counted revocation, J
  cannot countersign anything again. So each stolen-and-unrevoked key can
  countersign forgeries for others. It can only do that until its own
  revocation counts.

## Example

| pos | event                        | counts? | cutoff after          |
|-----|------------------------------|---------|-----------------------|
| 1   | A cuts x                     | —       | —                     |
| 2   | revoke B, countersigned by A | yes     | B=2                   |
| 3   | revoke A, countersigned by B | no (B cut at 2) | B=2           |
| 4   | revoke A, countersigned by C | yes     | A=4, B=2              |

A thief holding B forges A's revocation at 3 and gets nothing, because B was
already cut at 2. Their window was before position 2. This matches the race
described in `countersigner-race.md`, and the walk shows that race is the only
remaining attack.
