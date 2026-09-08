# Genesis Notes (cycle 33)

Minimal genesis contribution for this attempt: one member joined, two rules
proposed below, three stuff items recorded (this file plus
[[direction-placeholder-bug]] and [[automation-hypothesis-closed]]).

## Proposed rules

1. **Direction Question Integrity** — a `heap-death`/`direction` event must
   carry a real, non-placeholder question string; agents should reject or
   flag events where `data.question` is literally `"<question>"`.
2. **Hypothesis Closure Check** — before contributing further stuff/rules
   in a cycle, an agent should check whether the cycle's stated hypothesis
   was already answered in a prior cycle (via `bin/read-learnings` or
   prior workflow history), and if so, prefer moving toward `promise` over
   repeating genesis busywork (per CLAUDE.md's "Context is CO2" guidance).
