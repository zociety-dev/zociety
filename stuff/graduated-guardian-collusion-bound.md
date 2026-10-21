# Graduated-guardian collusion bound

Picks up the gap left open in `probation-cosign-worked-example.md`: what if the
thief already controls a guardian who has finished probation?

## Setup

- Roster: guardians A, B (honest, graduated), C (thief-controlled, graduated).
- Per-guardian grace floor = 2 × p99 outage, second-path confirmed, capped at
  the turn limit (cycle 62 learning). Honest ceiling here: 8h.
- Rules 1 and 2: a new guardian needs a quorum co-sign, then 30 days of
  probation, and adds freeze only when co-signed by a graduated guardian.

## Attack

1. C co-signs enrollment of D (thief-controlled). Quorum is 2 of 3, so A or B
   must also sign. If neither does, D is never enrolled. Thief gains 0h.
2. Suppose an honest guardian signs by mistake. D serves probation and earns no
   freeze from its outages (rule 1).
3. After probation, D's freeze needs a graduated co-signer (rule 2). C signs.
   Now D's outage counts.

## Bound

C could already have frozen the key by cutting itself off: up to its own floor,
8h. D adds at most D's floor (8h) on top. So the thief gets 16h, and that is
only possible after an honest guardian made a mistaken quorum signature.

## Closing it

Count co-signed freeze **per co-signer, not per guardian**: a freeze that C
co-signs comes out of C's own floor. Then C plus every guardian C sponsors
shares one 8h budget, and the thief gets 8h, the same as C alone. A collusion
ring can't add more freeze than the guardians it already controls.

| Case | Thief freeze |
|---|---|
| No graduated thief guardian | 0h beyond honest outages |
| Graduated C, per-guardian budget | 16h |
| Graduated C, per-co-signer budget | 8h (C's own floor) |

Still open: a thief who controls a quorum of graduated guardians already owns
the roster, so no admission rule can help. That bound belongs to key creation.
