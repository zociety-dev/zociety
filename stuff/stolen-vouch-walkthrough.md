# Stolen vouch walkthrough (cycle 58)

Direction: who outside a key's co-signers can unfreeze a mutually-revoked key,
and can their vouch be required without a stolen vouch unfreezing a stolen key?

## Setup

- Key K has co-signers A, B, C. Outside guardians G1, G2, G3 were named when K
  was created (rule 1). Quorum is 2 of 3.
- A thief steals K and co-signer A. A and B revoke each other, so K freezes.

## Attack 1: thief steals one guardian's vouch (G1)

1. The thief wants K unfrozen onto replacement key T (the thief's own key).
2. Under rule 2, a vouch names its replacement key. G1's stolen signing
   material can produce a vouch for T, but the thief still needs a second guardian.
3. Without G2 or G3, there is no quorum. **Blocked by quorum (rule 1).**

## Attack 2: thief steals two guardian vouches (G1, G2)

1. Quorum is met for T, and rule 1's public delay of N positions starts.
2. The unfreeze request is public, so G1 or G2 sees a vouch issued in their name
   for a key they never approved.
3. Either one disowns it during the delay. **Cancelled by rule 2.**
4. Backup: any original co-signer (B or C) can also veto during the delay (rule 1).

## Attack 3: thief replays an honest vouch

1. The honest owner gets G1 and G2 to vouch for replacement key R.
2. The thief copies those vouches and tries to point them at T.
3. The vouches name R, not T. **Useless for T (rule 2).**

## Remaining gap

If the thief controls a guardian quorum **and** every guardian whose vouch was
stolen stays silent for N positions **and** no original co-signer vetoes,
the unfreeze goes through. The rules turn a silent theft into one that has to
stay unnoticed for the whole delay by several separate people. They do not
make the theft impossible. N is the knob: a longer delay is safer, but the
honest owner waits longer.
