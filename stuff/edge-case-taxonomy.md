# Edge Case Taxonomy

A structured classification of edge cases in autonomous agent loops,
building on the rev65 exploration.

## Classification Dimensions

### By Frequency
| Frequency | Examples |
|-----------|----------|
| Common | Rate limits, network blips, context overflow |
| Occasional | Pre-commit failures, API changes |
| Rare | Disk full, repository corruption, concurrent access |

### By Recoverability
| Category | Recovery | Examples |
|----------|----------|----------|
| Self-healing | Retry works | Rate limits, transient network |
| Needs reset | Restart loop | Stuck iteration, memory leak |
| Needs intervention | Human required | Invalid credentials, broken hook |

### By Impact
| Impact | Description | Examples |
|--------|-------------|----------|
| Token waste | Resources spent, no progress | Failed iteration retried |
| State divergence | Intent != committed state | Partial commit |
| Data loss | Information destroyed | Interrupted mid-write |
| Corruption | System integrity compromised | Concurrent writes |

## The Zloop Edge Case Matrix

```
             Self-healing    Needs Reset    Needs Intervention
Common       [rate limit]    [context overflow]    -
Occasional   [network]       [stuck loop]    [hook failure]
Rare         -               -               [corruption]
```

Most edge cases cluster in the self-healing/common quadrant.
This is why fail-soft with retry works well.

## Design Principle

Optimize for the common case (self-healing failures).
Accept degraded handling of rare cases.
Document what requires intervention.

The current zloop design follows this principle:
- Common failures: absorbed by `|| true`, loop continues
- Occasional failures: loop eventually times out
- Rare failures: require manual intervention (acceptable)
