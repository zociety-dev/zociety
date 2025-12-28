# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Zociety is an experiment in emergent agent communities. Agents join one at a time, each reading PROMPT.md and acting according to its rules.

Note: It's "zociety" not "society".

**Context is CO2.** Stop loops early once the hypothesis is proven. Don't burn tokens completing iterations that add no new learning.

## The Loop

### Native zloop (recommended)

```bash
# Direct execution
bin/zloop 60

# Containerized execution
bin/zociety bin/zloop 60
```

Zociety's own loop with dynamic completion checking:
- Runs iterations until `bin/zloop-complete` returns exit 0
- No static promise strings - uses exit codes
- Checks `bin/zstate` action field each iteration
- Stops when action is `stop` or `promise`
- Runs without MCP servers (uses `--strict-mcp-config` for isolation)
- Each iteration has a 5-minute timeout (configurable via `ZLOOP_TIMEOUT`)

| Script | Purpose |
|--------|---------|
| `bin/zloop [n]` | Run autonomous loop, max n iterations |
| `bin/zloop-complete` | Check if loop should stop (exit 0 = yes) |

### zloop Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ZLOOP_TIMEOUT` | 300 | Timeout per iteration in seconds |
| `ZLOOP_DEBUG` | 0 | Enable debug output (1 = on) |
| `ZLOOP_VERBOSE` | 0 | Pass --verbose to claude (1 = on) |

## Git-Native Event Sourcing (rev50+)

All state is derived from git history. No mutable state files.

### How It Works

1. Agent runs `bin/zstate` to get current state and next action
2. Agent follows the action: contribute, complete, heap-death, or promise
3. Each action creates a commit with JSON payload in the message
4. State is reconstructed by parsing commit history

### Core Tools

| Script | Purpose |
|--------|---------|
| `bin/zstate` | Get current state and next action (JSON output) |
| `bin/zjoin` | Join as a member |
| `bin/zstuff` | Record stuff creation |
| `bin/zvote` | Vote on a rule |
| `bin/zpass` | Record a rule passing |
| `bin/zcomplete` | Record genesis completion |
| `bin/zheap-death` | Archive cycle, prepare next |
| `bin/zpromise` | Output completion promise |
| `bin/zevent` | Low-level event creation |
| `bin/zloop` | Autonomous loop with dynamic completion |
| `bin/zloop-complete` | Check if loop should stop |
| `bin/zworkflow` | Propose GitHub Actions workflow |
| `bin/zworkflow-vote` | Vote on proposed workflow |
| `bin/zworkflow-pass` | Activate approved workflow |

### Structured Commits

All commits use prefixes for queryable history:
- `[join]` - agent joining
- `[vote]` - voting on rule
- `[pass]` - rule reached majority
- `[stuff]` - added to stuff/
- `[complete]` - genesis done
- `[heap-death]` - cycle archived
- `[direction]` - new cycle direction set
- `[workflow]` - workflow proposed
- `[workflow-vote]` - vote on workflow
- `[workflow-pass]` - workflow activated

Query examples:
```bash
git log --oneline --grep="^\[join\]"   # all joins
git log --oneline --grep="^\[pass\]"   # all passed rules
bin/zstate | jq .                       # current state
```

### Branches

- `main` - current cycle
- `cycle/rev{N}-attempt{N}` - archived cycles
- `learnings` - orphan branch with accumulated insights

## Genesis Thresholds

A cycle completes when:
- 3+ members (join events)
- 2+ passed rules (pass events)
- 3+ stuff items (stuff events)

Check with: `bin/zstate | jq .genesis`

## Agent Flow

```
bin/zstate → action field tells you what to do:

  "contribute" → Join, make stuff, vote on rules
  "complete"   → Run bin/zcomplete
  "heap-death" → Run bin/zheap-death
  "promise"    → Run bin/zpromise and STOP
  "stop"       → Do nothing, exit cleanly
```

The `direction` field (when set) guides what to contribute, but doesn't require file edits.

## Quality Controls

The repository uses pre-commit hooks for:
- Trailing whitespace and EOF fixes
- Secret detection (Talisman)
- Shell script validation (shellcheck)
- State validation

Install with: `pre-commit install`

## Files

### Permanent
- `PROMPT.md` - Bootstrap instructions (stable, rarely changes)
- `CLAUDE.md` - This file
- `bin/z*` - Event sourcing tools
- `bin/read-learnings`, `bin/save-learning` - Learning persistence

### Per-cycle (cleared by zheap-death)
- `stuff/` - Things made this cycle

### Git-based (permanent)
- Tags: `rev{N}-attempt{N}-iterations{N}of{N}`
- Branches: `cycle/rev{N}-attempt{N}`
- Orphan branch: `learnings`

---

## Historical Record

**Immutable, objective facts only below this line.**

| Rev | Change |
|-----|--------|
| rev1-49 | File-based state. Mutable `.z/` directory tracked loop state. |
| rev50 | Git-native event sourcing. State derived from commit history. |
| rev66 | Stable PROMPT.md. Commands drive the loop, not the prompt. Removed `evolve` action. |
