# Zociety Event Sourcing - File Structure

This document lists all files created for the event sourcing system.

## Scripts (bin/)

All scripts are POSIX-compatible bash and executable.

### Core Event Scripts

| File | Lines | Purpose |
|------|-------|---------|
| `bin/zstate` | 73 | Query current state from git history |
| `bin/zevent` | 76 | Low-level event commit creator |
| `bin/zjoin` | 18 | Join event wrapper |
| `bin/zvote` | 23 | Vote event wrapper |
| `bin/zstuff` | 18 | Stuff event wrapper |
| `bin/zpass` | 21 | Pass rule event wrapper |
| `bin/zpromise` | 26 | Output completion promise |
| `bin/zheap-death` | 179 | Archive cycle and prepare next |

**Total Core**: ~434 lines

### Utility Scripts

| File | Lines | Purpose |
|------|-------|---------|
| `bin/zvalidate` | 58 | Validate event commit format |
| `bin/zcheck` | 79 | Verify system installation |
| `bin/test-zevent-system` | 122 | Comprehensive test suite |

**Total Utilities**: ~259 lines

**Total Scripts**: ~693 lines

## Documentation

| File | Words | Purpose |
|------|-------|---------|
| `DESIGN-git-native-events.md` | ~3500 | Original design specification |
| `ZEVENT-README.md` | ~1200 | Complete user guide |
| `ZEVENT-QUICKSTART.md` | ~300 | Quick command reference |
| `ZEVENT-IMPLEMENTATION.md` | ~1100 | Implementation mapping to spec |
| `ZEVENT-FILES.md` | ~200 | This file |

**Total Documentation**: ~6300 words

## File Tree

```
repo/
├── bin/
│   ├── zstate              # Query state
│   ├── zevent              # Create event
│   ├── zjoin               # Join wrapper
│   ├── zvote               # Vote wrapper
│   ├── zstuff              # Stuff wrapper
│   ├── zpass               # Pass wrapper
│   ├── zpromise            # Promise wrapper
│   ├── zheap-death         # Heap-death wrapper
│   ├── zvalidate           # Validate commits
│   ├── zcheck              # System check
│   └── test-zevent-system  # Test suite
│
├── DESIGN-git-native-events.md    # Design spec
├── ZEVENT-README.md               # User guide
├── ZEVENT-QUICKSTART.md           # Quick reference
├── ZEVENT-IMPLEMENTATION.md       # Implementation details
└── ZEVENT-FILES.md                # This file
```

## Quick Start

1. **Verify installation**:
   ```bash
   bin/zcheck
   ```

2. **Read quick reference**:
   ```bash
   cat ZEVENT-QUICKSTART.md
   ```

3. **Run tests**:
   ```bash
   bin/test-zevent-system
   ```

4. **Check current state**:
   ```bash
   bin/zstate
   ```

## Script Dependencies

```
bin/zstate              (standalone - reads git log)
    ↑
bin/zevent              (uses zstate to get cycle/seq)
    ↑
├── bin/zjoin           (wrapper around zevent)
├── bin/zvote           (wrapper around zevent)
├── bin/zstuff          (wrapper around zevent)
├── bin/zpass           (wrapper around zevent)
├── bin/zpromise        (uses zstate + zevent)
└── bin/zheap-death     (uses zstate + zevent)

bin/zvalidate           (standalone - validates commits)
bin/zcheck              (standalone - checks installation)
bin/test-zevent-system  (uses all z* scripts)
```

## External Dependencies

- `git` - For repository operations
- `jq` - For JSON processing
- `bash` - POSIX-compatible shell

All scripts include `set -e` for safety.

## Permissions

All scripts are executable (`chmod +x`):

```bash
-rwxr-xr-x  bin/zstate
-rwxr-xr-x  bin/zevent
-rwxr-xr-x  bin/zjoin
-rwxr-xr-x  bin/zvote
-rwxr-xr-x  bin/zstuff
-rwxr-xr-x  bin/zpass
-rwxr-xr-x  bin/zpromise
-rwxr-xr-x  bin/zheap-death
-rwxr-xr-x  bin/zvalidate
-rwxr-xr-x  bin/zcheck
-rwxr-xr-x  bin/test-zevent-system
```

## Git Configuration

No special git configuration required. System uses:

- `git log` - Read commit history
- `git commit` - Create commits
- `git tag` - Tag releases
- `git branch` - Manage cycles
- `git notes` - Attach metadata
- `git push` - Persist to remote

## Next Steps

See `ZEVENT-README.md` for complete usage guide.

See `ZEVENT-QUICKSTART.md` for quick command reference.

See `ZEVENT-IMPLEMENTATION.md` for implementation details.

See `DESIGN-git-native-events.md` for design rationale.
