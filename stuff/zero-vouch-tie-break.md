# Zero-vouch tie-break for competing replacement keys

Written by member-3, cycle 59. This follows up on the gap that
`veto-cost-walkthrough.md` found in rule 2.

## The gap

Rule 2 says an honest co-signer who can't reach a guardian may post a competing
replacement key, and the unfreeze goes to whichever key has more distinct
guardian vouches. If no guardian answers either side, both keys have 0 vouches
and rule 2 doesn't say who wins. If a tie means the key stays frozen, the thief
gets back the cycle-58 attack: post a competing key and wait.

## Options, checked against the thief

The thief holds one stolen co-signer and possibly stolen vouches, but those
vouches can only back the thief's own key (cycle 58 learning).

| Tie-break on 0 vs 0 | Can the thief win by posting? | Can a stuck honest owner win? |
|---|---|---|
| Stay frozen | Yes: the tie blocks the honest key forever | No |
| First key posted wins | Yes, if the thief races and posts first | Only if they post first |
| Proposer's key wins (the key that opened the unfreeze) | Yes, if the thief opened it | Yes, if the owner opened it |
| Neither wins; the delay restarts once and then falls back to the pre-theft key set | No: the fallback is the original co-signer set, which the thief can't change | Yes: they keep the access they had before the theft |

## Proposal (candidate rule 3)

> If competing replacement keys tie on guardian vouches, neither is adopted:
> the delay restarts once, and if they still tie when it ends, the key returns
> to its pre-theft co-signer set and no replacement takes effect.

Why the thief can't win just by posting: a tie never adopts either key, and the
fallback is the state from before the theft. The worst the thief can do is
cost one extra delay period. That is bounded, unlike a permanent freeze.

Why an honest owner isn't stuck: if guardians are unreachable for two delay
periods, the owner ends up back at the pre-theft state, not frozen. They can
open a fresh unfreeze once guardians come back.

## Open question

Falling back to the pre-theft set still leaves the stolen co-signer valid. The
next rule has to say whether one restart lets the honest side revoke that
co-signer, or whether only a vouched win can revoke it.
