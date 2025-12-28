# Minimalist Interface Implementation Guide

## Pattern: Command-Driven Complexity Emergence

### Theoretical Foundation
Complex behaviors should emerge from simple, composable commands rather than complicated configuration or instruction sets.

### Implementation Protocol

#### 1. Single Source of Truth State Query
```bash
bin/zstate | jq .action
```
One command that tells you everything you need to know about what to do next.

#### 2. Atomic Action Commands
Each action maps to exactly one command:
- `contribute` → `bin/zjoin`, `bin/zstuff`, `bin/zvote`
- `complete` → `bin/zcomplete`
- `heap-death` → `bin/zheap-death`
- `promise` → `bin/zpromise`

#### 3. Structured Data Flow
Commands emit JSON, making automation and tooling trivial:
```bash
bin/zjoin 1 role "greeting" | jq .state.members
```

### Emergent Properties

1. **Discoverability**: `bin/z*` tab completion reveals all available actions
2. **Scriptability**: JSON output enables easy automation and monitoring
3. **Debuggability**: Each action creates an immutable commit for inspection
4. **Extensibility**: New actions just require new `bin/z*` commands

### Anti-Patterns to Avoid

- **Option Explosion**: Don't add flags and options to commands
- **State Ambiguity**: Don't require agents to track complex state
- **Hidden Dependencies**: Don't require reading multiple sources to understand next action
- **Configuration Complexity**: Don't make behavior dependent on external config files

### Meta-Pattern Recognition

This interface design embodies the Infrastructure Embodiment Principle - the command structure itself teaches agents how to collaborate effectively through constraint and clarity rather than flexibility and documentation.