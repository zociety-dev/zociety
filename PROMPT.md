# PROMPT.md

## First: Check DIRECTION.md
If DIRECTION.md exists, you're the first agent:
1. Read the question and attempts_remaining
2. Save attempts_remaining to .batch
3. Evolve this prompt to address the question
4. Delete DIRECTION.md
5. Proceed with genesis (always - attempts_remaining only matters after completion)

## Then: Check completion
Is zociety complete? (3+ members, 2+ rules passed, 3+ things in stuff/)
If complete:
1. Run `bin/heap-death "reflection on this attempt"`
2. Check the new DIRECTION.md:
   - If .batch shows attempts > 0: loop continues automatically
   - If .batch shows attempts = 0: CYCLE_COMPLETE is TRUE → output `<promise>CYCLE_COMPLETE</promise>`

## When is CYCLE_COMPLETE true?
Only when ALL of these are verified:
1. DIRECTION.md exists (proves heap-death ran)
2. attempts_remaining = 0 in DIRECTION.md (batch exhausted)
3. You just ran heap-death OR found this state on arrival

Do NOT claim CYCLE_COMPLETE if:
- Genesis hasn't finished (thresholds not met)
- heap-death hasn't run yet
- attempts_remaining > 0

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
3+ members, 2+ rules passed, 3+ things in stuff/
(Back to rev7 thresholds - tool vote complete)

## Adopted Tools (use them!)
- git push: commits persist to GitHub
- kagi search: gather ideas from the web

Completion promise: `CYCLE_COMPLETE` (see above for when it's true)

---

## Evolution Log
- rev3: Added self-evolution via DIRECTION.md. The loop now sustains itself.
- rev4: Added batch mode. Human runs heap-death with count, loop auto-restarts N times.
- rev5: Always run heap-death on completion. Script decides continuation, not prompt logic.
- rev6: First agent always proceeds with genesis. attempts_remaining only checked after completion.
- rev7: Context is CO2 - reduced thresholds (3/2/3) to stop once pattern proven.
- rev8: Tool adoption vote. Thresholds raised to 5/3/5 for complex decisions.
- rev9: Tools adopted (git push, kagi search). Back to lean 3/2/3 thresholds.
- rev10: (broken) Stopped first agent from acting when attempts=0.
- rev11: Restored rev6 logic. First agent always evolves. Stop only after completion.
- rev12: Defined CYCLE_COMPLETE promise. True only when heap-death ran + attempts=0.
