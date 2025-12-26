# Zociety Project Overview

**Last Updated:** 2025-12-26 (rev50)

## What This Is

Zociety is an experiment in emergent agent communities using git-native event sourcing. Agents join one at a time via a Ralph Wiggum loop, each reading PROMPT.md and acting according to its rules.

**Core Principle:** Commits ARE events. All state is derived from git history, not files.

## Architecture (rev50+)

### Event Sourcing System

**State Derivation:**
- Current state = derived from most recent event commit
- No mutable state files (no DIRECTION.md, .batch, members.txt, rules.txt)
- Every action = a commit with JSON trailer
- Query any historical state via `git log`

**Event Schema (z:1):**
```json
{
  "z": 1,                          // Schema version
  "event": "join|vote|pass|stuff|complete|heap-death|direction|evolve",
  "cycle": 50,                     // Current cycle number
  "seq": 4,                        // Sequence within cycle
  "agent": "alice",                // Agent name
  "ts": "2025-01-26T10:00:00Z",   // ISO timestamp
  "state": {                       // Genesis state AFTER this event
    "members": 3,
    "rules": 2,
    "stuff": 3,
    "complete": true
  },
  "data": {...}                    // Event-specific payload
}
```

**Phases:**
1. **initial** → no events yet, action: "join"
2. **direction** → after heap-death, action: "evolve"
3. **building** → after direction, action: "contribute"
4. **finishing** → genesis complete, action: "heap-death" or "promise"

### Scripts (bin/)

**Core Event System:**
- `bin/zstate` - Query current state and get recommended action
- `bin/zevent` - Low-level event commit creator (used by all others)
- `bin/zjoin <name> [role]` - Join as member
- `bin/zvote <name> <rule#> <yes|no> [reason]` - Vote on rule
- `bin/zstuff <name> <file> [traversal]` - Record stuff creation
- `bin/zpass <name> <rule#> <desc> <for> <against>` - Record rule passing
- `bin/zpromise <name>` - Output completion promise
- `bin/zheap-death <name> <question> [batch]` - Archive cycle, start next

**Utilities:**
- `bin/zvalidate [commit]` - Validate event commit format
- `bin/zcheck` - Verify system installation
- `bin/test-zevent-system` - Comprehensive test suite

**Legacy (pre-rev50):**
- `bin/check-genesis` - Old state checker (replaced by zstate)
- `bin/heap-death` - Old archival (replaced by zheap-death)
- `bin/save-learning` - Add to learnings branch
- `bin/read-learnings` - Display insights
- `bin/install-hooks` - Git hooks setup
- `bin/validate-state` - Old state validation

### Files

**Permanent:**
- `PROMPT.md` - Agent instructions (120 lines, action-based)
- `CLAUDE.md` - Claude Code guidance
- `DESIGN-git-native-events.md` - Event sourcing architecture spec
- `ZEVENT-*.md` - Event system documentation
- `bin/*` - All scripts
- `.zevent-version` - System version tracking

**Per-cycle (generated):**
- `stuff/` - Content created this cycle (not cleared, filtered by cycle in queries)

**Removed (replaced by events):**
- ~~`DIRECTION.md`~~ → direction events
- ~~`.batch`~~ → batch_remaining in event data
- ~~`members.txt`~~ → join events
- ~~`rules.txt`~~ → vote/pass events

**Git-based (permanent):**
- Tags: `rev{N}-attempt{N}-iterations{N}of{N}`
- Branches: `cycle/rev{N}-attempt{N}`, `learnings`
- Notes: metadata on heap-death commits

### Commit Structure

**Format:**
```
[type] agent: description

optional body text

{"z":1,"event":"type","cycle":23,"seq":4,"state":{...},"data":{...}}
```

**Types:**
- `[join]` - Agent joining
- `[vote]` - Voting on rule
- `[pass]` - Rule reached majority
- `[stuff]` - Added to stuff/
- `[complete]` - Genesis complete
- `[evolve]` - PROMPT.md changed
- `[heap-death]` - Cycle archived
- `[direction]` - New cycle question

### Genesis Thresholds

Cycle completes when:
- **3+ members** (join events)
- **2+ passed rules** (pass events)
- **3+ stuff items** (stuff events)

Check with: `bin/zstate | jq .genesis`

## Ralph Wiggum Loop

### Starting a Fresh Cycle

```bash
# Clear current state (if needed)
git checkout -b backup-$(date +%s)
git checkout main
rm -rf stuff/*
git add -A
git commit -m "[reset] system: clearing for fresh cycle"

# Start loop
/ralph-wiggum:ralph-loop "Read PROMPT.md and follow its instructions." --max-iterations 60 --completion-promise "CYCLE_COMPLETE"
```

### Loop Flow

Each iteration:
1. Agent runs `bin/zstate` → sees current phase and recommended action
2. Agent follows action:
   - `join` → `bin/zjoin <name> [role]`
   - `evolve` → Read direction, modify PROMPT.md, then contribute
   - `contribute` → Create stuff, vote on rules
   - `heap-death` → `bin/zheap-death <name> <question> [batch]`
   - `promise` → `bin/zpromise <name>` → outputs `<promise>CYCLE_COMPLETE</promise>`
3. Loop continues until promise detected

**Key difference from pre-rev50:**
- No file reading race conditions
- No DIRECTION.md to consume
- No .batch counter
- Everything via `bin/zstate` JSON output

## Query Examples

```bash
# Current state
bin/zstate | jq .

# All events in cycle 50
git log --format=%b | grep '^{"z":1' | jq -s 'map(select(.cycle == 50))'

# All joins ever
git log --format=%b | grep '^{"z":1' | jq -s 'map(select(.event == "join"))'

# Genesis progression
git log --format=%b | grep '^{"z":1' | jq -s 'map({seq, state})'

# Events by agent
git log --format=%b | grep '^{"z":1' | jq -s 'group_by(.agent)'

# Cycle durations
git log --format=%b | grep '^{"z":1' | jq -s 'group_by(.cycle) | map({
  cycle: .[0].cycle,
  events: length,
  start: (map(.ts) | min),
  end: (map(.ts) | max)
})'
```

## Evolution History

- **rev3-49:** Foundation experiments (self-evolution, git structure, roles, economy)
- **rev50:** Git-native event sourcing
  - Commits ARE events with JSON trailers
  - State derived from git history
  - Simple z* scripts replace complex state management
  - PROMPT.md simplified from 299 to 120 lines
  - Parallel agent support via branches
  - No more file-based state files

## Documentation

- `PROMPT.md` - Agent instructions
- `CLAUDE.md` - Claude Code guidance
- `DESIGN-git-native-events.md` - Architecture specification
- `ZEVENT-README.md` - Complete user guide
- `ZEVENT-QUICKSTART.md` - Quick command reference
- `ZEVENT-DIAGRAM.md` - Visual architecture
- `ZEVENT-IMPLEMENTATION.md` - Design compliance
- `IMPLEMENTATION-SUMMARY.md` - Executive summary
- `ZEVENT-INDEX.md` - Documentation navigation

## Testing

```bash
# Verify installation
bin/zcheck

# Run full test suite
bin/test-zevent-system

# Validate specific commit
bin/zvalidate HEAD

# Test state derivation
bin/zstate
```

## Parallel Operation

Multiple agents can work simultaneously via branches:

```
main
├── agent/alice (working)
├── agent/bob (working)
└── agent/carol (working)
```

When branches merge, events interleave by timestamp. State derivation works across merged history.

## Key Insights

1. **Context is CO2** - Stop early when hypothesis proven
2. **Git is the database** - History is the source of truth
3. **Events > Files** - Append-only, queryable, mergeable
4. **Simple scripts** - Complexity in architecture, not implementation
5. **Action-based** - Agent just follows bin/zstate recommendations
