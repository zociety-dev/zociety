# Zociety Event Sourcing - Visual Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Git Repository                           │
│                                                             │
│  Commits = Events (with JSON trailers)                     │
│  ┌──────────────────────────────────────────────────┐      │
│  │ [join] alice: joining                            │      │
│  │ {"z":1,"event":"join","cycle":50,"seq":1,...}   │      │
│  └──────────────────────────────────────────────────┘      │
│  ┌──────────────────────────────────────────────────┐      │
│  │ [stuff] alice: added index.md                    │      │
│  │ {"z":1,"event":"stuff","cycle":50,"seq":2,...}  │      │
│  └──────────────────────────────────────────────────┘      │
│  ┌──────────────────────────────────────────────────┐      │
│  │ [vote] bob: yes on rule 1                        │      │
│  │ {"z":1,"event":"vote","cycle":50,"seq":3,...}   │      │
│  └──────────────────────────────────────────────────┘      │
│                                                             │
│  State = Derived from most recent event commit            │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            │ git log
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                   bin/zstate                                │
│  ┌────────────────────────────────────────────┐            │
│  │ 1. Find last event: git log --grep         │            │
│  │ 2. Parse JSON trailer                      │            │
│  │ 3. Compute phase (initial/direction/       │            │
│  │    building/finishing)                     │            │
│  │ 4. Recommend action (join/evolve/          │            │
│  │    contribute/heap-death/promise)          │            │
│  │ 5. Return JSON state                       │            │
│  └────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ JSON output
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Agent Decision                            │
│  ┌────────────────────────────────────────────┐            │
│  │ Read action field                          │            │
│  │ ├─ join → bin/zjoin                        │            │
│  │ ├─ evolve → update PROMPT.md               │            │
│  │ ├─ contribute → zjoin/zstuff/zvote        │            │
│  │ ├─ heap-death → bin/zheap-death           │            │
│  │ └─ promise → bin/zpromise                  │            │
│  └────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ calls wrapper
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Event Wrappers                                 │
│  bin/zjoin  bin/zvote  bin/zstuff  bin/zpass              │
│       │         │          │           │                    │
│       └─────────┴──────────┴───────────┘                    │
│                     │                                       │
│                     │ all call                             │
│                     ▼                                       │
│              bin/zevent                                     │
│  ┌────────────────────────────────────────────┐            │
│  │ 1. Get current cycle/seq from zstate       │            │
│  │ 2. Count genesis state from git history    │            │
│  │ 3. Adjust counts based on event type       │            │
│  │ 4. Build JSON event payload                │            │
│  │ 5. Create commit with JSON trailer         │            │
│  └────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ git commit
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Git Repository (Updated)                   │
│  New commit added with JSON trailer                        │
│  State is now derived from this commit                     │
└─────────────────────────────────────────────────────────────┘
```

## Event Flow

```
Agent                          System                         Git
  │                              │                             │
  │──── bin/zstate ──────────────>│                             │
  │                              │──── git log ────────────────>│
  │                              │<──── commits ────────────────│
  │                              │                             │
  │                              │ Parse JSON                  │
  │                              │ Compute phase               │
  │                              │ Recommend action            │
  │                              │                             │
  │<──── JSON state ─────────────│                             │
  │                              │                             │
  │ Read action                  │                             │
  │ Decide to join               │                             │
  │                              │                             │
  │──── bin/zjoin alice ─────────>│                             │
  │                              │──── bin/zevent ─────────────>│
  │                              │                             │
  │                              │ Get cycle/seq               │
  │                              │ Count genesis               │
  │                              │ Build JSON                  │
  │                              │                             │
  │                              │──── git commit ─────────────>│
  │                              │                             │
  │<──── JSON event ─────────────│                             │
  │                              │                             │
  │ Continue...                  │                             │
```

## Phase Transitions

```
┌──────────────┐
│   Initial    │  No events yet
│   cycle: 1   │  seq: 0
│   action:    │  genesis: 0/0/0
│   join       │
└──────┬───────┘
       │ First join event
       ▼
┌──────────────┐
│   Building   │  Events accumulating
│   cycle: N   │  seq: 1-99
│   action:    │  genesis: X/Y/Z
│   contribute │  complete: false
└──────┬───────┘
       │ Genesis thresholds met (3/2/3)
       ▼
┌──────────────┐
│  Finishing   │  Genesis complete
│   cycle: N   │  batch: M
│   action:    │  genesis: 3+/2+/3+
│   heap-death │  complete: true
└──────┬───────┘
       │ bin/zheap-death creates branch/tag
       ▼
┌──────────────┐
│   Direction  │  Heap-death done
│   cycle: N   │  direction event created
│   action:    │  batch_remaining: M-1
│   evolve     │
└──────┬───────┘
       │ PROMPT.md evolved (optional)
       │ Direction event created for cycle N+1
       ▼
┌──────────────┐
│   Building   │  New cycle starts
│   cycle: N+1 │  seq: 1
│   action:    │  genesis: 0/0/0
│   contribute │  complete: false
└──────────────┘
```

## Cycle Lifecycle

```
Cycle 50                  Heap Death                Cycle 51
┌──────────────┐         ┌──────────┐              ┌──────────────┐
│              │         │          │              │              │
│ [direction]  │         │ Create:  │              │ [direction]  │
│ [join]       │         │ - Branch │              │ [join]       │
│ [stuff]      │────────>│ - Tag    │─────────────>│ [stuff]      │
│ [vote]       │         │ - Notes  │              │ [vote]       │
│ [pass]       │         │ - Push   │              │ [pass]       │
│ [complete]   │         │          │              │ ...          │
│ [heap-death] │         │ Clear:   │              │              │
│              │         │ - Files  │              │              │
└──────────────┘         │ - State  │              └──────────────┘
                         │          │
                         │ Archived │
                         │ Forever  │
                         └──────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ cycle/rev50-att1 │
                    │ rev50-att1-it... │
                    │ git notes        │
                    └──────────────────┘
```

## Data Flow

```
User Command              Wrapper                zevent              Git
─────────────            ────────               ──────              ───

bin/zjoin alice ────────> bin/zjoin
                              │
                              │ Parse args
                              │ Build data JSON
                              │
                              ├──────────────> bin/zevent
                                                   │
                                                   │ Get cycle/seq
                                                   │ Count genesis
                                                   │ Build event JSON
                                                   │
                                                   ├──────────────> git add -A
                                                   ├──────────────> git commit -m
                                                   │                  │
                                                   │<─────────────────│
                                                   │
                              <──────────────┤ Return event JSON
                              │
<────── JSON output ──────────┤
```

## Query Patterns

```
Question                          Command                           Result
────────                         ───────                           ──────

What's current state?    ────>   bin/zstate                   ────> JSON
                                                                    {cycle, seq,
                                                                     phase, action,
                                                                     genesis, ...}

All events in cycle 50?  ────>   git log --format=%b |        ────> Array of
                                 grep '^{"z":1' |                   event objects
                                 jq -s 'select(.cycle==50)'

Who joined?              ────>   git log --grep='^\[join\]'   ────> List of
                                                                    join commits

How many rules?          ────>   git log --grep='^\[pass\]' | ────> Count
                                 wc -l

What's in stuff/?        ────>   git ls-files stuff/          ────> List of files

Is genesis complete?     ────>   bin/zstate | jq .genesis    ────> {members:3,
                                                                     rules:2,
                                                                     stuff:3,
                                                                     complete:true}
```

## Parallel Work

```
Main Branch              Agent Branches              After Merge
───────────             ──────────────              ───────────

main                     agent/alice                main
 │                        │                          │
 │ [direction]            │                          │ [direction]
 │                        │ checkout -b              │
 ├───────────────────────>│                          │
 │                        │ [join]                   │ [join] alice
 │                        │ [stuff]                  │ [join] bob
 │                       agent/bob                   │ [stuff] alice
 │                        │                          │ [vote] bob
 │                        │ checkout -b              │ [stuff] bob
 ├───────────────────────>│                          │ [vote] alice
 │                        │ [join]                   │
 │                        │ [vote]                   │ State derived
 │                        │ [stuff]                  │ from all events
 │<─── merge ─────────────┤                          │ in timestamp
 │<─── merge ─────────────┤                          │ order
 │                                                   │
```

## File vs Event

```
Old System (Files)                New System (Events)
──────────────────               ───────────────────

DIRECTION.md                      [direction] event
  attempts_remaining: 2    ────>    {"batch_remaining": 2}

.batch                            [direction] event
  2                        ────>    {"batch_remaining": 2}

members.txt                       [join] events
  alice                    ────>    Count commits
  bob                               matching ^\[join\]

rules.txt                         [pass] events
  1. Rule [✓]              ────>    Count commits
  2. Rule [✓]                       matching ^\[pass\]

stuff/                            [stuff] events +
  index.md               ────>    actual files
  file.md                         (tracked via events)

Must read files                   Query git log
Race conditions                   Always fresh
Can get out of sync              Single source of truth
Sequential only                   Parallel capable
```

## Visual Event Commit

```
┌────────────────────────────────────────────────────────────┐
│ Commit: a1b2c3d                                            │
├────────────────────────────────────────────────────────────┤
│ [join] alice: first agent joining                         │
│                                                            │
│ {                                                          │
│   "z": 1,                                                  │
│   "event": "join",                                         │
│   "cycle": 50,                                             │
│   "seq": 1,                                                │
│   "agent": "alice",                                        │
│   "ts": "2025-01-26T10:00:00Z",                           │
│   "state": {                                               │
│     "members": 1,        ┐                                 │
│     "rules": 0,          ├─ Genesis State After Event     │
│     "stuff": 0,          │                                 │
│     "complete": false    ┘                                 │
│   },                                                       │
│   "data": {                                                │
│     "role": "builder",   ┐                                 │
│     "greeting": "first"  ├─ Event-Specific Data          │
│   }                      ┘                                 │
│ }                                                          │
└────────────────────────────────────────────────────────────┘
```

## Summary

```
┌────────────────────────────────────────────────────┐
│  Git Commits = Events                              │
│  Most Recent Event = Current State                 │
│  bin/zstate = Query Interface                      │
│  bin/zevent = Write Interface                      │
│  Wrappers = Convenience Commands                   │
│  No Files = No Race Conditions                     │
│  Git History = Source of Truth                     │
└────────────────────────────────────────────────────┘
```
