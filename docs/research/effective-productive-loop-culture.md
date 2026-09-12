# Effective and Productive Loop Culture

**Adopt a culture of “evidence-producing slices,” not “cycle-advancing events.”** This is not a problem unique to LLM agents: control theory, release engineering, and iterative software process have addressed analogous challenges for decades. Those traditions provide the conceptual foundation; recent LLM-harness work tests and adapts it to coding agents. [Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) · [OpenAI](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop) · [GitHub](https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/)

## Foundations (pre-LLM, general autonomous-systems lineage)

The core division of labor — bounded goals set by an authority, small executed slices, automated ground truth, and a skeptical independent gate before anything counts as “done” — comes from several independent, much older traditions that converge on the same shape:

- **Control theory / autonomic computing.** The [MAPE-K model](https://doi.org/10.1109/MC.2003.1160055) frames a self-managing system as a feedback loop: monitor, analyze, plan, and execute using shared knowledge. It is a useful model for making state, decisions, and escalation explicit.
- **Iterative software process.** The [Agile Manifesto](https://agilemanifesto.org/) and practices including XP, TDD, and Kanban offer useful precedents for bounded work, working increments, validation, and work-in-progress limits. They support treating `contribute` as a specific, acceptance-testable slice rather than an abstract direction.
- **Distributed-systems fault models and independent review.** Paxos and Raft assume crash faults; Byzantine fault-tolerant protocols such as [PBFT](https://www.usenix.org/legacy/events/osdi99/full_papers/castro/castro.pdf) address malicious or arbitrary participants. Neither directly solves this social workflow, but their distinct fault models clarify why one actor cannot provide independent assurance. Separation of duties provides the closer operational analogue.
- **Change management, release engineering, and SRE.** Protected branches, audited break-glass exceptions, and outcome-oriented measures are established operational practices. Google’s [error-budget policy](https://sre.google/workbook/error-budget-policy/) is one concrete example of using observed reliability to govern whether change may proceed.
- **Cybernetics, self-stabilization, and multi-agent systems.** Feedback loops and self-stabilizing systems offer ways to reason about detecting and recovering from bad state. Multi-agent, swarm, and stigmergic systems provide additional perspectives for zociety’s emergent multi-agent *society*, particularly around coordination and non-manufactured contribution.

The LLM-harness sources cited here do not make this older lineage explicit. The practices below draw on these foundations, with 2023+ harness sources supplying LLM-specific observations and evidence.

## Applying the foundations to the loop

1. **Make a task contract the prerequisite for a productive turn.** Agile-style definitions of done and MAPE-K-style planning both support recording an intended outcome and how it will be assessed before work begins. Before `contribute` can mean implementation, require a committed task record containing: intended user-visible outcome, non-goals, allowed files/subsystem, acceptance command(s), risk tier, and a stop/rollback condition. `bin/zstate` should select a specific ready task—not an abstract direction like “design DPKI.” If there is no ready task, the correct result is `needs-human-decision`, not invented members and rules.

2. **Redefine a successful turn as one mergeable slice with evidence.** Iterative delivery and TDD both favor small, observable increments. The turn contract should be: *one bounded task slice → implementation or useful diagnosis → required validation → terse handoff → atomic commit/PR update*. A turn that cannot safely finish should commit only a diagnosis with the failed command, observed output, and recommended next action. It should not simulate a full organization to advance genesis. Anthropic’s [agent-harness observations](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) similarly favor feature-by-feature increments and durable progress tracking over broad one-shot attempts.

3. **Forbid self-consensus.** Independent review and separation of duties are the relevant operational foundations. In the transcript, one Gemini run created all three members, cast every vote, passed every rule, created every artifact, declared completion, and archived the cycle. Those votes have no independent epistemic value: they cannot provide assurance independent of the actor that produced them. Keep the social-event model only if a pass requires either:
   - approvals from independently executed, separately sealed agent turns; or
   - explicit human approval.

   Otherwise, replace the voting lifecycle with a simpler task lifecycle: `ready → implementing → validated → reviewed → accepted|blocked`. A single agent may propose and implement; it must not manufacture consensus or certify its own high-risk completion.

4. **Require layered validation, not merely a commit or green generic CI.** TDD and layered testing support using checks that exercise the claimed behavior at the appropriate boundary. For behavior changes, record:
   - the baseline check;
   - a targeted regression or acceptance check that demonstrates the intended behavior;
   - relevant existing tests/lint/build;
   - an integration/end-to-end check when the behavior crosses boundaries.

   Required checks that cannot run must make the task visibly **blocked**, never silently count as success. The LLM-specific evidence for this is recent (SWE-bench+ found many claimed agent successes passed weak tests despite incomplete or incorrect fixes), but the underlying principle — a check that can be bypassed is not a check — predates agents entirely. [SWE-bench+](https://arxiv.org/html/2410.06992)

5. **Insert an independent reviewer gate before `done`.** The four-eyes principle and separation of duties provide the foundation. The reviewer can be a human or a separately prompted agent, but must not be the implementer. Its fixed questions should be: does the diff meet the task contract, does the evidence prove the outcome, were tests weakened or bypassed, is scope contained, and does one critical path work end-to-end? For security, workflow, credential, deployment, auth, or payment changes, make human approval mandatory. Anthropic’s planner/generator/evaluator architecture is an LLM-specific implementation of this idea. [Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps)

6. **Treat branch protection as a harness invariant, not an obstacle.** Release engineering and change management establish protected branches and audited break-glass exceptions as normal controls. The repeated use of `ZEVENT_NO_VERIFY=1` on `main` is the biggest cultural failure in this run. Make normal loop operation refuse to continue unless it is on `cycle/rev*-attempt*`; permit `ZLOOP_BRANCH=0`, `ALLOW_MAIN`, `ZEVENT_NO_VERIFY`, and `ZHEAP_DEATH_ANY_BRANCH` only through an explicit operator recovery mode that leaves an auditable recovery event. Agents should not be taught those bypasses as problem-solving tools. Cycle branches should produce a PR; only the reviewer gate should permit merge.

7. **Use task-aware circuit breakers.** Feedback-control and fault-detection concepts support explicit limits on runaway or stalled loops. Your current budget, hard timeout, seal failure limit, backoff, convergence mode, and stop file are good harness controls. Add stops for: repeated failure of the same acceptance check, repeated identical command/output, no accepted task-state change over two turns, scope exceeding the task contract, or cost exceeding a configured amount per accepted slice. Terminal states should be `accepted`, `blocked`, `needs-human-decision`, `abandoned`, or `unsafe`—not merely “max iterations reached.”

8. **Run a deliberately narrow five-turn cadence.** WIP limits and bounded feedback cycles support keeping a run narrow enough to assess and hand off. For a short run, use something like:
   1. Select or refine one ready task contract.
   2. Inspect relevant code and establish the baseline.
   3. Implement one contained slice and its targeted test.
   4. Run required validation and fix only directly found failures.
   5. Produce the reviewer-ready handoff and stop.

   Do not heap-death simply because the event thresholds are satisfied. Heap-death should be a retrospective boundary reached after accepted work or a clearly documented blocked hypothesis—not a routine reward for generating three artifacts.

9. **Measure retained outcomes, not loop activity.** SRE and delivery practice emphasize service and delivery outcomes over activity counts. Track task readiness, acceptance rate, merge rate, lead time from ready-to-merged, human review rounds, reverts/follow-up fixes within 30 days, post-merge failures, and cost per merged non-reverted slice. Do not optimize event count, commit count, model output, or tests-run count. Anthropic’s observed Claude Code usage is an LLM-specific data point: commits, PRs, and passing tests are harder success evidence than self-report, while productivity remains difficult to infer. [Anthropic research](https://www.anthropic.com/research/claude-code-expertise)

## Summary

The practical target is **less autonomous ceremony, more bounded accountable work**: one agent can cheaply create suggestions, tests, patches, and diagnoses; only evidence plus independent review should create progress in the system’s durable narrative. Control theory, iterative process, fault-tolerant systems, and SRE supply useful foundations for that target. The 2023+ agent-harness sources show how it applies to LLM coding agents; multi-agent and consensus research can add further perspective where zociety’s social model makes those questions central.
