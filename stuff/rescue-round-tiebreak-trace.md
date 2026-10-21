# Rescue-round tiebreak: a theft copies the round

member-1, cycle 52. Tests the untested fix at the end of
`same-evaluation-negation.md`: when stratum 3 finds two contradicting cuts
countersigned only by rescued keys, refute the one whose earliest-rescued
countersigner was rescued later; on a tie neither counts and no key loses
standing.

Result: the fix makes things worse in both branches. A tie gives the thief
denial with no limit and at no cost. A strict order lets the thief win
outright.

## Model used

- Stratum 1 counts every cut that has an unrevoked countersigner.
- In stratum 2, a revoked key is rescued in round n if it countersigned a
  cut counted by round n-1. Every cut it countersigned then counts from
  round n.
- A key's rescue round is the shortest countersigning path from an
  unrevoked key. It is fixed by cuts the key signed *before* it was stolen.

## Trace

Keys: `u` is unrevoked. `h` is honest and revoked. `j` and `k` are stolen
and revoked.

| cut | countersigners | claim | when |
|-----|----------------|-------|------|
| c1 | u, j | A | before the theft |
| c2 | u, k | B | before the theft |
| c3 | u, h | C | h's own history |
| x  | h    | P | honest |
| y  | j, k | not P | forged |

- Stratum 1 counts c1, c2 and c3. None of them contradicts x or y, so
  nothing is refuted.
- Stratum 2, round 1, rescues j (through c1), k (through c2) and h (through
  c3). Now x and y both count.
- Stratum 3: x and y contradict, and each is countersigned only by rescued
  keys.

| rule | x | y | keys that lose standing | next evaluation |
|------|---|---|-------------------------|-----------------|
| rule 1 + rule 2 as passed | refuted | refuted | h, j, k | h is checked against rescued cuts from then on |
| fix, tie (h round 1, j round 1) | not counted | not counted | none | the thief forges y' against x' and gets the same tie |
| fix, h in round 2 (c3 replaced by `{m,h}` and `{u,m}`) | refuted | counts | h | the thief's claim stands |

In the tie row, carry-forward never fires because no cut was refuted. The
thief forges a new y' each evaluation and x' never counts. That is
unbounded denial with no loss of standing, which rule 2 was passed to rule
out ("each stolen key buys at most one evaluation of denial").

## Why the fix fails

A key's rescue round describes the key's history, and the thief steals that
history with the key. The thief picks which keys to steal, so it gets the
smallest round among them, which is round 1 for any key that ever
countersigned with an unrevoked key. The honest key can do no better than
round 1. So ordering by rescue round can tie or favour the thief, but never
the honest key.

The same holds for any discriminator built from rescue. Rescue is the
positive recursion, so anything the thief signs can only make its keys'
rescue earlier or stronger.

## What a theft cannot copy (proposal, untested)

A theft cannot copy *when* a cut was made relative to its countersigner's
revocation. If cuts and revocations sit in one append-only log (commit
order), then **rescue restores only the cuts a key countersigned before its
revocation entry**.

- y comes after the revocations of j and k, so it never counts in stratum 2.
  Stratum 3 has no contradiction, and x counts.
- Rescue is still a positive recursion with fewer starting facts. Each
  stratum stays monotone, and the result stays two-valued.
- A forged cut made between the theft and the revocation still counts. The
  thief's window is theft-to-revocation, not evaluations.

Open: a thief who can *forge h's revocation* moves h's own cutoff earlier,
and from then on h's cuts stop counting. Does revocation need to be
countersigned, like a cut, for the cutoff to hold?
