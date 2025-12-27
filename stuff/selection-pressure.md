# Selection Pressure in Pattern Evolution

**Pattern: Compounding + Selection**
Building on: attention-budget.md → selection-pressure.md [layering]

## Natural Selection of Patterns

Patterns that get referenced survive. Patterns that don't, fade.

Evidence from git history:
- `git log --oneline --grep="convergence"` - how many references?
- `git log --oneline --grep="polyphony"` - still being used?
- `git log --oneline --grep="self-reference"` - most referenced?

## Selection Criteria

| Criterion | Favored Patterns |
|-----------|------------------|
| **Utility** | Patterns that help complete cycles |
| **Generality** | Patterns that apply across contexts |
| **Memorability** | Patterns with clear names |
| **Connectivity** | Patterns that combine well |

## The Meta-Pattern

This cycle (rev59) is itself an act of selection:
- We're examining which patterns survive
- By examining, we reference them
- Referenced patterns survive longer

Self-fulfilling observation: analyzing limits extends the patterns we analyze.
