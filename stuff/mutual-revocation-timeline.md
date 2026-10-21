# Mutual-revocation timeline: one key through rules 1 and 2

This walks one key, position by position, from mutual revocation to a working
replacement key. It checks whether rules 1 and 2 work together when the owner
is honest and a thief is also active.

## Setup

- Key K has co-signers A and B, and outside guardians G1, G2 and G3, named
  when K was created. The quorum is 2 of 3. The public delay is N = 5.
- The thief holds K and B's signing key. A is honest.

## Timeline

| pos | event | effect |
|-----|-------|--------|
| 0 | B (the thief) revokes A; A counter-revokes B | mutual revocation, so K is frozen |
| 1 | thief steals G1's vouching key and issues a vouch for K' (thief's key) | 1 of 2 vouches, nothing happens yet |
| 2 | G2 vouches for K'' (A's new key) | 1 vouch for K'', 1 for K' |
| 3 | G3 vouches for K'' | quorum for K''; rule 1's delay starts (ends at 8) |
| 4 | thief, as B, vetoes the K'' unfreeze | **unfreeze cancelled** under rule 1 |
| 5 | G1 notices and disowns the K' vouch | the K' vouch is dead under rule 2 |

## What this shows

1. **Rule 2 stops the stolen vouch.** The thief's G1 vouch names K', and it
   can never be combined with G2 and G3's vouches for K''. A stolen vouch
   cannot be counted toward a different replacement key.
2. **Rule 1 lets the thief stall.** B is an "original co-signer", so the
   thief's veto at position 4 is valid. Each new honest attempt can be vetoed
   again. This is the same spite-veto gap that guardian-loss-walkthrough.md
   found, but here the thief is the one using it.
3. **Order matters.** If G1 had not disowned the vouch and G2 had vouched for
   K' instead, the thief would have had a quorum for K'. A could then use the
   same veto to stop it. The two vetoes cancel each other out, so the key
   stays frozen.

## Open question for the next rule

Whenever a co-signer is stolen, the veto is symmetric: either side can block
the other indefinitely. Two possible fixes:

- **Veto costs a guardian's vouch.** A veto only counts if at least one named
  guardian co-signs it. The thief then has to steal a second guardian key,
  not just B, to stall.
- **Veto names its alternative.** A veto must name a competing replacement
  key that already has at least one guardian vouch. If no such key exists, the
  veto lapses at the end of the delay.

Both make the veto cost the thief something it does not already hold.
