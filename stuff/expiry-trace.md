# Trace: does rule 1's expiry shrink the theft-window union?

Setup from cycle 54: two stolen countersigners.
- Thief A: forged revocation filed at 2, A's key revoked at 9.
- Thief B: forged revocation filed at 4, B's key revoked at 6.
- Without expiry, a forgery counts from when it is filed until its thief is revoked.
  Union of windows = 2..9 (7 positions).

Rule 1 with K = 3: a forgery expires at filed+K unless its signer is still unrevoked then.

| forgery | filed | check at | signer revoked by then? | counts until |
|---------|-------|----------|-------------------------|--------------|
| A       | 2     | 5        | no (revoked at 9)       | 9            |
| B       | 4     | 7        | yes (revoked at 6)      | 6            |

Union under rule 1 = 2..9, the same 7 positions as before.

## Finding
The "unless still unrevoked" clause keeps a forgery alive exactly when its thief
has not been caught. When the thief is caught before filed+K, the window
already ended at the revocation. So expiry never cuts a window short:
window = [filed, revoked) both with and without rule 1.

To actually bound the union, a forgery has to expire at filed+K
unconditionally. That gives union <= (latest filing - earliest filing) + K.
Here that is 2..7 = 5 positions. The cost is that a forgery from a thief who
is never caught stops counting after K positions.

Settled cuts: rule 2 only settles a cut when no forgery against its signers
is unexpired. Under the unconditional variant, expiry happens only at
position filed+K, which is still in the future when any earlier cut is
settled. So expiry cannot change a verdict that is already settled.
