# Exposure price: what unconditional expiry costs

This picks up the question settlement-trace.md left open: if a forged
revocation expires at filed + K whether or not its thief has been caught, is
the gap that opens up an acceptable price?

## Setup (same as the earlier traces)

K = 3. Thief A forges at position 2 and is revoked at 9. Thief B forges at 4
and is revoked at 7. A thief's revocation ends that thief's forgeries at once.

| Variant | A's forgery counts | B's forgery counts | Union of denials | Span |
|---|---|---|---|---|
| Rule 1 as passed (expires only once the signer is revoked) | 2..9 | 4..7 | 2..9 | 7 |
| Unconditional expiry at filed + K | 2..5 | 4..7 | 2..7 | 5 |

## The gap

Under unconditional expiry, A is still unrevoked from 5 to 9 and holds a key
that no forgery is using. A can simply forge again:

| A's forgery filed | Counts | Ends because |
|---|---|---|
| 2 | 2..5 | expiry |
| 5 | 5..8 | expiry |
| 8 | 8..9 | A revoked at 9 |

The union goes back to 2..9, 7 positions, the same as under rule 1. So
unconditional expiry does not bound exposure in time. What it bounds is the
**exposure per forgery**: each forged revocation denies at most K positions.
For a thief who stays uncaught for W positions, that means
**ceil(W / K) forgeries**, every one of them a separate, visible log entry.

## Settled cuts stay put

A's re-forgeries are new filings at 5 and 8, and rule 2 fixes K at the moment
each one is filed. Under rule 2 a cut filed at 6 settles only once K positions
have passed with no unexpired forgery against its signers. With A re-forging,
that point is pushed back to 9 + 3 = 12, the same value settlement-trace.md
found. No re-forgery reaches back to a cut that has already settled, so the
no-change property holds in both variants.

## Verdict

The gap is an acceptable price under one condition: forging has to cost the
thief something, such as a filing fee, a rate limit per key, or a detection
chance for every log entry. Under that condition, unconditional expiry turns
one silent, open-ended denial into a stream of forgeries, each of which can be
detected and costs the thief. Without that condition the two variants give the
same exposure, and rule 1's version is simpler.

A rate limit such as "one revocation per key per K positions" does not close
the gap: A's filings at 2, 5 and 8 are already K apart. A rule that does close
it, and is worth putting to a vote: **"a key whose revocation expired without
being confirmed may not file another."** With that rule A gets only 2..5, each
stolen key adds at most K positions, and the union is bounded by
K × (number of stolen keys), here 2..7 = 5. The cost falls on honest keys: a
real revocation that expires unconfirmed also loses its right to file again,
so confirmation has to be possible within K.
