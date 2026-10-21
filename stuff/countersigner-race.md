# Countersigner race: what the thief needs to move a cutoff

Rules 1 and 2 leave one way to drag a key's cutoff earlier: the thief must
hold a second key with no countersigned revocation before the forgery. This
file checks what that costs and whether the strata stay two-valued.

## Setup

Keys A (honest, stolen) and B (also stolen, still unrevoked). Commit log:

| pos | event                                   |
|-----|-----------------------------------------|
| 1   | A signs cut c1                          |
| 2   | thief forges revoke(A), countersigned by B |
| 3   | A signs cut c2 (honest owner, unaware)  |
| 4   | honest revoke(A), countersigned by C    |

## Outcome

- Rule 2: B has no countersigned revocation before pos 2, so B's
  countersignature counts. A's first countersigned revocation is pos 2.
- Rule 1: rescue restores c1 (pos 1 < 2) and drops c2 (pos 3 > 2).
  The thief moved the cutoff from 4 to 2 and denied c2.
- Each stratum is still a single split at one log position: everything
  before is restored, everything after is not. Monotone, two-valued.

## Race

The forgery also burns B's usefulness only if someone revokes B. Once
revoke(B) is countersigned at pos p, rule 2 voids every countersignature B
makes after p, but not the one at pos 2. So the honest side wins only by
revoking B *before* the forgery lands: it is a race on log position, and
pos 2 < pos of revoke(B) means the thief keeps the gain.

## Takeaway

Countersigning a revocation raises the price from one stolen key to two
unrevoked stolen keys, but does not make the cutoff unforgeable. A
retroactive rule (void B's countersignatures once B is shown to have been
stolen earlier) would break the "single position" property, since a later
event would then move an earlier cutoff back out.
