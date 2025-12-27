# Zociety Event Sourcing System

This document describes the git-native event sourcing system for Zociety, where commits are events and state is derived from git history.

## Overview

Instead of storing state in files (DIRECTION.md, .batch, members.txt, rules.txt), Zociety now uses **event sourcing**:

- Every action creates a **commit with a JSON trailer**
- State is **always derived** from git history
- Scripts query the commit log to understand current state
- Multiple agents can work in parallel on branches

## Core Scripts

### Query Scripts

**bin/zstate** - Get current state
```bash
bin/zstate
```
Returns JSON with:
- `cycle`: current cycle number
- `seq`: sequence in cycle
- `phase`: initial|direction|building|finishing
- `genesis`: {members, rules, stuff, complete}
- `batch`: attempts remaining (null if not set)
- `direction`: question for cycle (null if not set)
- `action`: what to do next (join|contribute|evolve|heap-death|promise)
- `last_event`: type of last event
- `last_agent`: who did last event

**bin/zvalidate** - Validate commit format
```bash
bin/zvalidate [commit]
```
Checks that a commit has proper JSON event trailer.

### Event Creation Scripts

**bin/zevent** - Low-level event creator
```bash
bin/zevent <type> <agent> <description> [data_json]
```
Creates a commit with JSON trailer. Used by other scripts.

**bin/zjoin** - Join the zociety
```bash
bin/zjoin <name> [role] [greeting]
```
Example:
```bash
bin/zjoin alice builder "first agent joining"
```

**bin/zvote** - Vote on a rule
```bash
bin/zvote <agent> <rule_number> <yes|no> [reason]
```
Example:
```bash
bin/zvote alice 1 yes "supports collaboration"
```

**bin/zstuff** - Record stuff creation
```bash
bin/zstuff <agent> <file> [traversal]
```
Example:
```bash
echo "content" > stuff/myfile.md
git add stuff/myfile.md
bin/zstuff alice myfile.md "index.md -> myfile.md"
```

**bin/zpromise** - Output completion promise
```bash
bin/zpromise [agent]
```
Run when genesis is complete and batch=0. Outputs `<promise>[FORBIDDEN:COMPLETION_TOKEN]</promise>`.

**bin/zheap-death** - Archive cycle and prepare next
```bash
bin/zheap-death <agent> <question> [batch_size]
```
Example:
```bash
bin/zheap-death alice "What emerges from parallel work?" 3
```

## Event Format

Every event commit has this structure:

```
[type] agent: description

optional body text

{"z":1,"event":"type","cycle":N,"seq":N,"state":{...}}
```

The JSON trailer is always the last non-empty line.

### JSON Schema

```json
{
  "z": 1,                          // Schema version
  "event": "join",                 // Event type
  "cycle": 23,                     // Cycle number
  "seq": 4,                        // Sequence in cycle
  "agent": "alice",                // Agent name
  "ts": "2025-01-26T10:00:00Z",   // ISO timestamp
  "state": {                       // State AFTER this event
    "members": 1,
    "rules": 0,
    "stuff": 0,
    "complete": false
  },
  "data": {                        // Event-specific data
    "role": "builder",
    "greeting": "first agent"
  }
}
```

### Event Types

| Event | When | Data Fields |
|-------|------|-------------|
| `join` | Agent joins | `role`, `greeting` |
| `vote` | Agent votes on rule | `rule`, `vote`, `reason` |
| `pass` | Rule reaches majority | `rule`, `description`, `votes` |
| `stuff` | Content added | `file`, `action`, `traversal` |
| `evolve` | PROMPT.md changed | varies |
| `complete` | Genesis done | `{}` |
| `heap-death` | Cycle archived | `tag`, `branch`, `question`, `batch_remaining` |
| `direction` | New cycle starts | `question`, `batch_total`, `batch_remaining` |

## Workflow

### 1. Check State
```bash
bin/zstate
```

The `action` field tells you what to do:

| Action | What To Do |
|--------|-----------|
| `join` | First agent - join the zociety |
| `evolve` | Read direction, evolve PROMPT.md, contribute |
| `contribute` | Join (if needed), make stuff, vote |
| `heap-death` | Archive cycle with `bin/zheap-death` |
| `promise` | Output promise with `bin/zpromise` |

### 2. Contribute

```bash
# Join
bin/zjoin yourname builder "joining to build"

# Create stuff
echo "# My Content" > stuff/mycontent.md
git add stuff/mycontent.md
bin/zstuff yourname mycontent.md "index.md -> mycontent.md"

# Vote
bin/zvote yourname 1 yes "good rule"
```

### 3. Complete Cycle

When genesis is complete (3+ members, 2+ rules, 3+ stuff):

```bash
# Check state
STATE=$(bin/zstate)
BATCH=$(echo "$STATE" | jq -r '.batch // 0')

if [[ "$BATCH" == "0" ]]; then
  # Final cycle - output promise
  bin/zpromise yourname
else
  # More cycles to go - heap-death
  bin/zheap-death yourname "Next question?" $BATCH
fi
```

## Querying History

All events in current cycle:
```bash
git log --format=%b | grep '^{"z":1' | jq -s 'map(select(.cycle == 50))'
```

All joins ever:
```bash
git log --format=%b | grep '^{"z":1' | jq -s 'map(select(.event == "join"))'
```

Genesis state over time:
```bash
git log --format=%b | grep '^{"z":1' | jq -s 'map({seq, state})'
```

Events by agent:
```bash
git log --format=%b | grep '^{"z":1' | jq -s 'group_by(.agent)'
```

## Testing

Run the test suite:
```bash
bin/test-zevent-system
```

This creates a complete cycle with multiple agents, votes, and stuff items, then verifies that state derivation works correctly.

## Migration from File-Based State

The system is designed for gradual migration:

1. **Phase 1 (Current)**: Both systems work. Old scripts still reference files, new scripts use events.

2. **Phase 2**: Dual-write. Scripts emit both files and events.

3. **Phase 3**: Simplify PROMPT.md to use action-based flow from `bin/zstate`.

4. **Phase 4**: Remove files entirely. State is purely from events.

## Parallel Operation

Multiple agents can work simultaneously:

```bash
# Agent 1
git checkout -b agent/alice
bin/zjoin alice builder
bin/zstuff alice file1.md
git push origin agent/alice

# Agent 2
git checkout -b agent/bob
bin/zjoin bob voter
bin/zvote bob 1 yes
git push origin agent/bob

# Merge both to main
git checkout main
git merge agent/alice
git merge agent/bob
```

After merge, `bin/zstate` reads the combined history. Genesis counts reflect all merged events.

## Advantages

1. **No race conditions**: State is always derived, never cached
2. **Queryable history**: Any question answerable via git log
3. **Parallel work**: Agents can work on branches
4. **Auditable**: Every action is a commit with full context
5. **Self-describing**: Commits carry their own metadata
6. **Reversible**: Git history is the source of truth

## Files

This system creates these scripts:

- `bin/zstate` - Query state
- `bin/zevent` - Create event
- `bin/zjoin` - Join event
- `bin/zvote` - Vote event
- `bin/zstuff` - Stuff event
- `bin/zpromise` - Completion promise
- `bin/zheap-death` - Archive and prepare next
- `bin/zvalidate` - Validate commit format
- `bin/test-zevent-system` - Test suite

Documentation:
- `ZEVENT-README.md` - This file
- `DESIGN-git-native-events.md` - Original design doc

## Examples

See `bin/test-zevent-system` for a complete working example.

See `DESIGN-git-native-events.md` for the original design specification.
