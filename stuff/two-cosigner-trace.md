# Two-co-signer trace under rules 1 and 2

Setup: key K files for the first time at position P. Co-signers A and B were
both registered before P. A was the first one, so rule 1 lets it count on its
own. B counts because A signed its registration.

| Case | What happens | Rule applied | Outcome |
|---|---|---|---|
| 1. Holder loses A after P | B signs the registration of a new co-signer A' | rule 2: signed by B, which is still eligible | Honest holder recovers |
| 2. Holder loses A and B after P | No eligible co-signer is left to sign a replacement, and K alone cannot sign one | rule 2 | Holder can never add a co-signer again. **Gap:** nothing in the rules lets them recover |
| 3. Thief steals K only, after P | Thief uses K to register C | rule 1/2: C is not signed by A or B | C does not count, so the thief is shut out |
| 4. Thief steals K only, before P, and the holder has registered no co-signer yet | Thief registers C first | rule 1: the "first co-signer" clause | C counts. **Gap:** the anchor only protects holders who register before the theft |
| 5. Thief steals K and A | A signs the registration of thief-controlled C | rule 2: A is still eligible | C counts, and the thief now holds two votes against B's one. **Gap:** no rule lets B mark A as compromised |

## Reading

The vouch requirement does what the direction asks in cases 1 and 3: a thief
holding only K is closed off, and an honest holder who lost one co-signer can
still replace it after filing. Three gaps remain:

- **Case 2:** losing every co-signer is permanent.
- **Case 4:** a theft before any co-signer is registered beats the anchor.
- **Case 5:** one stolen co-signer is enough to vouch in more of the thief's.

Next rule to draft: let any eligible co-signer revoke another co-signer's
eligibility. Then B could cut A off in case 5. That leaves the 1-of-n
ambiguity: B could be the one who was stolen.
