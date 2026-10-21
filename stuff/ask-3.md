# ask-3: does an M-of-N threshold over a window replace guardian turns and grace rules?

**Answer.** Partly. An M-of-N threshold with a window removes the *per-guardian turn limit*. There are no turns, so a thief gains nothing by making any one guardian unreachable: up to N−M missing guardians cost the recovery nothing. It does **not** remove the *grace rules*. Their job moves from each guardian's turn to the approval window as a whole. The window is now the thing an outage has to outlast. A thief who keeps more than N−M−k honest guardians unreachable for one window (k = guardians the thief holds) makes that attempt fail. That costs one window per attempt, the same bound our cycle-61 cap gave per pass. Fewer than M guardians do not let a thief take the wallet. What they buy depends on who holds the veto. If the owner key can veto, the key alone lets a thief block every recovery for as long as they like, and the k guardians add nothing. If only guardians can veto, or the key cannot veto, k guardians mainly buy blocking power: withholding k approvals means the thief needs to suppress only (N−k)−M+1 honest guardians, not N−M+1. With k > N−M they need to suppress none.

## Reasoning

- **Turns vs. threshold.** Our rules assumed guardians act one after another, so each unreachable guardian added a wait. That is why we capped total waiting at one turn limit per pass. With M-of-N, every guardian can act at once in the same window. One slow guardian is just one of the N−M you can do without, so there is no turn left to cap.
- **The grace rules still apply, to the window.** Rule 1 (floor = 2 × 30-day p99 ordinary outage, set only by roster vote, never shortened while frozen) carries over directly as a floor on the *approval window*. Rule 2 (count an outage only when signed probes fail *and* a second roster member reached the guardian over a second path) still matters: it stops a thief from inflating the p99 with fake outages to stretch the window. Without these, a short window lets ordinary outages sink honest recoveries, and a window the thief can lengthen while the key is frozen becomes the freeze.
- **Thief with key + k < M guardians, by lever:**
  1. *Executing a handover:* not possible. They still need M−k honest approvals.
  2. *Blocking an honest recovery:* withhold k approvals and make the remaining slack ((N−k)−M+1 honest guardians) unreachable for the window. stuff/thief-outage-induction-model.md covers the inducing side: a shared network provider, under 30 days of data, and guardians kept reachable only from the observer.
  3. *Veto:* if the current owner key holds the timelock veto, a thief holding that key can veto forever. That beats every threshold, and the fix is that a veto signed by the key under recovery cannot block that recovery.
  4. *Repeat attempts:* each failed window costs the honest side one window. Whether a new attempt can start straight away decides whether this is a delay or a stall.

## Unsure, and what would settle it

- I have not read github.com/dngr2/social-recovery. Its code would settle **who can veto** (owner key, guardians, or both), **whether a failed or vetoed recovery can restart straight away**, and **whether guardian approvals carry over between windows**. Points 3 and 4 above depend on all three.
- I don't know whether the window length can be changed while a recovery is pending. If it can, the never-shortened-while-frozen part of rule 1 is needed there too.
- This cycle's rules were written for turn-based guardians. Using them for the window is my reading, not something the roster voted on.
