# PROMPT.md

## Auto-restart check
First, check if zociety is already complete (7 members, 5 rules, 7 things in stuff/).
If complete, check .batch file:
- If .batch exists and attempts_remaining > 0: run bin/heap-death with the question and decremented count, then proceed as first agent
- If .batch exists and attempts_remaining = 0: output DONE and stop (human returns)
- If no .batch: output DONE and stop

## First agent check
If DIRECTION.md exists, you're the first agent:
1. Read the question and attempts_remaining
2. Save attempts_remaining to .batch file
3. Evolve this prompt to address the question
4. Delete DIRECTION.md
5. Proceed

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
7 members, 5 rules, 7 things in stuff/

Output <promise>DONE</promise> when complete.

---

## Evolution Log
- rev3: Added self-evolution via DIRECTION.md. The loop now sustains itself.
