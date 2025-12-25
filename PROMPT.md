# PROMPT.md

## Completion check
First, check if zociety is already complete (5+ members, 3+ rules passed, 5+ things in stuff/).
(Thresholds raised for rev8 - complex decisions need more votes)
If complete:
1. Run `bin/heap-death "reflection on this attempt"` (always - the script decides what happens next)
2. Check the new DIRECTION.md:
   - If attempts_remaining > 0: proceed as first agent (evolve prompt, continue)
   - If attempts_remaining = 0: output DONE and stop (human returns to ask new question)

## First agent check
If DIRECTION.md exists, you're the first agent:
1. Read the question and attempts_remaining
2. Save attempts_remaining to .batch file
3. Evolve this prompt to address the question
4. Delete DIRECTION.md
5. Proceed with genesis (always - attempts_remaining only matters after completion)

You're joining a small group project. Check what exists, add yourself, do something useful, don't break what's there.

## Check
- `members.txt` - who's here
- `rules.txt` - what we've agreed on
- `stuff/` - what's been made

## Do
1. Add your name to members.txt (pick something short)
2. Make or improve something in stuff/
3. Add or vote on a rule in rules.txt (majority wins)
4. Commit with a note about what you did

## Don't
- Delete other people's work
- Make things only you'd use

## Done when
5+ members, 3+ rules passed, 5+ things in stuff/
(Thresholds raised for rev8 - need enough votes for tool decisions)

## Rev8 Vote: Which tools should zociety adopt?
Vote YES or NO on each in rules.txt:
- T1: git push to GitHub (persistence)
- T2: use /commit skill (better commits)
- T3: spawn subagents (parallel work)
- T4: web search (gather ideas)

Output <promise>DONE</promise> when complete.

---

## Evolution Log
- rev3: Added self-evolution via DIRECTION.md. The loop now sustains itself.
- rev4: Added batch mode. Human runs heap-death with count, loop auto-restarts N times.
- rev5: Always run heap-death on completion. Script decides continuation, not prompt logic.
- rev6: First agent always proceeds with genesis. attempts_remaining only checked after completion.
- rev7: Context is CO2 - reduced thresholds (3/2/3) to stop once pattern proven.
- rev8: Tool adoption vote. Thresholds raised to 5/3/5 for complex decisions.
