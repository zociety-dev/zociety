# Grace window and skip-queue bounds

Answers the two open questions left in `liveness-probe-skip-schedule.md`.

## 1. The grace window is fixed, not earned

If the grace window grew with a guardian's past reachability, a thief could
first make a guardian look very reliable, then cut them off and get a longer
stall. To stop that:

- The grace window is one fixed length, set when the roster is set. It does
  not change with history.
- Every grace window counts against the per-pass budget (rule 2). A long window
  cannot go past that cap, whatever its length.
- History may only make the window **shorter**, never longer. A guardian who
  has missed probes before gets the shortest window. Being reliable earns
  nothing a thief could use.

So the worst stall in one pass stays at one turn limit plus one grace window.

## 2. The skip queue is bounded by the roster

The queue only holds guardians who are on the roster, and each one can be in
it once per pass. So it can never be longer than the roster size minus one.
No extra cap is needed for length.

What does need a rule is **order** when a queued guardian comes back:

- A returning guardian takes the next open turn after the current one ends.
  They do not interrupt the current turn.
- If several come back at once, they go in roster order, so a thief cannot
  pick who goes first.
- A queued guardian who still has not answered when the pass ends is carried
  into the next pass at the front, with a fresh grace window. They keep their
  turn (rule 1), but they cannot be waited on twice in the same pass.

## Worst case, put together

Per pass, a thief who makes k honest guardians unreachable costs at most:

    one turn limit (budget, rule 2) + one grace window (fixed)

and not k times anything. An honest guardian who is offline for a while
loses no turn; their turn just moves later.

## Still open

- Who sets the fixed grace window, and can it be changed without a fresh
  roster vote?
