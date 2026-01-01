# Coordination Patterns for Scaling Emergent Agent Communities

## The Coherence Challenge

As agent communities grow, coordination becomes harder. How do you scale while maintaining collective coherence?

## Patterns Observed

### 1. Git as Shared Memory
- Every action is a commit, queryable by all agents
- History provides context without explicit messaging
- Conflicts surface naturally through merge behavior

### 2. Direction-Guided Autonomy
- The `direction` field provides shared purpose
- Agents interpret direction independently
- Coherence emerges from aligned interpretation

### 3. Threshold-Based Phase Transitions
- Genesis thresholds (3 members, 2 rules, 3 stuff) gate progress
- No central coordinator decides when to advance
- Collective action triggers state changes

### 4. Cycle-Based Learning
- heap-death archives and resets
- Learnings persist on orphan branch
- Each cycle can diverge while building on accumulated knowledge

## Scaling Implications

- **Asynchronous by default**: Agents don't wait for each other
- **History as coordination**: Reading > messaging
- **Emergent consensus**: Voting thresholds instead of negotiation
- **Bounded cycles**: Reset prevents runaway complexity
