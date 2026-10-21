# Confirmation trace: thief vs honest revoker (K = 3)

Rules applied: rule 1 (independent pre-registered co-signer confirms; no-refile
bar only on keys whose revocation expired unconfirmed; refiling with
confirmation attached lifts the bar) and rule 2 (co-signer registered at least
K positions before filing, not controlled by the revoked key, confirmation
before filed + K).

## Thief (stolen key A, co-signer C registered at position 0)

| pos | event                                   | result                          |
|-----|-----------------------------------------|---------------------------------|
| 2   | thief files revocation of A             | pending until 5                 |
| 5   | no confirmation from C                  | expires; A barred from refiling |
| 5   | thief re-files                          | rejected: bar, no confirmation  |
| 5   | thief registers C' and asks it to sign  | rejected: C' registered at 5, not by 2 - 3 = -1 |

Denied span: 2..4 only. The repeat forgeries at 5 and 8 from cycle 55 can't
happen.

## Honest revoker (key B, co-signer D registered at position 0)

| pos | event                                   | result                          |
|-----|-----------------------------------------|---------------------------------|
| 2   | owner files revocation of B             | pending until 5                 |
| 5   | D was offline; expires unconfirmed      | B barred from refiling alone    |
| 7   | owner refiles with D's confirmation     | bar lifted; revocation stands   |

The honest revoker loses time but can still act: the bar blocks a filing with
no confirmation, not a confirmed one.

## Remaining gap

If D is lost for good, B can never be revoked. Rule 2 needs a co-signer that
was registered in advance, so the owner has to register a replacement before
filing. Positions settled before this point are unchanged.
