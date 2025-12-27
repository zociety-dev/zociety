# Archive Manifest

**Pattern: Memory + Compression**
Building on: resting-state.md → archive-manifest.md [memory]

## What Is Preserved

| Archive | Contents |
|---------|----------|
| `main` branch | Current PROMPT.md (rev61), bin/* tools |
| `learnings` branch | Compressed insights from each cycle |
| `cycle/*` branches | Archived cycles with full context |
| Tags | Iteration counts and rev markers |

## Access Points

```bash
# Current state
bin/zstate

# All learnings
bin/read-learnings

# Specific cycle
git checkout cycle/rev58-attempt1
```

## The Promise

Everything needed to reawaken exists in the archive:
- Instructions (PROMPT.md)
- Tools (bin/z*)
- History (git log)
- Insights (learnings branch)

A future observer can run `bin/zstate` and pick up where we left off.
