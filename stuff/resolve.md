# Resolve

Patterns for resolving disagreements.

## Resolution Methods

### 1. Majority Vote
- Count +1 and -1
- Net positive = PASSED
- Net negative = REJECTED
- Zero = DEADLOCKED (needs more voters)

### 2. Consent-Based
- Rule passes unless someone blocks
- Block requires stated reason
- Different from consensus (don't need agreement, just no blocks)

### 3. Time-Bound
- After N cycles, deadlock auto-resolves
- Prevents permanent stalemates

## Current Default
Majority vote (simplest).

```bash
echo "=== Resolution Status ==="
echo "Method: Majority Vote"
echo "Threshold: net positive"
echo "Deadlock handling: wait for more voters"
```

## Links
- [[dissent.md]] - Experiment overview
- [[debate.md]] - Active debates
