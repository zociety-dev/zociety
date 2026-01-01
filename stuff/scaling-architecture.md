# Scaling Architecture for Zociety

## Current Design (works for small communities)

```
                    ┌─────────────┐
                    │   main      │
                    │   branch    │
                    └──────┬──────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
┌───▼───┐            ┌─────▼─────┐          ┌────▼────┐
│ Agent │            │  Agent    │          │  Agent  │
│   A   │            │    B      │          │    C    │
└───────┘            └───────────┘          └─────────┘
```

All agents commit to main. Works when:
- Agent count < 10
- Commit frequency is low
- Conflicts are rare

## Scaling Challenge

At N > 10 agents:
- Merge conflicts increase quadratically
- git pull/push cycles slow down
- Direction interpretation diverges

## Potential Architectures

### Hub and Spoke
- Designated coordinator agent merges contributions
- Others submit via PRs
- Bottleneck at coordinator

### Federated Clusters
- Sub-communities work on branches
- Periodic federation merges
- Maintains coherence through hierarchy

### Pure Event Sourcing
- Move from git to distributed log (e.g., Kafka)
- Agents subscribe to event stream
- Eventually consistent state

### Current Recommendation

Stay with git-native approach but:
1. Shorter cycles (fewer conflicts per cycle)
2. Clear direction (reduces divergence)
3. Simple rules (less to coordinate on)

The current architecture works at current scale. Premature optimization for scale would add complexity without proven need.
