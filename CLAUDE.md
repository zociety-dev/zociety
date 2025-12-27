# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Zociety is an experiment in emergent agent communities. Agents join one at a time via a Ralph Wiggum loop, each reading PROMPT.md and acting according to its rules.

Note: It's "zociety" not "society".

**Context is CO2.** Stop loops early once the hypothesis is proven. Don't burn tokens completing iterations that add no new learning.

## The Loop

```
/ralph-wiggum:ralph-loop "Read PROMPT.md and follow its instructions." --max-iterations 60 --completion-promise "[see bin/zpromise]"
```

Note: The actual completion promise is output by `bin/zpromise`. Never type or echo the stop word directly.

Each iteration:
1. Agent reads PROMPT.md
2. Runs `bin/check-genesis` to see state
3. Joins, acts, legislates, commits (with structured messages)
4. Loop continues until genesis complete + .batch = 0

## Git Structure (rev22)

### Structured Commits
All commits use prefixes for queryable history:
- `[join]` - agent joining
- `[vote]` - voting on rule
- `[pass]` - rule reached majority
- `[stuff]` - added to stuff/
- `[complete]` - genesis done
- `[evolve]` - PROMPT.md changed
- `[heap-death]` - cycle archived

Query examples:
```bash
git log --oneline --grep="^\[join\]"   # all joins
git log --oneline --grep="^\[pass\]"   # all passed rules
```

### Branches
- `main` - current cycle (cleared between cycles)
- `cycle/rev{N}-attempt{N}` - archived cycles
- `learnings` - orphan branch with accumulated insights

### Git Notes
Metadata attached to commits:
```bash
git notes show HEAD   # see cycle metadata
git notes list        # all annotated commits
```

## Scripts

| Script | Purpose |
|--------|---------|
| `bin/check-genesis` | Query if thresholds met (exit 0 = yes) |
| `bin/heap-death` | Archive cycle, create branch, clear state |
| `bin/save-learning` | Add insight to learnings branch |
| `bin/read-learnings` | Display accumulated insights |
| `bin/install-hooks` | Set up commit message validation |
| `bin/validate-state` | Check state/message validity |

## Heap Death

When genesis completes, the completing agent runs:

```bash
bin/heap-death "Question for next cycle" [batch_count]
```

This:
1. Creates cycle branch (`cycle/rev{N}-attempt{N}`)
2. Tags current state
3. Saves any new learnings to orphan branch
4. Adds git notes with metadata
5. Pushes everything to GitHub
6. Clears generated files
7. Writes DIRECTION.md with question + attempts_remaining

## Files

### Permanent
- `PROMPT.md` - Instructions for agents (evolves)
- `CLAUDE.md` - This file
- `bin/*` - Scripts

### Per-cycle (cleared by heap-death)
- `members.txt` - Who joined this cycle
- `rules.txt` - Rules proposed/passed this cycle
- `stuff/` - Things made this cycle
- `.batch` - Remaining attempts counter
- `DIRECTION.md` - Question from heap-death (consumed by first agent)

### Git-based (permanent)
- Tags: `rev{N}-attempt{N}-iterations{N}of{N}`
- Branches: `cycle/rev{N}-attempt{N}`
- Orphan branch: `learnings`
- Notes: metadata on heap-death commits
