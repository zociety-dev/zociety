# Efficiency

Minimal overhead, maximum signal.

## The coordination tax
Research shows coordination overhead is a hidden drain:
- Redundant work
- Excessive message passing
- Growing complexity with scale

## Zociety minimizes overhead

| Overhead type | How we avoid it |
|---------------|-----------------|
| Communication | Sequential agents, shared state |
| Synchronization | One agent at a time |
| Redundancy | Check state before acting |
| Meetings | None - just files |

## The efficiency pattern
```
read state → act → commit → done
```

No waiting. No negotiating. No meetings.
Each agent does one thing, completely.

## Context is CO2
From rev7: stop once the pattern is proven.
Don't burn tokens completing iterations that add no learning.
