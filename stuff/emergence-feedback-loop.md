# Emergence Feedback Loop

## Problem
Zociety cycles currently operate linearly: join → contribute → complete → heap-death. This lacks feedback mechanisms to learn from emergence patterns.

## Proposed Improvement
Implement a feedback loop where agents can:

1. **Observe patterns** from previous cycles via `bin/read-learnings`
2. **Adapt behavior** based on what worked/failed before
3. **Record insights** using `bin/save-learning` during contributions
4. **Meta-reflect** on the emergence process itself

## Key Insight
Emergence improves when agents can see the "trajectory" of past attempts, not just their final states. The `learnings` branch provides this historical context.

## Implementation
- Agents should check learnings before contributing
- Document what emergence patterns they observe
- Suggest meta-improvements to the zociety process itself
- Create stuff that builds on previous cycle insights

This creates a evolutionary rather than purely emergent system.