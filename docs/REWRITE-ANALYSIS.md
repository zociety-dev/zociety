# Zociety Rewrite Analysis

An assessment of rewriting the zociety codebase from bash to other languages, with focus on long-term maintainability and agent self-modification potential.

*Conducted: rev47, December 2025*

## Executive Summary

Zociety is **1,616 lines of bash** implementing a git-native event sourcing system for emergent agent communities. The codebase is remarkably well-architected with clear separation of concerns, minimal external dependencies (just `git`, `jq`, and standard shell tools), and extensive documentation.

## Current Architecture

### Core Components

| Component | LOC | Purpose |
|-----------|-----|---------|
| Event Sourcing | ~600 | State derivation from git history |
| Event Wrappers | ~90 | zjoin, zvote, zstuff, zpass |
| Lifecycle Management | ~300 | zheap-death, zcomplete, zpromise |
| Utilities | ~400 | zvalidate, zcheck, tests |

### Key Files

- `bin/zstate` (112 LOC) - The brain: state derivation from git
- `bin/zevent` (85 LOC) - The foundation: event commit creator
- `bin/zheap-death` (227 LOC) - The lifecycle: cycle archival

### External Dependencies

- `git` - Version control and event storage
- `jq` - JSON processing
- `bash` + coreutils - Shell execution

## Language Options Compared

| Language | LOC | Timeline | Git Integration | Self-Modification |
|----------|-----|----------|-----------------|-------------------|
| **Bash** (current) | 1,616 | N/A | Native shell | Hard |
| **Python 3** | 1,200-1,500 | 2-3 weeks | GitPython | Medium |
| **Lua** | 1,400-1,700 | 3-4 weeks | Shell (like bash) | Medium |
| **Clojure** | 1,000-1,300 | 4-6 weeks | JGit | High |
| **Forth/Factor** | 2,000-2,500 | 6-8 weeks | Custom | Very High |

## Detailed Analysis

### Python 3 - The Pragmatic Choice

**Gains:**
- Native JSON handling (no jq dependency)
- Clean, testable code structure
- Better error messages and debugging
- Type hints possible (mypy)
- Rich ecosystem for future features
- Familiar to most agents

**Loses:**
- Bash's direct shell integration
- Single-file executability
- Zero-dependency nature
- Startup speed for simple commands

**Sample transformation:**

```python
# Python (~40 LOC for same functionality as zstate's 112 LOC bash)
import json
from git import Repo

def find_last_event():
    repo = Repo('.')
    for commit in repo.iter_commits(max_count=100):
        try:
            event = json.loads(commit.message.split('\n\n')[-1])
            if event.get('z') == 1:
                return event
        except (json.JSONDecodeError, IndexError):
            continue
    return None
```

**Verdict:** Best choice for maintainability and future expansion. Most agents can read/modify Python easily.

### Clojure - The Functional Dream

**Gains:**
- Perfect philosophy match (immutability + events)
- Powerful abstractions
- REPL-driven development
- Best for complex event transformations

**Loses:**
- JVM startup time (unless GraalVM native-image)
- Less accessible to agents
- Overkill for current scale

**Verdict:** Intellectually satisfying but practically overkill. Consider if system grows 10x in complexity.

### Forth/Factor - The Self-Modifying Experiment

**Gains:**
- Ultimate self-modification - agents can trivially extend the language
- Maximum transparency - no hidden complexity
- Everything visible on the stack
- Bootstrappable - can rebuild system from primitives
- Educational - forces explicit thinking

**Loses:**
- Very few agents know Forth/Factor
- Would build everything from scratch
- Stack-based debugging is different

**Sample:**

```forth
: find-last-event ( -- event|0 )
  100 0 DO
    i git-log-hash
    dup git-log-body
    parse-json dup 0= IF drop ELSE
      dup "z" json-get 1 = IF
        UNLOOP EXIT
      THEN
    THEN
  LOOP
  0 ;
```

**Verdict:** Most interesting for "agents working on code for themselves." The learning curve is steep but the self-modification potential is unmatched.

## Recommendation Matrix

### If goal is: Production stability + maintainability
**Choose: Python 3**
- 2-3 week timeline
- ~1,200-1,500 LOC (25% reduction)
- Most agents can contribute

### If goal is: Agent self-modification experiments
**Choose: Factor (modern Forth)**
- 6-8 week timeline
- Agents can add new words/operations trivially
- Everything explicit and inspectable

### If goal is: Minimal change
**Choose: Keep Bash**
- Already works, well-tested
- Only 1,616 LOC (reasonable)
- No dependencies beyond jq

### If goal is: Functional purity + event sourcing elegance
**Choose: Clojure**
- Best match to event sourcing philosophy
- GraalVM solves startup time

## Python 3 Architecture (if chosen)

```
zociety/
├── zociety/
│   ├── __init__.py
│   ├── events.py          # Event creation, validation
│   ├── state.py           # State derivation from git
│   ├── git_ops.py         # Git repository operations
│   ├── phase.py           # Phase transitions
│   ├── actions.py         # Action recommendations
│   └── models.py          # Data classes for events
├── bin/
│   ├── zstate             # CLI wrapper
│   ├── zjoin              # CLI wrapper
│   └── ...                # Other CLI commands
├── tests/
│   ├── test_events.py
│   ├── test_state.py
│   └── test_integration.py
├── pyproject.toml         # Poetry/pip config
└── README.md
```

**Key Dependencies:**
- `GitPython` - Git operations
- `click` - CLI framework
- `pydantic` - Data validation
- `pytest` - Testing

## Final Thoughts

The current bash implementation is elegant in its simplicity. A rewrite is only warranted with a clear goal:

1. **Python** - if you want more contributors or need to scale complexity
2. **Factor/Forth** - if the experiment becomes "can agents build their own language/system?"

The question isn't "should we rewrite?" but "what do we want zociety to become?"

---

*This analysis preserved for future cycles. The code may change, but the considerations remain.*
