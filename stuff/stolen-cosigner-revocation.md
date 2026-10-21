# Revoking the stolen co-signer after a tie fallback

`zero-vouch-tie-break.md` left one gap: when two replacement keys still tie
and the key reverts to its pre-theft co-signer set, the stolen co-signer is
still in that set. The thief can start the whole contest again.

## What the thief holds

- One stolen co-signer key.
- No guardian vouches. Under rule 2 each vouch is tied to one replacement
  key, so a vouch the thief steals can only back the thief's own key.

## Options

1. **Drop the co-signer that started the losing or tied unfreeze.**
   Cheap, but an honest owner who started a real unfreeze and then tied
   would lose their own co-signer. That punishes the victim.
2. **Drop every co-signer that signed a key with zero vouches.**
   Under rule 1, a veto needs a guardian. A zero-vouch replacement key means
   no guardian supported that co-signer. An honest owner who can reach no
   guardian loses only the co-signer they used, and keeps the others.
3. **Let any one guardian revoke a co-signer at any time.**
   This gives guardians power outside the delay. One rogue guardian could
   remove honest co-signers one at a time.
4. **Rate-limit instead of revoking.** Each co-signer can start one unfreeze
   per N delays. The thief still holds the key, but every new attempt costs
   them N delay periods.

## Recommendation

Use 2 and 4 together. Option 2 removes the stolen co-signer after the first
tie, because the thief's key cannot get any vouches. Option 4 sets an upper
limit when option 2 doesn't apply, for example when the honest owner's key
also gets no vouches. Option 4 never leaves the key frozen for good, so the
condition from rule 1's timeout still holds.

## Open question

If both keys tie at zero vouches, option 2 removes both co-signers. With a
small co-signer set, that could leave fewer co-signers than the unfreeze
threshold needs. The next rule should set a minimum co-signer count that
revocation cannot go below.
