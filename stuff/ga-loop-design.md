# GitHub Actions Loop Design

Pattern: **Compounding** - building on existing git-native event sourcing

## The Problem

The zociety loop currently requires:
1. Human runs `bin/zociety` locally
2. Container with Claude Code executes
3. Agent iterates via ralph-loop
4. Results commit back to git

Can this run headlessly in GitHub Actions?

## Proposed Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Trigger Event  │────▶│  GA Workflow    │────▶│  Commit Result  │
│  (dispatch/push)│     │  (claude --print)│     │  (git push)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │                        │
                                ▼                        ▼
                        ┌───────────────┐        ┌───────────────┐
                        │  bin/zstate   │        │  Trigger Next │
                        │  (get action) │        │  (if !complete)│
                        └───────────────┘        └───────────────┘
```

## Key Components

### 1. API Mode Entry Point

Claude Code supports `--print` mode for non-interactive use:
```bash
claude --print "Read PROMPT.md and follow bin/zstate action"
```

This outputs to stdout instead of requiring TTY.

### 2. Iteration Strategy

Option A: **Matrix Strategy**
- Single workflow creates N jobs
- Each job runs one iteration
- Simple but fixed iteration count

Option B: **Self-Triggering**
- Workflow dispatches itself after commit
- Continues until genesis complete
- Dynamic but requires care to avoid infinite loops

Option C: **Scheduled Heartbeat**
- Cron triggers workflow periodically
- Each run does one iteration
- Slow but resilient

### 3. Completion Detection

The workflow checks `bin/zstate | jq -r .action`:
- If "promise" or "stop" → exit cleanly
- Otherwise → continue or trigger next

### 4. Commit Strategy

```yaml
- name: Commit and push
  run: |
    git config user.name "zociety[bot]"
    git config user.email "zociety[bot]@users.noreply.github.com"
    git add -A
    git diff --cached --quiet || git commit -m "[action] result"
    git push
```

## Open Questions

1. **Credentials** - How does ANTHROPIC_API_KEY get injected?
2. **Concurrency** - How to prevent overlapping runs?
3. **Rate Limits** - How many iterations per hour are safe?
4. **Observability** - How do humans monitor the loop?

## Next Steps

1. Create minimal workflow YAML
2. Test with workflow_dispatch trigger
3. Add self-continuation logic
4. Implement safety boundaries
