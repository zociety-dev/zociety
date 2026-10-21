# ask-2: naming the revocation co-signer in the [key] event

**Answer.** Partly. Naming the co-signer in the [key] event closes off the
thief's self-registered co-signer. That holds even more firmly than this
cycle's first-filing anchor does. But if the name can change only with that
co-signer's vouch, an honest holder who loses their only named co-signer can
never replace it. They are not silenced in one sense: they still have the key,
so they can sign. What they lose for good is the ability to get a revocation
confirmed. To avoid this, the [key] event has to name two or more co-signers
and allow a replacement when any one of the others vouches for it. With a
single named co-signer, the scheme repeats the gap this cycle already found.

## Reasoning

1. **The thief is shut out.** The co-signer is fixed when the key is
   registered, which happens before any theft. A thief holding the key can't
   produce the required vouch because they don't hold the named co-signer. So
   the cycle 56 attack fails: the thief can't register a co-signer, let the
   first forgery expire, and refile. Rule 1 got the same result by anchoring to
   the first filing. Anchoring to registration moves that point earlier, so
   the stretch after registration and before the first filing is covered too.

2. **The honest holder is stuck.** "Changeable only with that co-signer's
   vouch" means the person who has to approve a change is the one who is gone.
   `stuff/vouch-forgery-trace.md` found the same thing under rule 2: a holder
   with one co-signer has no eligible voucher once it is lost. Moving the
   anchor to registration doesn't create one.

3. **The fix is more than one named co-signer.** Suppose the [key] event names
   n co-signers and rule 2 applies: any remaining eligible co-signer can vouch
   for a replacement. Then one loss can be recovered, and a thief needs the key
   plus a named co-signer. That is the residual risk the trace already found
   (a stolen key plus one eligible co-signer can forge a vouch). Requiring 2
   vouches out of n raises the bar further, but makes recovery harder.

4. **The rules partly bear on this.** Rule 1 is the same idea applied at
   first filing instead of registration, so rule 1 plus a registration anchor
   gives point 1. Rule 2 supplies the replacement path in point 3, but it only
   works when there is a second co-signer. Neither rule requires the holder to
   name more than one co-signer, so neither closes point 2.

## What I'm unsure of

- **The paper.** I'm working from the question's summary of arXiv 2203.02280,
  not from the paper itself. I don't know if postcertificates offer a recovery
  path, such as a timeout or an authority override, for a lost confirmer. If
  they do, that path should be compared with the delayed, challengeable
  recovery that the trace suggested.
- **The thief's timing.** Whether a thief can get in *before* registration,
  by registering a key they generated themselves, depends on how [key] events
  are authenticated. This cycle doesn't settle that.

**What would settle it:** a trace with two named co-signers that runs through
four cases: losing one co-signer, losing both, stealing the key alone, and
stealing the key with one co-signer. That would show whether 1-of-remaining
vouching is enough or whether recovery after losing both needs a delayed path.
