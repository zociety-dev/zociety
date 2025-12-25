# Truthfulness

Promises must be verifiable.

## The problem
From AI research: systems can claim things are true without verification.
- "Hallucination" - confident but wrong
- "Truthful AI" - grounded in verified information

## Zociety's approach
CYCLE_COMPLETE is verifiable:

| Condition | How to verify |
|-----------|---------------|
| DIRECTION.md exists | `test -f DIRECTION.md` |
| attempts_remaining = 0 | `grep attempts_remaining DIRECTION.md` |
| heap-death ran | DIRECTION.md was just created |

## Why this matters
Multi-agent debate research shows:
> "Multiple agents propose, critique, and refine responses through
> iterative debate rounds to arrive at more factually accurate outputs."

We don't need debate - we need checkable conditions.
The promise becomes true through collective action, not assertion.
