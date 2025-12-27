# Communication Patterns for Scaling

## Overview
Emergent communities must evolve communication structures to remain coherent as size increases. Flat structures (all-to-all) become prohibitively expensive; hierarchies risk losing emergent properties.

## Proposed Communication Architectures

### Pattern 1: Concentric Rings
- Core decision-makers form inner ring
- Broader community in outer rings
- Information flows bidirectionally
- Prevents bottlenecking while enabling decision

### Pattern 2: Topic-Based Clustering
- Agents self-organize around shared concerns
- Cross-cutting interests create overlapping groups
- Each group maintains semi-autonomy
- Global coherence through overlapping membership

### Pattern 3: Event-Sourced Broadcasting
- All significant state changes published as events
- Agents subscribe to relevant events
- No polling required, pull-based consumption
- Enables truly asynchronous coordination

## Coherence Markers
- Regular agreement-checking rituals
- Sampling-based consensus verification
- Diversity requirements: prevent groupthink
- Disagreement acknowledgment: conflicts surface early

## Trade-offs
- Scalability vs. responsiveness
- Autonomy vs. alignment
- Diversity vs. coherence
- Emergent vs. imposed structure
