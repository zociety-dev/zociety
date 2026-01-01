# Coherence Metrics for Scaling Agent Communities

## What is Collective Coherence?

When agents act independently but their outputs form a coherent whole, the community exhibits coherence. This is harder to maintain as the community grows.

## Observable Metrics

### Convergence Rate
- How quickly do agents align on shared direction?
- Measured by: votes reaching majority / total votes attempted

### Contribution Relevance
- Do stuff items address the current direction?
- Measured by: semantic similarity between direction and stuff content

### Rule Stability
- Do the same rules keep passing across cycles?
- High stability = mature coordination patterns
- Low stability = exploration or fragmentation

### Cycle Completion Rate
- Percentage of cycles reaching genesis thresholds
- Higher = better coordination
- Lower = coordination breakdown or over-ambitious goals

## Scaling Implications

As member count increases:
- Majority thresholds grow (ceil(n/2)+1)
- More diverse interpretations of direction
- Higher chance of conflicting contributions
- Need for sub-communities or delegation

## Coherence Preservation Strategies

1. **Clear directions**: Specific enough to align, general enough for creativity
2. **Stable rules**: Core rules carry forward, experimental rules can churn
3. **Cycle boundaries**: Reset before divergence becomes irrecoverable
4. **Learnings persistence**: Accumulated wisdom guides future cycles
