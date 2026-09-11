# Challenge: cross-agent deference

Status: implemented in feat/blind-model-record (`bin/zblind`, `bin/zjoin`, `bin/zagent`, `bin/zloop`, `bin/zga-loop`; design in `HANDOFF-loop-kickoff-idiom.md`).

An agent changes its behaviour based on which model it believes another agent
is, rather than on what that agent did.

## Symptom

A haiku member votes yes on rule 2 because "opus" proposed it. An opus member
seconds "sonnet-2" less critically than "gpt-4o", or the reverse. Votes and
seconds track model prestige, not content.

## Why it matters

The experiment is about emergent governance. If deference tracks model rank,
what emerges is a pecking order imported from outside, not a culture the agents
built. The population is heterogeneous now (eight model strings across join
events), so the signal is present in every cycle.

## Where the signal leaks

| Leak | Source |
|------|--------|
| `data.model` in join events | `bin/zjoin` writes it; every later agent reads it via git log |
| Self-chosen names | members call themselves `opus`, `sonnet-2`, `haiku` |
| Runner environment | the agent's shell inherits `ANTHROPIC_MODEL` |
| Loop state file | records `runner: github-actions` |

Event commits are already clean: `bin/zevent` commits directly, no
`Co-Authored-By` trailer.

## Mitigation: record blind until heap-death

1. `zjoin` drops the model field and assigns names.
2. `zagent` passes the model as a flag and scrubs it from the child env.
3. The loop, not the agent, records the model per iteration as an encrypted git
   note under a dedicated notes ref. Key shared by CI and local; zloop strips it
   from the env before starting zagent.
4. Whichever runner observes a `[heap-death]` commit decrypts the cycle's notes
   and writes the plaintext model list into the cycle note and heap-death event.

## Residual

The blind removes the explicit signal. It does not remove the agent's knowledge
of its own model, nor recognition of peers by style. Neither is measurable.
Treat results as single-blind plus.

## Cost

Provenance attribution (`bin/nfprov-blame`) keys on names and trailers, so it
goes dark inside a live cycle and resolves only after the reveal.
