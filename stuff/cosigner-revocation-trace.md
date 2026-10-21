# Co-signer revocation trace

The previous trace ended with an open gap: a key and one co-signer are both
stolen, and under rules 1 and 2 the stolen co-signer can vouch in more of the
thief's co-signers. The suggested fix was to let any eligible co-signer revoke
another. This file runs that fix to see where it breaks.

## Setup

- Key K, honest co-signers A and B, both eligible before K's first filing.
- The thief steals K and B.

## Candidate rule: any eligible co-signer may revoke another

1. The thief, as B, registers co-signer T (rule 2: B is eligible, so T counts).
2. A revokes B. A revokes T.
3. The thief, as B, revokes A first if they are faster.

The first revocation filed wins. That turns revocation into a race, and the
thief controls when the theft starts, so the thief usually wins.

## Fix 1: a revocation stays pending for N positions

A revocation takes effect only if nobody counter-revokes it within N
positions. If both sides revoke each other, the pending revocations block each
other and both co-signers are frozen.

- A freeze stops the thief from vouching in T or anyone else.
- The honest holder loses the ability to replace a co-signer, but nothing
  else. Filings that need only K still work.

A freeze is enough here: it closes the gap without having to tell which
co-signer was stolen.

## Fix 2: break the freeze by seniority

If co-signers registered earlier outrank later ones, A (registered first)
would win. But the thief can steal whichever co-signer is older, so seniority
just tells the thief which one to steal.

## Result

| Theft | Any-revokes | Pending + freeze |
|---|---|---|
| K + B, A honest | race, thief usually wins | both frozen, no new co-signers |
| K only | no effect | no effect |
| Both co-signers lost | holder stuck | holder stuck |

## Suggested rule

A co-signer revocation takes effect after N positions unless the revoked
co-signer files a counter-revocation in that window; mutual revocations freeze
both co-signers' ability to vouch.

Still open: a frozen key with no working co-signers is the same dead end as
"both co-signers lost". Getting out of it needs something outside the key's
own co-signer set.
