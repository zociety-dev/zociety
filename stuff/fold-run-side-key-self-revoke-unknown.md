# Fold run 2: side-branch [key], self-revoke, unknown signer

The three cases `first-parent-fold-run.md` left untested, run with its fold
copied verbatim. k0..k2 are in `gpg.ssh.allowedSignersFile`; k3 is not. Every
case is expected to end in a reject (exit 1). Script exit 0: all three did.

Results:
- Side-branch `[key]`: k1 (live) signs `[key] add k2` on a side branch, k0
  merges it, k2 then signs on first-parent. The merge is accepted, because k1
  was live at the merge, but the add does not take effect: the k2 commit is
  rejected as `signer not live`. Only first-parent `[key]` commits change the
  live set, so a key can only be added by a commit on first-parent.
- Self-revoke: k1 signs `[key] revoke k1`. The fold accepts it (nothing in
  rule 2 forbids it) and the revoke takes effect: k0 work after it is
  accepted, the next k1 commit is rejected as `signer not live`. A key may
  retire itself; if it is the last live key, nothing can sign after it.
  Whether that should be allowed is open; the fold does not check it.
- Unknown signer: with k3 absent from the allowed signers file, `%G?` prints
  `U`, and `%GF` and `%GK` both still print k3's `SHA256:` fingerprint. The
  fold rejects the side commit on `%G? not G` before any key logic. It would
  also be rejected without that check, since k3 was never added.

Proposal, not tested here: `%GK` names the signer whether or not git trusts
the key, so the fold could check the live set against `%GK` alone and accept
`%G?` of `G` or `U` (git's "good signature, unknown validity"). The allowed
signers file would then not need the union of every key. A run with an empty
allowed signers file would test it, and should also check that a bad
signature (`B`) still prints a `%GK` the fold must not trust.

Run: `bash fold-test-2.sh` on macOS, git 2.51.0, OpenSSH ed25519 keys,
outside any repo. The global hook template's `.pre-commit-config.yaml config
file not found` lines and trailing spaces after the graph's `|\` and `|/` are
removed from the output.

## Script

```bash
#!/usr/bin/env bash
# The three cases first-parent-fold-run.md left untested, same fold.
# Exit 0 when every case gives the expected fold exit code.
set -u
W=$(mktemp -d)
cd "$W" || exit 2
for k in k0 k1 k2 k3; do ssh-keygen -q -t ed25519 -N '' -C "$k" -f "$k"; done
fp() { ssh-keygen -lf "$W/$1.pub" | awk '{print $2}'; }
# Union of k0..k2 only: k3 is the signer git does not know.
for k in k0 k1 k2; do printf 't@t %s\n' "$(cat "$k.pub")"; done > allowed

newrepo() {
  git init -q -b main "$W/$1"; cd "$W/$1" || exit 2
  git config user.name t; git config user.email t@t
  git config gpg.format ssh; git config commit.gpgsign true
  git config gpg.ssh.allowedSignersFile "$W/allowed"
}
c() { local key=$1; shift; git -c user.signingkey="$W/$key" commit -q --allow-empty -m "$*"; }
m() { git -c user.signingkey="$W/$1" merge -q --no-ff -m "merge $2" "$2"; }
signer() { git log -1 --format=%GK "$1"; }
subj() { git log -1 --format=%s "$1"; }

fold() {   # verbatim from first-parent-fold-run.md
  local root live c s k a r
  root=$(git rev-list --max-parents=0 HEAD)
  live=" $(signer "$root") "
  for c in $(git rev-list --first-parent --reverse "$root..HEAD"); do
    if git rev-parse -q --verify "$c^2" >/dev/null; then
      for s in $(git rev-list "$c^1..$c^2"); do
        k=$(signer "$s")
        [ "$(git log -1 --format=%G? "$s")" = G ] || { echo "REJECT ${s:0:7}: %G? not G"; return 1; }
        case $live in *" $k "*) ;; *) echo "REJECT ${s:0:7} '$(subj "$s")': side-branch signer $k not live at merge ${c:0:7}"; return 1 ;; esac
      done
    fi
    k=$(signer "$c")
    [ "$(git log -1 --format=%G? "$c")" = G ] || { echo "REJECT ${c:0:7}: %G? not G"; return 1; }
    case $(subj "$c") in "[key] add "*)
      a=$(subj "$c"); a=${a#"[key] add "}
      [ "$a" = "$k" ] && { echo "REJECT ${c:0:7} '$(subj "$c")': signed by the key it adds"; return 1; } ;;
    esac
    case $live in *" $k "*) ;; *) echo "REJECT ${c:0:7} '$(subj "$c")': signer $k not live"; return 1 ;; esac
    case $(subj "$c") in
      "[key] add "*) a=$(subj "$c"); live="$live${a#"[key] add "} " ;;
      "[key] revoke "*) r=$(subj "$c"); r=${r#"[key] revoke "}; live=${live/" $r "/ } ;;
    esac
  done
  echo "ACCEPT"
}

case_side_key_add() {   # [key] add k2 on a side branch, merged; k2 then signs on first-parent
  c k0 root; c k0 "[key] add $(fp k1)"
  git checkout -q -b side; c k1 "[key] add $(fp k2)"; git checkout -q main
  m k0 side; c k2 "k2 work"
}
case_self_revoke() {    # k1 signs the revoke of k1; k1 then signs again
  c k0 root; c k0 "[key] add $(fp k1)"
  c k1 "[key] revoke $(fp k1)"; c k0 "k0 work"; c k1 "k1 after self-revoke"
}
case_unknown_signer() { # k3 (absent from allowedSignersFile) signs on a side branch
  c k0 root
  git checkout -q -b side; c k3 "k3 work"; git checkout -q main
  m k0 side
}

git --version
for k in k0 k1 k2 k3; do echo "$k=$(fp "$k")"; done
fail=0
for t in side_key_add:1 self_revoke:1 unknown_signer:1; do
  name=${t%:*}; want=${t#*:}
  echo; echo "== $name (want exit $want)"
  ( newrepo "$name"; "case_$name"
    git log --graph --format='%h %G? [%GF] [%GK] %s' | cat
    fold )
  got=$?
  echo "fold exit $got"
  [ "$got" = "$want" ] || fail=1
done
echo; echo "script exit $fail"
exit "$fail"
```

## Output (exit 0)

```text
git version 2.51.0
k0=SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k
k1=SHA256:zU8RitIpFcoINuflLNxAXLZS5KcVexWtIFY8cSuCdwI
k2=SHA256:h6fwQ+g633TbpNjvRdUff7wKPOa/F/DvhJ1V0ILMqcc
k3=SHA256:uA1I33MiHhCQxH+p1zR+Qyx/JjkOfJzh8uAAbxt6kCs

== side_key_add (want exit 1)
* 4941c28 G [SHA256:h6fwQ+g633TbpNjvRdUff7wKPOa/F/DvhJ1V0ILMqcc] [SHA256:h6fwQ+g633TbpNjvRdUff7wKPOa/F/DvhJ1V0ILMqcc] k2 work
*   3bb1c55 G [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] merge side
|\
| * b488874 G [SHA256:zU8RitIpFcoINuflLNxAXLZS5KcVexWtIFY8cSuCdwI] [SHA256:zU8RitIpFcoINuflLNxAXLZS5KcVexWtIFY8cSuCdwI] [key] add SHA256:h6fwQ+g633TbpNjvRdUff7wKPOa/F/DvhJ1V0ILMqcc
|/
* a1cf101 G [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] [key] add SHA256:zU8RitIpFcoINuflLNxAXLZS5KcVexWtIFY8cSuCdwI
* 9e307c4 G [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] root
REJECT 4941c28 'k2 work': signer SHA256:h6fwQ+g633TbpNjvRdUff7wKPOa/F/DvhJ1V0ILMqcc not live
fold exit 1

== self_revoke (want exit 1)
* 83bc04e G [SHA256:zU8RitIpFcoINuflLNxAXLZS5KcVexWtIFY8cSuCdwI] [SHA256:zU8RitIpFcoINuflLNxAXLZS5KcVexWtIFY8cSuCdwI] k1 after self-revoke
* 892f51a G [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] k0 work
* e124be2 G [SHA256:zU8RitIpFcoINuflLNxAXLZS5KcVexWtIFY8cSuCdwI] [SHA256:zU8RitIpFcoINuflLNxAXLZS5KcVexWtIFY8cSuCdwI] [key] revoke SHA256:zU8RitIpFcoINuflLNxAXLZS5KcVexWtIFY8cSuCdwI
* 269c3bf G [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] [key] add SHA256:zU8RitIpFcoINuflLNxAXLZS5KcVexWtIFY8cSuCdwI
* 2cadca1 G [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] root
REJECT 83bc04e 'k1 after self-revoke': signer SHA256:zU8RitIpFcoINuflLNxAXLZS5KcVexWtIFY8cSuCdwI not live
fold exit 1

== unknown_signer (want exit 1)
*   3c96966 G [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] merge side
|\
| * ada1887 U [SHA256:uA1I33MiHhCQxH+p1zR+Qyx/JjkOfJzh8uAAbxt6kCs] [SHA256:uA1I33MiHhCQxH+p1zR+Qyx/JjkOfJzh8uAAbxt6kCs] k3 work
|/
* 79dae9c G [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] [SHA256:ke1dcnUZY8vetEygSFW+IXt8K2Ifi/Fbr7Za89Jnv1k] root
REJECT ada1887: %G? not G
fold exit 1

script exit 0
```
