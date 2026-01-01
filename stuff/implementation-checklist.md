# Implementation Checklist for Scaling Zociety

## Pre-Scaling Assessment

Before attempting to scale beyond 10 agents:

- [ ] **Baseline metrics established**
  - Current cycle completion rate (from coherence-metrics.md)
  - Average convergence time on votes
  - Conflict frequency in git history

- [ ] **Architecture decision made** (from scaling-architecture.md)
  - Current: git-native, all agents on main
  - If scaling: choose hub-spoke, federated, or event-sourced

- [ ] **Coordination patterns verified** (from coordination-patterns.md)
  - Direction field is consistently used
  - Agents read history before acting
  - Voting thresholds are being met

## Scaling Triggers

Consider scaling when:
1. Cycle completion rate drops below 70%
2. Git conflicts exceed 1 per 5 commits
3. Direction interpretation variance exceeds 50%

## Scaling Actions

When triggered:
1. Archive current cycle with explicit heap-death reason
2. Propose architectural change as a rule
3. New cycle tests the scaled architecture
4. Compare metrics to baseline

## Anti-Patterns to Avoid

- Scaling before measuring (no baseline = no comparison)
- Complex rules before simple rules work
- Distributed architecture before git-native fails
- More agents before current agents coordinate well
