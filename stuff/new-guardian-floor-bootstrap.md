# Grace floor for a new guardian with no outage history

Rule 1 sets each guardian's grace floor at twice its 30-day p99 ordinary
outage, capped at the per-pass turn limit. A guardian that joined less than
30 days ago has no p99. If it gets the cap by default, it is the cheapest
guardian for a thief to target: cut it off and the key waits a full turn
limit.

## Proposal

1. **Borrow the roster median until there is data.** A new guardian's
   floor is the median of the other guardians' current floors, not the cap.
   This is a value the roster already voted for, and it gives a thief no
   reason to pick the newcomer over anyone else.
2. **Phase in its own number.** After d days of signed probes (d < 30), the
   floor is `(d/30) * own + (1 - d/30) * median`, where `own` is twice the
   p99 over those d days. At day 30 it is the rule 1 value.
3. **Rule 2 applies from day one.** Outages count toward `own` only when
   another roster member confirmed them over a second path. A thief can't
   pad a young guardian's short history with outages it caused.
4. **No changes while frozen.** The blend is frozen with the key, as
   rule 1 already requires of floors.

## Worked numbers

Roster floors: 20, 30, 45 minutes. Median = 30. Turn limit = 120.

| Day | Own p99 x2 | Floor |
|-----|-----------|-------|
| 0   | none       | 30    |
| 10  | 60         | 40    |
| 20  | 60         | 50    |
| 30  | 60         | 60    |

Capping at the turn limit would have given 120 on day 0. The bootstrap
cuts the newcomer's worst-case freeze by 4x, and the guardian still ends
up at its own measured floor.

## Still open

- With a roster of 2 the median is a single guardian's floor, so that one
  guardian sets the newcomer's floor too.
- What a thief gains by getting a guardian onto the roster and then cutting
  it off right away is bounded by the median, not removed.
