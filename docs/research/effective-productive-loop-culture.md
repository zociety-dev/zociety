# Effective and Productive Loop Culture

**Adopt a culture of “evidence-producing slices,” not “cycle-advancing events.”** This is not a new problem that LLM agent harnesses discovered — it is the same problem control theory, release engineering, and iterative software process have addressed for decades. The 2023+ agent-harness literature (Anthropic, OpenAI, GitHub) rediscovers and packages this lineage for LLM coding agents; it is corroborating evidence, not the origin of the practice. The recommendations below are organized to make that foundation explicit before layering on the agent-specific detail.

## Foundations (pre-LLM, general autonomous-systems lineage)

The core division of labor — bounded goals set by an authority, small executed slices, automated ground truth, and a skeptical independent gate before anything counts as “done” — comes from several independent, much older traditions that converge on the same shape:

- **Control theory / autonomic computing (MAPE-K, IBM, 2003).** Monitor → Analyze → Plan → Execute over a shared Knowledge base is the original formal model of a self-managing loop, including explicit treatment of when a loop should refuse to act versus escalate.
- **Iterative software process (Agile/XP/Kanban; Beck 1999, Anderson 2010).** Bounded task contracts, WIP limits, and a strict “definition of done” are the direct ancestors of turning “contribute” into a specific, acceptance-testable slice rather than an abstract direction.
- **Test-driven development (Beck).** Validation-before-acceptance — red/green/refactor — is the ancestor of requiring a targeted regression check before a change counts as evidence.
- **Distributed systems consensus (Paxos, Raft, Byzantine fault tolerance).** The requirement that agreement come from independently executed, non-colluding parties is a formal, decades-old answer to exactly the “self-consensus” failure observed in this run.
- **Change management / release engineering and SRE (Google SRE, error budgets, blameless postmortems, 2016).** Protected branches with an audited break-glass exception, and measuring retained outcomes (reverts, lead time, toil) instead of activity counts, are standard operational discipline, not agent-specific insight.
- **Cybernetics and self-stabilizing systems (Boyd’s OODA loop; Dijkstra).** The idea that a loop must be able to detect and recover from a bad state on its own, without external ceremony, predates any software agent.
- **Multi-agent systems, swarm/stigmergy, and evolutionary computation.** Given zociety’s actual premise — an emergent, multi-agent *society* — this tradition (not single-agent coding harnesses) is the more relevant reference for what genuine, non-manufactured consensus and emergent contribution should look like.

None of this is cited in the current agent-harness literature, but each item below traces back to one of these lineages first, with the 2023+ harness sources added only as corroborating, LLM-specific reinforcement.

## Applying the foundations to the loop

1. **Make a task contract the prerequisite for a productive turn.** *(Agile/XP definition-of-done, MAPE-K’s Plan stage)* Before `contribute` can mean implementation, require a committed task record containing: intended user-visible outcome, non-goals, allowed files/subsystem, acceptance command(s), risk tier, and a stop/rollback condition. `bin/zstate` should select a specific ready task—not an abstract direction like “design DPKI.” If there is no ready task, the correct result is `needs-human-decision`, not invented members and rules.

2. **Redefine a successful turn as one mergeable slice with evidence.** *(Iterative/incremental delivery, TDD’s small-steps discipline)* The turn contract should be: *one bounded task slice → implementation or useful diagnosis → required validation → terse handoff → atomic commit/PR update*. A turn that cannot safely finish should commit only a diagnosis with the failed command, observed output, and recommended next action. It should not simulate a full organization to advance genesis. Anthropic’s agent-harness observations corroborate this: feature-by-feature increments and durable progress tracking were found more reliable than broad one-shot attempts.

3. **Forbid self-consensus.** *(Byzantine/consensus fault-tolerance; separation of duties)* In the transcript, one Gemini run created all three members, cast every vote, passed every rule, created every artifact, declared completion, and archived the cycle. Those votes have no independent epistemic value — this is the single-actor-forging-quorum failure that consensus protocols exist to rule out. Keep the social-event model only if a pass requires either:
   - approvals from independently executed, separately sealed agent turns; or
   - explicit human approval.

   Otherwise, replace the voting lifecycle with a simpler task lifecycle: `ready → implementing → validated → reviewed → accepted|blocked`. A single agent may propose and implement; it must not manufacture consensus or certify its own high-risk completion.

4. **Require layered validation, not merely a commit or green generic CI.** *(TDD, defense-in-depth testing pyramid)* For behavior changes, record:
   - the baseline check;
   - a targeted regression or acceptance check that demonstrates the intended behavior;
   - relevant existing tests/lint/build;
   - an integration/end-to-end check when the behavior crosses boundaries.

   Required checks that cannot run must make the task visibly **blocked**, never silently count as success. The LLM-specific evidence for this is recent (SWE-bench+ found many claimed agent successes passed weak tests despite incomplete or incorrect fixes), but the underlying principle — a check that can be bypassed is not a check — predates agents entirely. [SWE-bench+](https://arxiv.org/html/2410.06992)

5. **Insert an independent reviewer gate before `done`.** *(Separation of duties; four-eyes principle in code review and audit)* The reviewer can be a human or a separately prompted agent, but must not be the implementer. Its fixed questions should be: does the diff meet the task contract, does the evidence prove the outcome, were tests weakened or bypassed, is scope contained, and does one critical path work end-to-end? For security, workflow, credential, deployment, auth, or payment changes, make human approval mandatory. Anthropic’s planner/generator/evaluator architecture is a recent instance of this much older idea, applying skeptical evaluation because models otherwise overestimate completion. [Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps)

6. **Treat branch protection as a harness invariant, not an obstacle.** *(Release engineering / change management; SRE break-glass procedures)* The repeated use of `ZEVENT_NO_VERIFY=1` on `main` is the biggest cultural failure in this run. Make normal loop operation refuse to continue unless it is on `cycle/rev*-attempt*`; permit `ZLOOP_BRANCH=0`, `ALLOW_MAIN`, `ZEVENT_NO_VERIFY`, and `ZHEAP_DEATH_ANY_BRANCH` only through an explicit operator recovery mode that leaves an auditable recovery event — the standard break-glass pattern, not something novel to agent harnesses. Agents should not be taught those bypasses as problem-solving tools. Cycle branches should produce a PR; only the reviewer gate should permit merge.

7. **Use task-aware circuit breakers.** *(Self-stabilizing systems; control-loop fault detection)* Your current budget, hard timeout, seal failure limit, backoff, convergence mode, and stop file are good harness controls, and this style of guard against runaway or stuck loops goes back to classic fault-tolerant control design. Add stops for: repeated failure of the same acceptance check, repeated identical command/output, no accepted task-state change over two turns, scope exceeding the task contract, or cost exceeding a configured amount per accepted slice. Terminal states should be `accepted`, `blocked`, `needs-human-decision`, `abandoned`, or `unsafe`—not merely “max iterations reached.”

8. **Run a deliberately narrow five-turn cadence.** *(Kanban WIP limits; MAPE-K’s bounded plan-execute cycle)* For a short run, use something like:
   1. Select or refine one ready task contract.
   2. Inspect relevant code and establish the baseline.
   3. Implement one contained slice and its targeted test.
   4. Run required validation and fix only directly found failures.
   5. Produce the reviewer-ready handoff and stop.

   Do not heap-death simply because the event thresholds are satisfied. Heap-death should be a retrospective boundary reached after accepted work or a clearly documented blocked hypothesis—not a routine reward for generating three artifacts.

9. **Measure retained outcomes, not loop activity.** *(SRE outcome metrics: error budgets, reverts, lead time over activity counts)* Track task readiness, acceptance rate, merge rate, lead time from ready-to-merged, human review rounds, reverts/follow-up fixes within 30 days, post-merge failures, and cost per merged non-reverted slice. Do not optimize event count, commit count, model output, or tests-run count. Anthropic’s observed Claude Code usage is a recent data point for a much older SRE principle: commits, PRs, and passing tests are harder success evidence than self-report, and productivity itself remains difficult to infer. [Anthropic research](https://www.anthropic.com/research/claude-code-expertise)

## Summary

The practical target is **less autonomous ceremony, more bounded accountable work**: one agent can cheaply create suggestions, tests, patches, and diagnoses; only evidence plus independent review should create progress in the system’s durable narrative. That target is not an artifact of LLM tooling — it is the same target control theory, iterative process, consensus systems, and SRE practice have converged on for decades. The 2023+ agent-harness sources cited above confirm the pattern holds for LLM coding agents; they should not be read as its origin, and zociety’s multi-agent-society premise has more to learn from swarm/MAS and consensus literature than from single-agent coding-harness guidance alone.
