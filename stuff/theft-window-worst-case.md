# Theft-window worst case under rules 1 and 2

Setup: honest key H, countersigner C. C's key is stolen at log position t;
C's own revocation first counts at log position p (t < p). Forged
revocations of H, countersigned by stolen C, can land anywhere in [t, p).

## Walk-through (one in-order pass)

| pos | event                         | H cutoff seen by cuts at this pos |
|-----|-------------------------------|-----------------------------------|
| t   | C stolen (not yet visible)    | none                              |
| f   | forged revoke of H, signed C  | f  (pulled earlier)               |
| p   | C's own revocation counts     | none again for cuts after p       |
| q>p | H cuts                        | accepted                          |

- Rule 2: each H cut at q is judged once from events before q. Cuts in
  (f, p) were judged while the forgery counted, so they stay denied.
- Rule 1: from p on, forged revocations signed by C stop counting, so H's
  cutoff recovers at p. Nothing before p is recomputed.

## Worst-case count

The forger's best move is f = t (forge immediately). Denied cuts are then
H's cuts in (t, p]: at most `p - t` positions, and exactly the number of H
cuts the log holds in that interval. The bound depends only on detection
latency `p - t`, not on how many forgeries are issued: a second forgery in
the same window denies nothing the first did not.

## Answer to the direction

Yes, recovery is forward-only at p with no retroactive recomputation. The
window denies at most H's cuts inside (t, p]; shrinking `p - t` (faster
countersigner revocation) is the only lever that reduces it.
