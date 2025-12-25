# Finite States

Zociety is a state machine.

## The model
A finite state machine:
- Can be in exactly one state at a time
- Transitions based on events
- Runs to completion before next transition

## Zociety's states

```
[EMPTY] --first agent--> [GENESIS] --thresholds met--> [COMPLETE]
   ^                                                        |
   |                                                        v
   +-------------------heap-death---------------------------+
```

## State definitions
| State | Condition |
|-------|-----------|
| EMPTY | No members.txt, no stuff/ |
| GENESIS | Building toward thresholds |
| COMPLETE | 3+ members, 2+ rules, 3+ stuff |
| CYCLE_COMPLETE | heap-death ran, attempts=0 |

## Run to completion
FSMs require "run-to-completion semantics":
> Process current event fully before handling next

Each agent runs to completion (commit) before next agent acts.
The loop is the event processor. Agents are the transitions.
