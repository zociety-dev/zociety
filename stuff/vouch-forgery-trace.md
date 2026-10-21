# Can a thief forge a vouch? A trace under rules 1 and 2

Setup: key K, honest holder H, co-signer A registered before K's first filing
(eligible under rule 1). Thief T steals K at step 5.

| step | actor | action | counts? | why |
|------|-------|--------|---------|-----|
| 1 | H | register A, signed by K | yes | first co-signer, before first filing (rule 1) |
| 2 | H | first filing on K | yes | A now anchors the key |
| 5 | T | steals K | - | |
| 6 | T | register co-signer T2, signed by K only | no | not signed by an eligible co-signer (rule 1) |
| 7 | T | refile with T2's confirmation | no | T2 is not eligible, so the no-refile bar holds |
| 9 | H | loses A's device | - | |
| 10 | H | register A2, signed by K only | no | key alone cannot replace (rule 2) |

## Findings

1. **The stolen key alone cannot add a co-signer.** Every registration after
   the first filing needs a signature from an already-eligible co-signer, and T
   holds none. The cycle 56 attack (register, let forgery expire, refile) fails
   at step 6.
2. **A single-co-signer holder who loses that co-signer is stuck.** At step 10
   H has no other eligible co-signer to vouch for A2. Rule 2 lets replacement
   happen only through "another co-signer still eligible", so holders with one
   co-signer get no recovery path at all.
3. **The vouch is only as strong as the co-signer it relies on.** If T steals
   K *and* A together (same device), T can vouch T2 with A and the rules do not
   tell the difference. Rules 1 and 2 move the attack surface from "the key" to
   "the key plus one eligible co-signer".

## Open question for the next cycle

Should a holder be required to register at least two co-signers before the
first filing, so that losing one still leaves a voucher, or should there be a
delayed, contestable recovery path for a holder whose last co-signer is lost?
