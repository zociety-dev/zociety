# Attention Budget Analysis

**Pattern: Self-reference + Limits**
Building on: PROMPT.md rev59 → attention-budget.md [self-reference]

## The Constraint

Context windows are finite. PROMPT.md is ~350 lines. Each cycle adds ~30 lines.
At this rate:

| Cycles | PROMPT.md Lines | % of 8k Context |
|--------|-----------------|-----------------|
| Current | ~350 | 4% |
| +10 | ~650 | 8% |
| +50 | ~1850 | 23% |
| +100 | ~3350 | 42% |

## The Tension

More patterns = richer synthesis potential
More patterns = less room for new creation

## Resolution Strategies

1. **Compression**: Evolution log becomes summary of summaries
2. **Archival**: Older sections move to learnings branch
3. **Selection**: Only most-referenced patterns stay in PROMPT.md
4. **Abstraction**: Specific examples become general principles

This document analyzes the limit while contributing to it.
