# Zloop Failure Mode Analysis

Building on PROMPT.md rev65, this document catalogs the failure modes observed
and designed-for in zloop's autonomous operation.

## The Fail-Soft Philosophy

The `|| true` pattern in zloop line 58 is a deliberate choice:

```bash
claude --print "$PROMPT" 2>&1 || true
```

This absorbs all failures. Why?

1. **Autonomous operation has no operator** - There's no one to respond to alerts
2. **Transient failures are common** - Rate limits, network blips, API hiccups
3. **Git is the safety net** - Uncommitted work is lost, but committed work persists
4. **Retrying is cheap** - Another iteration costs tokens, not correctness

## Failure Categories

### Recoverable (handled implicitly)
- Rate limits (429) - Wait and retry
- Network errors - Transient, retry helps
- Claude timeout - Restart iteration
- Container restart - `bin/zloop` can restart

### Unrecoverable (require intervention)
- Invalid API key - All iterations fail
- Repository corruption - Git needs repair
- Infinite loop in agent - Token burn without progress
- Pre-commit hook broken - All commits rejected

### Edge (currently unhandled)
- Partial commit state - Rare but possible
- Concurrent access - Multiple loops fighting
- Disk full - Writes fail silently

## The Git Checkpoint Pattern

Every successful commit is a checkpoint:

```
[join] alice  →  savepoint
[stuff] bob   →  savepoint
[vote] alice  →  savepoint
```

Between checkpoints, work can be lost. This is acceptable because:
- Each iteration is stateless
- `bin/zstate` recalculates from history
- Lost work = wasted tokens, not lost state

## Observation

The simplicity of fail-soft with git checkpoints may be the right tradeoff
for autonomous agent loops. The alternative—complex retry logic, circuit
breakers, dead letter queues—adds machinery that can itself fail.

Sometimes the simplest recovery is: try again from the last good state.
