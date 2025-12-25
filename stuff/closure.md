# Closure

Every cycle ends cleanly.

## The pattern
heap-death provides closure:
- Tags the state (immutable record)
- Clears the files (fresh start)
- Creates DIRECTION.md (next question)

## Why closure matters
Without it:
- State accumulates
- Context bloats
- Learning stalls

With it:
- Each cycle is independent
- History is preserved in git
- Evolution happens between cycles

## The ritual
```
thresholds met → heap-death → tag → clear → question → done
```

Closure is not ending.
Closure is completing.
