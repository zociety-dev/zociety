# Liveness-probe skip schedule

How rules 1 and 2 fit together when a pass reaches a guardian who does not answer.

## Per guardian (rule 1)

1. When the turn opens, send a signed liveness probe that includes a nonce and the pass id.
2. Re-probe at fixed intervals across a grace window G. Do not skip on the first miss.
3. If a signed answer arrives within G, the guardian keeps the turn with the normal limit L.
4. If every probe in G goes unanswered, mark the guardian *skipped*. The guardian keeps their seat. A signed answer later puts them back in their place in the rotation.

## Per pass (rule 2)

- Keep a budget B = L for the pass. Each grace window spent on a guardian who ends up skipped is subtracted from B.
- When B reaches 0, no further guardians are probed and waited on in this pass. Each one left is queued, and the next pass probes them first.
- The longest a thief can stall one pass is about L + G: one full budget plus the window already running. The worst case is no longer L × roster size.

## Why an honest guardian who is briefly offline is safe

- One missed probe never costs a turn, because of the grace window.
- Being queued does not skip the guardian. They are probed first in the next pass.
- When they answer, they get their turn back. Being offline for a while delays their turn but does not remove it.

## Open questions

- Should G scale with how often a guardian has been reachable before? A thief could use that to push G longer.
- Queued guardians could build up over many passes if the thief keeps cutting them off. Is a cap on the queue length needed?
