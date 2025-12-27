# GA Loop Safety Boundaries

Pattern: **Self-reference** - the loop observing its own limits

## Why Safety Matters

An autonomous loop that triggers itself can:
- Burn API credits indefinitely
- Create runaway commit histories
- Overwhelm GitHub Actions quotas
- Generate incoherent output without human review

## Boundary Layers

### Layer 1: Iteration Limits

```yaml
inputs:
  iterations:
    default: '5'  # Hard cap per dispatch
```

The workflow counts down and stops at zero.

### Layer 2: Time Limits

GitHub Actions has built-in job timeouts:
```yaml
jobs:
  iterate:
    timeout-minutes: 30  # Max time per iteration
```

### Layer 3: Concurrency Control

```yaml
concurrency:
  group: zociety-loop
  cancel-in-progress: false  # Don't overlap runs
```

Only one loop runs at a time.

### Layer 4: State-Based Exit

The loop checks `bin/zstate` for natural completion:
```bash
ACTION=$(bin/zstate | jq -r .action)
if [[ "$ACTION" == "promise" ]] || [[ "$ACTION" == "stop" ]]; then
  exit 0  # Natural completion
fi
```

### Layer 5: Human Override

workflow_dispatch allows manual triggering with custom iteration count.
Humans can also cancel running workflows via GitHub UI.

## The Meta-Boundary

This document itself is a boundary - a record of the system reflecting
on its own limits. The loop that reads this understands why it stops.

## Monitoring Recommendations

1. Set up GitHub Actions usage alerts
2. Watch for unusual commit frequency
3. Review loop output periodically
4. Keep iteration counts conservative initially
