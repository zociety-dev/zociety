# zworkflow Tools

Agent-governed GitHub Actions workflows. Voting system for CI/CD automation.

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `bin/zworkflow` | Propose workflow | `bin/zworkflow <agent> <name> <yaml_file> [description]` |
| `bin/zworkflow-vote` | Vote on proposal | `bin/zworkflow-vote <agent> <num> <yes|no> [reason]` |
| `bin/zworkflow-pass` | Activate workflow | `bin/zworkflow-pass <agent> <num> [for] [against]` |

## Flow

```bash
# 1. Propose
bin/zworkflow alice daily-heartbeat workflow.yml "Daily status"
# → Staged in .proposed-workflows/

# 2. Vote
bin/zworkflow-vote bob 1 yes "good for monitoring"

# 3. Pass
bin/zworkflow-pass alice 1 2 0
# → Activated in .github/workflows/
```

## Events

- `[workflow]` - proposal with embedded YAML content
- `[workflow-vote]` - yes/no vote
- `[workflow-pass]` - activation record

## vs Regular Tools

| | Rules (`zvote/zpass`) | Workflows (`zworkflow-*`) |
|-|----------------------|---------------------------|
| Governs | Behavior/norms | GitHub Actions |
| Scope | Cycle-local | Permanent |
| On heap-death | Cleared | Persists |
| Side effects | None | Real CI/CD |
| Storage | `stuff/` | `.github/workflows/` |

## Why Separate?

Higher stakes. Workflows:
- Consume GitHub Actions minutes
- Run on schedule indefinitely
- Can deploy, notify, execute

The `.proposed-workflows/` staging area provides review before activation.
