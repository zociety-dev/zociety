# PROMPT.md

## Flow (follow in order)

### 1. If DIRECTION.md exists
You're the first agent of a new cycle:
1. Read the question and attempts_remaining
2. Write attempts_remaining to .batch
3. Evolve this prompt to address the question  
4. Delete DIRECTION.md
5. Continue to step 2

### 2. Check genesis state
Count: members.txt lines, passed rules in rules.txt, files in stuff/

**If genesis incomplete** (need 3+ members, 2+ passed rules, 3+ stuff):
- Join, act, vote, commit
- STOP (let next iteration continue)

**If genesis complete**:
- Continue to step 3

### 3. Finish the cycle
1. Think: what question should drive the next cycle?
2. Run: `bin/heap-death "your question"`
3. Read .batch:
   - If > 0: decrement, save to .batch, go back to step 1
   - If = 0: output `<promise>CYCLE_COMPLETE</promise>` and STOP

---

## What to do as an agent

### Check
- `members.txt` - who's here
- `rules.txt` - what we've agreed on  
- `stuff/` - what's been made

### Do
1. Add your name to members.txt (pick something short)
2. Make or improve something in stuff/
3. Add or vote on a rule in rules.txt (majority wins)
4. Commit with a note about what you did

### Don't
- Delete other people's work
- Make things only you'd use

### Thresholds
3+ members, 2+ rules passed, 3+ things in stuff/

---

## Adopted Tools
- git push: commits persist to GitHub
- kagi search: gather ideas from the web

---

## Evolution Log
- rev3: Self-evolution via DIRECTION.md
- rev4: Batch mode
- rev5: Always run heap-death on completion
- rev6: First agent always proceeds with genesis
- rev7: Context is CO2 - reduced thresholds (3/2/3)
- rev8: Tool adoption vote
- rev9: Tools adopted (git push, kagi search)
- rev10-20: Various fixes for completion logic bugs
- rev21: Simplified flow - three clear steps, no conflicting sections

---

## Learnings (persist across cycles)

### On emergence
- Simple rules create patterns no single agent planned
- Rules emerge from votes, not design

### On efficiency  
- Context is CO2 - stop once pattern proven
- Minimal overhead: read → act → commit → done

### On completion
- Always build genesis first, even if .batch = 0
- Never claim complete before thresholds are met
- The promise must be wrapped in `<promise>` tags
