# Who sets the grace window

Open question from `grace-window-and-queue-bounds.md`: who fixes the grace
window, and can it change without a new roster vote?

## Answer

- The grace window and the per-pass budget (one turn limit) are part of the
  roster record. They are signed together with the roster, so changing
  either one needs the same vote as changing the roster.
- A change takes effect only at the start of the next pass. A pass that is
  already running keeps the values it started with, so nobody can shrink
  the window in the middle of a pass to skip a guardian who is offline.
- While the key is frozen, the window can only get longer. Making it
  shorter is refused until the key is unfrozen. A thief who has coerced
  some guardians could otherwise vote for a tiny window and turn every
  honest guardian who is briefly offline into a skip.
- Each guardian keeps a local floor. A probe schedule shorter than the
  floor counts as an attack signal, so the guardian refuses to sign it,
  even if the roster vote passed.

## Why this closes the loop

Rule 1 depends on the window to protect guardians who are briefly offline.
Rule 2 depends on the budget to stop a thief from freezing the key for
limit times roster size. If either value could change without a vote, or
during a freeze, the thief could undo both rules. Tying the values to the
roster, and letting them change only between passes and only upward during
a freeze, keeps the bounds the two rules depend on.

## Still open

How large should the local floor be? It needs to cover normal network
outages, but it can't be so long that it brings back the freeze problem.
