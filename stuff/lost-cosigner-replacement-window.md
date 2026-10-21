# Lost co-signer: when the honest revoker can still recover (K = 3)

Rules 1 and 2 leave one honest case open: the key's only co-signer is gone.
This traces what a replacement co-signer buys, and what it cannot.

## Setup

- Key A registered at position 0 with co-signer C1.
- C1 is lost at position 4 (keys destroyed, unreachable).
- A's holder discovers the theft of A at position 6.

## Trace: honest holder replaces C1 first

| pos | event | effect |
|-----|-------|--------|
| 6 | holder registers co-signer C2 for A | C2 not yet eligible (needs K = 3 positions) |
| 9 | holder files revocation of A | C2 registered at 6, 9 - 6 = 3 >= K: eligible |
| 10 | C2 confirms | before filed + K = 12: revocation confirmed |

Exposure: the thief can use A for positions 6..9, i.e. K + 1 positions
after discovery. No bar ever applies, because nothing expired unconfirmed.

## Trace: honest holder files immediately with no eligible co-signer

| pos | event | effect |
|-----|-------|--------|
| 6 | holder files revocation of A | only C1 is registered; C1 is lost |
| 6 | holder also registers C2 | eligible from 9 |
| 9 | filed + K passes, no confirmation | expires unconfirmed: A barred from refiling |
| 10 | C2 confirms, refiling with confirmation attached | rule 1: bar lifted, A revoked |

The honest revoker is delayed, not silenced: rule 1's "refile with
confirmation attached" is the exit, and rule 2 only requires C2 to predate
the *refiling*, not the original filing.

## Trace: thief tries the same move

| pos | event | effect |
|-----|-------|--------|
| 2 | thief forges revocation of A | C1 does not confirm |
| 5 | expires unconfirmed | A barred |
| 5 | thief registers C3 for A | rule 2: C3 is controlled by the revoked key's holder? |

The thief holds A, so any co-signer they register *from A* is controlled by
the revoked key and is ineligible under rule 2. The thief cannot use the
honest exit.

## What remains open

The distinction above relies on "not controlled by the revoked key". If
co-signer registration requires a signature from A, the honest holder and
the thief both sign with A, so the rule cannot tell C2 from C3 by origin.
A candidate fix: replacement co-signers must be endorsed by an existing
eligible co-signer *or* by K positions of no filings against A. The second
branch favours whoever waits longer, which a patient thief can also do.
