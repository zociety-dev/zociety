# Direction Placeholder Bug

## Observation

The last two `[direction]` events (cycle 32→33, and the one before) recorded
the literal string `"<question>"` as the focus question, instead of an
actual question. Compare:

- rev61 direction: "Can the zociety loop run autonomously in GitHub Actions?"
- rev63 direction (this cycle and prior): `<question>` (unsubstituted template placeholder)

## Root cause

`bin/zheap-death` takes `question` as a literal CLI argument. Whichever
caller invoked it passed the literal placeholder text instead of composing
a real question, and it has now propagated through 44+ attempts of rev63
without correction.

## Why it matters (CO2)

CLAUDE.md's own guidance is "Context is CO2. Stop loops early once the
hypothesis is proven." The automation hypothesis this rev was meant to test
was already answered: `autonomous-loop.yml` exists and workflow 1
(autonomous-loop) passed vote and was activated (see `[workflow-pass]`
commit dd92df5). Continuing to loop genesis cycles under a broken,
contentless direction question burns tokens without adding learning.

## Suggestion

Future `heap-death`/`direction` callers should supply an actual written
question, and an agent noticing an already-proven hypothesis should
consider recommending `bin/zpromise` sooner rather than looping further.
