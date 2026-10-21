# Grace-window floor: a worked example under rules 1 and 2

Rule 1: floor = 2 × (30-day p99 ordinary outage), capped at the per-pass turn limit,
set by roster vote, never shortened while frozen.
Rule 2: an outage counts toward the p99 input only if the guardian's signed probes
failed AND another roster member reached that guardian over a second network path.

## Inputs (illustrative roster of 5 guardians, turn limit 24h)

| guardian | counted outages (30d, rule 2) | p99 duration | 2 × p99 | floor (capped) |
|----------|-------------------------------|--------------|---------|----------------|
| g1 home fibre   | 6  | 40 min | 80 min | 80 min |
| g2 mobile only  | 31 | 5 h    | 10 h   | 10 h   |
| g3 datacentre   | 1  | 4 min  | 8 min  | 8 min  |
| g4 travelling   | 12 | 14 h   | 28 h   | 24 h (cap) |
| g5 new, no data | 0  | —      | —      | default: cap (24h) until 30 days of data |

## What the thief gets

- Freeze per pass is still bounded by one turn limit (cycle 61 learning), so the
  floors only decide *who* is queued vs. skipped, not total freeze length.
- To keep g3 queued instead of skipped, the thief must hold it unreachable for
  only 8 min — but rule 2 means an induced outage that a second path sees through
  does not raise g3's p99, so the thief cannot inflate the floor by attacking g3.
- An outage the thief makes total (both paths dead) is excluded from the p99 input
  only if a second path *reached* the guardian; a total blackout is not counted,
  so it cannot ratchet the floor up either. The floor can only rise from outages
  the guardian really had while still reachable some other way.

## Open edges

1. g5 (no data) defaulting to the cap is the safe choice for the owner but gives
   a thief a full-limit queue slot; a newly added guardian is therefore the
   cheapest one to target. Possible fix: new guardians do not count toward the
   threshold until they have 30 days of data.
2. g4 hits the cap, so for it the floor equals the whole pass budget — one
   travelling guardian can consume a pass. Rule 1's cap bounds this but does not
   stop it; the roster may want to vote such guardians out of the "queue" role.
3. The "second path" witness is itself a roster member; a thief holding one
   guardian could refuse to witness. Requiring any one of the other N−1 members to
   witness (not a fixed one) limits that to a thief holding all of them.
