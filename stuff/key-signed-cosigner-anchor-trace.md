# Key-signed co-signer registration: anchoring eligibility to the first filing

Follows up the open gap in `lost-cosigner-replacement-window.md`: if registering
a co-signer needs a signature from the key itself, the honest holder and the thief
both produce valid registrations, and rule 2's "not controlled by the revoked key"
cannot tell them apart. Window K = 3.

## Thief under rule 2 as written

- Position 1: theft. Thief registers co-signer C_t, signed with the key.
- Position 2: thief files a forged revocation, no confirmation.
- Position 5: it expires unconfirmed; rule 1's no-refile bar applies.
- Position 5: thief refiles with C_t's confirmation attached. C_t was registered
  4 positions earlier (>= K), and nothing marks it as thief-controlled, so rule 2
  accepts it. The bar is lifted. Denied span runs 2..8 and can repeat.

## Candidate fix: anchor to the earliest filing

A co-signer is eligible only if it was registered at least K positions before the
**first** revocation filing on that key, not just the current one.

- Thief: first filing at 2, C_t registered at 1. Ineligible for every later refile.
  The bar holds and exposure stays capped at K positions (2..5).
- Honest holder with a long-standing co-signer (registered at -10): eligible,
  confirmed, never barred.
- Honest holder who replaces a lost co-signer first (registers at 0, files at 3):
  eligible, confirmed.
- Honest holder who files first and replaces after (files at 2, registers at 3,
  refiles at 6): **ineligible**. The anchor closes the thief's path and also the
  honest file-first path that rule 2 had opened.

## Result

The earliest-filing anchor stops key-signed co-signer laundering and leaves settled
cuts unchanged, but it trades back the file-first honest holder. Still open: some
registration signal that the thief cannot produce from the key alone (e.g. a
co-signer registered through an existing eligible co-signer), so the honest
file-first holder can recover without reopening the thief's route.
