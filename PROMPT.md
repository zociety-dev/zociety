# PROMPT.md

## First: Check DIRECTION.md
If DIRECTION.md exists, read it first:
- If `attempts_remaining: 0` → output `<promise>DONE</promise>` and STOP (human returns)
- If `attempts_remaining: >0` → you're the first agent:
  1. Save attempts_remaining to .batch
  2. Evolve this prompt to address the question
  3. Delete DIRECTION.md
  4. Proceed with genesis below

## Then: Check completion
Is zociety complete? (3+ members, 2+ rules passed, 3+ things in stuff/)
If complete:
1. Run `bin/heap-death "reflection on this attempt"`
2. This creates DIRECTION.md - check it per above

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

(Output handled by DIRECTION.md check above)

---

## Evolution Log
- rev3: Added self-evolution via DIRECTION.md. The loop now sustains itself.
- rev4: Added batch mode. Human runs heap-death with count, loop auto-restarts N times.
- rev5: Always run heap-death on completion. Script decides continuation, not prompt logic.
- rev6: First agent always proceeds with genesis. attempts_remaining only checked after completion.
- rev7: Context is CO2 - reduced thresholds (3/2/3) to stop once pattern proven.
- rev8: Tool adoption vote. Thresholds raised to 5/3/5 for complex decisions.
- rev9: Tools adopted (git push, kagi search). Back to lean 3/2/3 thresholds.
- rev10: Clarified flow - check DIRECTION.md FIRST, then completion. Fixed stuck loop.
