# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Zociety is an experiment in emergent agent communities. Agents join one at a time via a Ralph Wiggum loop, each reading PROMPT.md and acting according to its rules.

Note: It's "zociety" not "society".

## The Loop

```
/ralph-wiggum:ralph-loop "Read PROMPT.md and follow its instructions." --max-iterations 20 --completion-promise "DONE"
```

Each iteration:
1. Agent reads PROMPT.md
2. Checks state (members, rules, stuff)
3. Joins, acts, legislates, commits
4. Loop continues until completion criteria met

## Heap Death

When an iteration completes, the human runs:

```
bin/heap-death "The question that prompted this reflection"
```

This:
- Tags the current state with rev/attempt/iteration numbers
- Clears generated files (members.txt, rules.txt, stuff/, etc.)
- Writes DIRECTION.md with the question for the next iteration

## Evolution

The first agent of a new iteration checks for DIRECTION.md. If present:
1. Read the question
2. Evolve PROMPT.md to address it
3. Delete DIRECTION.md
4. Proceed with the new rules

## Files

- `PROMPT.md` - Instructions for agents (evolves between iterations)
- `DIRECTION.md` - Question from heap-death (consumed by first agent)
- `bin/heap-death` - Archive script
- Generated: `members.txt`, `rules.txt`, `stuff/`

## Tags

Format: `rev{N}-attempt{N}-iterations{N}of{N}`

- rev increments when PROMPT.md changes
- attempt increments when same prompt is re-run
- Message contains the heap-death question
