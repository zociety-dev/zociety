# First-parent fold on a throwaway repo: self-signed [key] and revoked side branch

The fold from rule 2, run against three throwaway repos. Every case uses one
`allowedSignersFile` holding the union of every key any case adds, so git
verifies every signature (`%G?` is `G` on every commit below) and the fold, not
git, decides trust. The root is pinned by its signer: the root commit's `%GK`
is the only live key at the start.

Result: the fold rejects a `[key]` signed by the key it adds (exit 1) and a
side-branch commit signed by a key revoked on first-parent before the merge
(exit 1). The control, the same side-branch commit merged before the revoke,
is accepted (exit 0). Script exit 0: all three cases gave the expected code.

What the run settles:
- `%GK` prints the same `SHA256:...` string as `ssh-keygen -lf` field 2, so a
  `[key] add <fingerprint>` subject compares directly against `%GK`.
- A side-branch commit is judged at the merge that brings it in, not at its
  own position: `fc0ad1f` (case 1) and `c4c4097` (case 3) are both signed by
  k1 while k1 was live on their own branch; only the merge order differs.
- The self-add check runs before the live-set check, so the reject reason
  names the self-signing. With the checks in the other order the commit is
  still rejected, as `signer not live`.

Not tested here: a `[key]` commit on a side branch (the fold ignores it, since
only first-parent `[key]` commits change the live set), a key signing its own
revoke, and an untrusted signer (`%G?` other than `G`), which the fold rejects
before any key logic.

Run: `bash fold-test.sh` on macOS, git 2.51.0, OpenSSH ed25519 keys, outside
any repo. The global hook template printed `.pre-commit-config.yaml config
file not found` once per commit; those lines are removed from the output.

## Script

```bash
#!/usr/bin/env bash
# First-parent fold over [key] add/revoke commits, on throwaway repos.
# Exit 0 when every case gives the expected fold exit code.
set -u
W=$(mktemp -d)
cd "$W" || exit 2
for k in k0 k1 k2; do ssh-keygen -q -t ed25519 -N '' -C "$k" -f "$k"; done
fp() { ssh-keygen -lf "$W/$1.pub" | awk '{print $2}'; }
# Union of every key any case adds: git can verify every signature, trust is the fold's job.
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

fold() {
  local root live c s k a r
  root=$(git rev-list --max-parents=0 HEAD)
  live=" $(signer "$root") "   # root pinned: its signer is the only live key
  for c in $(git rev-list --first-parent --reverse "$root..HEAD"); do
    if git rev-parse -q --verify "$c^2" >/dev/null; then
      # commits a merge brings in are checked against the live set at that merge
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

case_merge_then_revoke() {   # control: k1 work merged while k1 live, revoked afterwards
  c k0 root; c k0 "[key] add $(fp k1)"
  git checkout -q -b side; c k1 "side work"; git checkout -q main
  m k0 side; c k0 "[key] revoke $(fp k1)"
}
case_self_add() {            # k2 signs the [key] that adds k2
  c k0 root; c k2 "[key] add $(fp k2)"
}
case_revoke_then_merge() {   # k1 work merged after k1 revoked on first-parent
  c k0 root; c k0 "[key] add $(fp k1)"
  git checkout -q -b side; c k1 "side work"; git checkout -q main
  c k0 "[key] revoke $(fp k1)"; m k0 side
}

git --version
echo "k0=$(fp k0)"; echo "k1=$(fp k1)"; echo "k2=$(fp k2)"
fail=0
for t in merge_then_revoke:0 self_add:1 revoke_then_merge:1; do
  name=${t%:*}; want=${t#*:}
  echo; echo "== $name (want exit $want)"
  ( newrepo "$name"; "case_$name"
    git log --graph --format='%h %G? %GK %s' | cat
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
k0=SHA256:VeWUxK7TUIUl42FbPawvpZajm+Ggkb0ZzWJMvr6lzYA
k1=SHA256:Epm9xBW6HtupKjA/WPuQVWTI7iCTQklBG9ym6K3EPzM
k2=SHA256:e/07vFSWTI9z3HcAP+tdGSibU/OLjMgafdENqZCxTdo

== merge_then_revoke (want exit 0)
* e05e66b G SHA256:VeWUxK7TUIUl42FbPawvpZajm+Ggkb0ZzWJMvr6lzYA [key] revoke SHA256:Epm9xBW6HtupKjA/WPuQVWTI7iCTQklBG9ym6K3EPzM
*   7eb2148 G SHA256:VeWUxK7TUIUl42FbPawvpZajm+Ggkb0ZzWJMvr6lzYA merge side
|\
| * fc0ad1f G SHA256:Epm9xBW6HtupKjA/WPuQVWTI7iCTQklBG9ym6K3EPzM side work
|/
* c714f23 G SHA256:VeWUxK7TUIUl42FbPawvpZajm+Ggkb0ZzWJMvr6lzYA [key] add SHA256:Epm9xBW6HtupKjA/WPuQVWTI7iCTQklBG9ym6K3EPzM
* 7a83193 G SHA256:VeWUxK7TUIUl42FbPawvpZajm+Ggkb0ZzWJMvr6lzYA root
ACCEPT
fold exit 0

== self_add (want exit 1)
* 03f9485 G SHA256:e/07vFSWTI9z3HcAP+tdGSibU/OLjMgafdENqZCxTdo [key] add SHA256:e/07vFSWTI9z3HcAP+tdGSibU/OLjMgafdENqZCxTdo
* 3e409f1 G SHA256:VeWUxK7TUIUl42FbPawvpZajm+Ggkb0ZzWJMvr6lzYA root
REJECT 03f9485 '[key] add SHA256:e/07vFSWTI9z3HcAP+tdGSibU/OLjMgafdENqZCxTdo': signed by the key it adds
fold exit 1

== revoke_then_merge (want exit 1)
*   dac9998 G SHA256:VeWUxK7TUIUl42FbPawvpZajm+Ggkb0ZzWJMvr6lzYA merge side
|\
| * c4c4097 G SHA256:Epm9xBW6HtupKjA/WPuQVWTI7iCTQklBG9ym6K3EPzM side work
* | 9e08604 G SHA256:VeWUxK7TUIUl42FbPawvpZajm+Ggkb0ZzWJMvr6lzYA [key] revoke SHA256:Epm9xBW6HtupKjA/WPuQVWTI7iCTQklBG9ym6K3EPzM
|/
* 00a74d7 G SHA256:VeWUxK7TUIUl42FbPawvpZajm+Ggkb0ZzWJMvr6lzYA [key] add SHA256:Epm9xBW6HtupKjA/WPuQVWTI7iCTQklBG9ym6K3EPzM
* bd92e62 G SHA256:VeWUxK7TUIUl42FbPawvpZajm+Ggkb0ZzWJMvr6lzYA root
REJECT c4c4097 'side work': side-branch signer SHA256:Epm9xBW6HtupKjA/WPuQVWTI7iCTQklBG9ym6K3EPzM not live at merge dac9998
fold exit 1

script exit 0
```
