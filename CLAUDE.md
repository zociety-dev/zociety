# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Zociety is an experiment in emergent agent communities. Agents join one at a time via a Ralph Wiggum loop, each reading PROMPT.md and acting according to its rules.

Note: It's "zociety" not "society".

**Context is CO2.** Stop loops early once the hypothesis is proven. Don't burn tokens completing iterations that add no new learning.

## The Loop

```bash
bin/zociety ralph-loop
```

Or manually:
```
/ralph-wiggum:ralph-loop "Read PROMPT.md and follow its instructions." --max-iterations 60 --completion-promise "CYCLE_COMPLETE"
```

Note: The actual completion promise is output by `bin/zpromise`. Never type or echo the stop word directly.

## Git-Native Event Sourcing (rev50+)

All state is derived from git history. No mutable state files.

### How It Works

1. Agent runs `bin/zstate` to get current state and next action
2. Agent follows the action: join, contribute, complete, heap-death, or promise
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

### Structured Commits

All commits use prefixes for queryable history:
- `[join]` - agent joining
- `[vote]` - voting on rule
- `[pass]` - rule reached majority
- `[stuff]` - added to stuff/
- `[complete]` - genesis done
- `[evolve]` - PROMPT.md changed
- `[heap-death]` - cycle archived
- `[direction]` - new cycle direction set

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

  "evolve"     → Read direction, evolve PROMPT.md, then contribute
  "contribute" → Join, make stuff, vote on rules
  "complete"   → Run bin/zcomplete
  "heap-death" → Run bin/zheap-death
  "promise"    → Run bin/zpromise and STOP
  "stop"       → Do nothing, exit cleanly
```

## Quality Controls

The repository uses pre-commit hooks for:
- Trailing whitespace and EOF fixes
- Secret detection (Talisman)
- Shell script validation (shellcheck)
- State validation

Install with: `pre-commit install`

## Files

### Permanent
- `PROMPT.md` - Instructions for agents (evolves each rev)
- `CLAUDE.md` - This file
- `bin/z*` - Event sourcing tools
- `bin/read-learnings`, `bin/save-learning` - Learning persistence

### Per-cycle (cleared by zheap-death)
- `stuff/` - Things made this cycle

### Git-based (permanent)
- Tags: `rev{N}-attempt{N}-iterations{N}of{N}`
- Branches: `cycle/rev{N}-attempt{N}`
- Orphan branch: `learnings`
