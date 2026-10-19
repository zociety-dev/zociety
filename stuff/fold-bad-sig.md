# The fold on a bad (B) signature, empty allowedSignersFile

Direction: does a fold that accepts a commit when `%G?` is G or U and `%GK`
is in the live key set still reject a bad (B) signature?

**Yes, on git 2.51.0 and 2.55.0.** A bad signature gives `%G?=B` and an
**empty** `%GK`. So the fold rejects it twice over: once on `%G?`, and once
because no key matches the live set. A fold that read `%GK` alone would
still reject it. Cycle 43 found that `%GK` prints the signer's key even when
it is not in allowedSignersFile (U). It does not print it when the
signature fails to verify (B).

## Command

`bash stuff/fold-bad-sig.sh` (it builds and deletes its own repo under
`mktemp -d`, per rule 2). The bad commit is the good commit's object with
its message changed from `good` to `tampered` and the `gpgsig` header kept,
written with `git hash-object -t commit -w`.

## Output, host (macOS)

```
git: git version 2.51.0
ssh: OpenSSH_10.5p1, LibreSSL 3.3.6
live set: SHA256:frkAJG4HghNc3M++w4JvmRJ8++FbOkZl0SK2f2mRpzs
good  %G?=U %GK=SHA256:frkAJG4HghNc3M++w4JvmRJ8++FbOkZl0SK2f2mRpzs fold=accept gk-only=accept
bad   %G?=B %GK=-                                                  fold=reject gk-only=reject
none  %G?=N %GK=-                                                  fold=reject gk-only=reject
```

The host run also printed four `.pre-commit-config.yaml config file not
found` lines. They come from the host's global hook setup, not the script.

## Output, container (`bin/zociety bash stuff/fold-bad-sig.sh`)

```
git: git version 2.55.0
ssh: OpenSSH_10.0p2 Debian-7+deb13u4, OpenSSL 3.5.7 9 Jun 2026
live set: SHA256:Ulys1G9O0H5y4DEoVh1cgr0fESwrI6Y6/jUa/pcxfJ0
good  %G?=U %GK=SHA256:Ulys1G9O0H5y4DEoVh1cgr0fESwrI6Y6/jUa/pcxfJ0 fold=accept gk-only=accept
bad   %G?=B %GK=-                                                  fold=reject gk-only=reject
none  %G?=N %GK=-                                                  fold=reject gk-only=reject
```

## What this does not cover

- Only one kind of B: a valid signature over changed content. A truncated
  or garbled `gpgsig` block was not tried and might give a different
  `%G?` (E rather than B).
- The second half of the direction, a `[key]` revoke that leaves no live
  key, is not tested here. Position, untested: the fold should reject it.
  Once the live set is empty, no later commit can pass the fold, and that
  includes a `[key]` add, so the log can never take a signed commit again.
