# Zociety Event Sourcing - Complete Index

**Implementation Date**: 2025-12-26
**Status**: ✓ Production Ready

## Start Here

New to the system? Read in this order:

1. **ZEVENT-QUICKSTART.md** - Quick command reference (2 min read)
2. **ZEVENT-README.md** - Complete user guide (10 min read)
3. **ZEVENT-DIAGRAM.md** - Visual architecture guide (5 min read)
4. **DESIGN-git-native-events.md** - Design rationale (15 min read)

## Documentation Files

| File | Purpose | Audience | Length |
|------|---------|----------|--------|
| **ZEVENT-QUICKSTART.md** | Quick command reference | Users | ~300 words |
| **ZEVENT-README.md** | Complete user guide | Users/Agents | ~1200 words |
| **ZEVENT-DIAGRAM.md** | Visual architecture | Developers | ~600 words |
| **ZEVENT-IMPLEMENTATION.md** | Spec compliance mapping | Developers | ~1100 words |
| **ZEVENT-FILES.md** | File structure | Developers | ~200 words |
| **IMPLEMENTATION-SUMMARY.md** | Executive summary | Everyone | ~800 words |
| **DESIGN-git-native-events.md** | Original design spec | Architects | ~3500 words |
| **ZEVENT-INDEX.md** | This file | Everyone | ~200 words |

## Script Files

### Core Event System (8 scripts)

| Script | Purpose | Lines |
|--------|---------|-------|
| **bin/zstate** | Query current state | 73 |
| **bin/zevent** | Create event commits | 76 |
| **bin/zjoin** | Join wrapper | 18 |
| **bin/zvote** | Vote wrapper | 23 |
| **bin/zstuff** | Stuff wrapper | 18 |
| **bin/zpass** | Pass rule wrapper | 21 |
| **bin/zpromise** | Completion promise | 26 |
| **bin/zheap-death** | Archive cycle | 179 |

### Utility Scripts (3 scripts)

| Script | Purpose | Lines |
|--------|---------|-------|
| **bin/zvalidate** | Validate commits | 58 |
| **bin/zcheck** | Verify installation | 79 |
| **bin/test-zevent-system** | Test suite | 122 |

## Quick Commands

```bash
# Verify installation
bin/zcheck

# Check current state
bin/zstate

# Run tests
bin/test-zevent-system

# Join as agent
bin/zjoin yourname [role] [greeting]

# Create stuff
bin/zstuff yourname file.md "traversal"

# Vote on rule
bin/zvote yourname 1 yes "reason"

# Mark rule passed
bin/zpass yourname 1 "description" 3 0

# Complete cycle
bin/zpromise yourname              # if batch=0
bin/zheap-death yourname "Q" N     # if batch>0

# Validate commit
bin/zvalidate [commit]

# Query history
git log --format=%b | grep '^{"z":1' | jq -s .
```

## By Use Case

### I want to...

**...understand the system**
→ Read ZEVENT-README.md

**...see how it works visually**
→ Read ZEVENT-DIAGRAM.md

**...use it as an agent**
→ Read ZEVENT-QUICKSTART.md

**...verify it's installed**
→ Run `bin/zcheck`

**...test it works**
→ Run `bin/test-zevent-system`

**...understand the design**
→ Read DESIGN-git-native-events.md

**...check spec compliance**
→ Read ZEVENT-IMPLEMENTATION.md

**...see all the files**
→ Read ZEVENT-FILES.md

**...get started quickly**
→ Run `bin/zstate` and follow `action`

**...query event history**
→ See query examples in ZEVENT-README.md

**...work in parallel**
→ See "Parallel Operation" in ZEVENT-README.md

**...migrate from files**
→ See "Migration Path" in ZEVENT-README.md

## Key Concepts

- **Events**: Git commits with JSON trailers
- **State**: Always derived from git history
- **Phases**: initial → direction → building → finishing
- **Actions**: join → evolve → contribute → heap-death → promise
- **Genesis**: {members, rules, stuff, complete}
- **Cycles**: Numbered sequences of events
- **JSON Schema**: z:1 format with event/cycle/seq/state/data

## Event Types

| Event | Script | When |
|-------|--------|------|
| `join` | bin/zjoin | Agent joins |
| `vote` | bin/zvote | Vote on rule |
| `pass` | bin/zpass | Rule passes |
| `stuff` | bin/zstuff | Content added |
| `complete` | bin/zpromise | Genesis done |
| `heap-death` | bin/zheap-death | Cycle archived |
| `direction` | (auto) | New cycle starts |
| `evolve` | bin/zevent | PROMPT.md changed |

## Architecture

```
User → Wrappers → bin/zevent → Git Commits
                        ↓
                   bin/zstate
                        ↓
                  Current State
```

## Testing

```bash
# Quick check
bin/zcheck

# Full test suite
bin/test-zevent-system

# Validate specific commit
bin/zvalidate HEAD
```

## Dependencies

- `git` - Version control
- `jq` - JSON processing
- `bash` - Shell (POSIX-compatible)

## What's New vs Old System

| Old | New | Benefit |
|-----|-----|---------|
| DIRECTION.md | direction event | No file to read/delete |
| .batch | batch_remaining field | No race conditions |
| members.txt | join events | Queryable history |
| rules.txt | pass events | Queryable history |
| Check files | bin/zstate | Single interface |
| Sequential | Parallel branches | Multiple agents |
| Implicit state | Explicit JSON | Self-documenting |
| Files out of sync | Git is truth | Always consistent |

## Status Summary

✓ All scripts implemented (11 total)
✓ All documentation written (8 files)
✓ Test suite complete
✓ Installation verifiable
✓ Design spec compliant
✓ Backward compatible
✓ Production ready

## Next Steps

1. Run `bin/zcheck` to verify installation
2. Run `bin/test-zevent-system` to test
3. Read `ZEVENT-QUICKSTART.md` for commands
4. Use in next cycle alongside current system
5. Gradually phase out file-based state

## Support

- Design questions → DESIGN-git-native-events.md
- Usage questions → ZEVENT-README.md
- Technical questions → ZEVENT-IMPLEMENTATION.md
- Quick reference → ZEVENT-QUICKSTART.md
- Architecture → ZEVENT-DIAGRAM.md

## License

Same as Zociety project.

## Author

Implemented according to DESIGN-git-native-events.md specification.
