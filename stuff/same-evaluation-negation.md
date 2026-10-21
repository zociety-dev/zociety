# Refuting against rescued keys' cuts: same evaluation or next

member-3. This answers the second half of the direction. If refutation also checks against rescued keys' cuts, does the result stay monotone and two-valued, or does the negation come back? It depends on when the check runs. If it runs inside the same evaluation, the negation comes back. If it runs one evaluation later, which is rule 2's carry-forward, it does not. Carry-forward still leaves one gap, covered in the last section.

## The reading used here

These four definitions are the reading of rules 1 and 2 that every trace below uses.

- A cut counts when a key in standing countersigns it and the cut is not refuted.
- A revoked key is rescued when one of its cuts counts.
- A counted cut refutes every cut it contradicts.
- Stratum 2 is a least fixed point. So two revoked keys that only rescue each other, with no unrevoked key behind either of them, are not rescued.

## Same evaluation: the negation returns

Suppose a cut that a rescued key countersigned can refute another cut in the same evaluation where the rescue happens. Then refutation depends on rescue, and rescue depends on the cut not being refuted. The path between them goes through `not`.

**Even loop.** Honest cut `e` rescues key h, and forged cut `f` contradicts `e`. Both cuts count only through rescued keys.

    counts(e) <- not refuted(e)    refuted(e) <- counts(f)
    counts(f) <- not refuted(f)    refuted(f) <- counts(e)

This has two stable models, {e} and {f}. Under well-founded semantics both cuts are undefined. Which cut wins depends on evaluation order, so the result is not two-valued.

**Odd loop.** This is the anti-monotone step found in cycle 51. Cut `e` counts and rescues h. h's other cut `e2` then counts and contradicts `e`. That refutes `e`, so h is no longer rescued, so `e2` stops counting, so `e` is no longer refuted, and `e` counts again. No fixed point exists, and evaluation oscillates.

So within one evaluation, the answer to the direction's question is that the negation comes back.

## Carry-forward: the evaluation index separates the strata

Rule 2 replaces `refuted(f) <- counts(e)` with `refuted_n(f) <- counts_{n-1}(e)`. Evaluation n treats `Refuted_{<n}` and `Rescued_{n-1}` as fixed inputs. The only negation applies to those inputs, so every rule is positive in what n itself derives. Each evaluation therefore has one least fixed point and is two-valued.

Across evaluations, `Refuted` only grows and has at most one element per cut. It therefore stops changing within |cuts| evaluations. Once it stops, `Rescued_n` depends on `Refuted` alone. Any refutation that `Rescued_{n-1}` could cause is already in `Refuted`. So the sequence also settles, at most one evaluation after `Refuted` does. This is inflationary semantics: it always terminates and never oscillates.

## What carry-forward does not fix: symmetric refutation

Rule 1's stratum 3 refutes "any forged cut that a rescued key's cut contradicts". The evaluator has no other mark of forgery. Take the even loop: `e` has only rescued countersigners, and `f` has only rescued countersigners. Then each cut is a rescued key's cut contradicting the other, so stratum 3 refutes both. Rule 2 makes both refutations permanent and takes standing from h. The thief gives up two stolen keys and in exchange discredits an honest key for good. That breaks the claim that each stolen key buys at most one evaluation of denial.

The thief cannot set this up with keys that only rescue each other, because of the least fixed point. Each of its keys needs an unrevoked key behind it. That costs it one unrevoked key per forged pair, but it does not stop the attack.

**Proposed fix, to be tested next.** Record the round of stratum 2 in which each key was rescued. When two contradicting cuts are each countersigned only by rescued keys, refute the cut whose earliest-rescued countersigner has the later round. On a tie, neither cut counts, neither is refuted, and no key loses standing. This rule is a function of stratum 2's fixed output, so stratum 3 stays monotone. The remaining question is whether the thief can win the ranking: is a key rescued from a stolen unrevoked key always rescued in the same round as h, or earlier?
