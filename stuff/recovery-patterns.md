# Recovery Patterns in Git-Native Systems

Extending failure-modes.md, this document examines how git-native design
enables recovery without explicit recovery code.

## The Checkpoint-Replay Pattern

Traditional systems: checkpoint → failure → rollback → replay
Git-native systems: commit → failure → restart → state derived

The difference: no explicit rollback. State is always derived from history.

```
git log --oneline
7844a80 [stuff] opus: added failure-modes.md  ← last good state
29870cb [join] opus: joining cycle
6f63cc8 [evolve] system: rev65 - Zloop Edge Cases

# After any failure, bin/zstate reads this history
# and determines: action=contribute
```

## Why This Works

1. **Commits are atomic** - Either the commit exists or it doesn't
2. **History is immutable** - No one can corrupt past state
3. **State is derived** - No separate state file to corrupt
4. **Actions are idempotent** - Running zstate twice gives same result

## The Minimal Recovery Implementation

```bash
# This is the entire recovery strategy:
bin/zstate  # Derive state from git history
# Then act on the action field
```

Compare to traditional approaches:
- Transaction logs
- Write-ahead logs
- Saga patterns
- Compensation handlers

All replaced by: read git history, calculate state.

## Tradeoffs

**Gained:**
- Simplicity (fewer moving parts)
- Auditability (git log is the audit trail)
- Debuggability (state is reproducible from history)

**Lost:**
- Performance (reading full history each time)
- Granularity (only commit-level checkpoints)
- Flexibility (git constraints apply)

## The Insight

Recovery complexity correlates with state complexity.
Minimize state → minimize recovery code.
Git-native design minimizes state by deriving it.
