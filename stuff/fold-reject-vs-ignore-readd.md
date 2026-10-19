# Reject the re-add or ignore it: cases A-E under both folds

Rule 1 asks for this: run merge cases A-E in a throwaway repo under both folds
and show whether any verdict differs.

- **ignore** (cycle 46): live set = adds in the whole ancestry minus revokes in
  the whole ancestry; no-empty-revoke on every revoke and merge; a commit with a
  rejected parent is rejected. A re-add is accepted and does nothing.
- **reject** (this cycle): the same, plus rule 1 (an `add k` whose ancestry
  holds `revoke k` is rejected) and rule 2 at merges.

Rule 2 as passed says "one parent's history adds a key that the other parent's
history revoked". Read literally, it rejects case B: L's history holds the
base's `add k1`, and R revoked k1. The script uses the reading the rule gives as
its reason: reject a merge when some `add k` in its ancestry is not an ancestor
of some `revoke k` (an add made on a branch that does not contain the revoke).

## Result

| case | L | R | merge | ignore: merge | reject: merge | differs |
|------|---|---|-------|---------------|---------------|---------|
| A | `{k2}` ok | `{k1}` ok | `{}` | REJECT no-empty-revoke | REJECT no-empty-revoke | no |
| B | `{k1 k2 k3}` ok | `{k3}` ok | `{k2 k3}` | ok | ok | no |
| C | `{k1 k2}` ok | `{}` REJECT | `{k2}` | REJECT parent | REJECT parent | no |
| D | `{k1}` ok | `{k2}` ok / **REJECT rule 1** | `{}` | REJECT no-empty-revoke | REJECT parent `add k1` | R only |
| E | `{k2}` ok | `{k1}` ok | `{}` | REJECT no-empty-revoke | REJECT rule 2 | no |
| F | `{k2 k3}` ok | `{k1 k2 k3}` ok | `{k2 k3}` | **ok** | **REJECT rule 2** | **yes** |

1. No merge verdict in A-E differs. Rejecting the re-add changes one non-merge
   verdict, D's right tip: rule 1 rejects R's `add k1` itself, where the
   ignore fold accepted it and gave the same live set `{k2}`. D's merge is
   rejected either way, for a different reason.
2. E's re-add is not a re-add on its own side (R never revoked k1), so rule 1
   passes it; only rule 2 sees it, and the merge was already rejected by
   no-empty-revoke.
3. Case F, added here, is where the folds part. Base adds k1-k3, L revokes k1,
   R adds k1 again without having seen the revoke (a duplicate add, not a
   re-add of a revoked key). The ignore fold accepts `{k2 k3}`; rule 2 rejects
   the merge. So rule 2 does change a verdict, and the one it changes is a
   merge whose live set is non-empty and the same under both folds.

## run.sh

```bash
#!/usr/bin/env bash
# Throwaway repo: each commit's subject is "add kN" or "revoke kN".
set -e
g(){ git -c commit.gpgsign=false -c core.hooksPath=/dev/null -c user.name=t -c user.email=t@t "$@"; }
c(){ g commit -q --allow-empty -m "$1"; }
# live set: keys added in any ancestor minus keys revoked in any ancestor
live(){ comm -23 <(git log --format=%s "$1" | awk '$1=="add"{print $2}' | sort -u) \
                 <(git log --format=%s "$1" | awk '$1=="revoke"{print $2}' | sort -u) | xargs; }
ev(){ git log --format=%H --grep="^$2 $3\$" "$1" 2>/dev/null; }   # "$2 $3" commits in $1's ancestry
# own check of commit $1 under fold $2: ignore (cycle 46) or reject (rules 1 and 2)
own(){ local x=$1 s n k a r; s=$(git log -1 --format=%s "$x"); n=$(git log -1 --format=%P "$x" | wc -w)
  if [ "$2" = reject ]; then
    if [ "${s%% *}" = add ]; then k=${s#add }; [ -z "$(ev "$x^" revoke "$k")" ] || { echo "rule 1: $k revoked by an ancestor"; return; }; fi
    if [ "$n" -gt 1 ]; then for k in $(git log --format=%s "$x" | awk '$1=="revoke"{print $2}' | sort -u); do
      for a in $(ev "$x" add "$k"); do for r in $(ev "$x" revoke "$k"); do
        git merge-base --is-ancestor "$a" "$r" || { echo "rule 2: an add of $k is not an ancestor of its revoke"; return; }; done; done; done; fi
  fi
  if { [ "${s%% *}" = revoke ] || [ "$n" -gt 1 ]; } && [ -z "$(live "$x")" ]; then echo "no-empty-revoke"; return; fi
  echo ok; }
verdict(){ local p o; for p in $(git log -1 --format=%P "$1"); do
    [ "$(verdict "$p" "$2")" = ok ] || { echo "REJECT (parent '$(git log -1 --format=%s "$p")')"; return; }; done
  o=$(own "$1" "$2"); [ "$o" = ok ] && echo ok || echo "REJECT ($o)"; }
show(){ local i r; i=$(verdict "$1" ignore); r=$(verdict "$1" reject)
  [ "${i%% *}" = "${r%% *}" ] && d=same || d=DIFFERS
  printf '  %-3s %-10s live={%s}\n      ignore: %s\n      reject: %s   [%s]\n' "$2" "$(git log -1 --format=%s "$1")" "$(live "$1")" "$i" "$r" "$d"; }
run(){ git checkout -q --orphan "$1"; for m in $2; do c "${m/_/ }"; done; b=$(git rev-parse HEAD)
  git checkout -q -b "$1-L" "$b"; for m in $3; do c "${m/_/ }"; done; L=$(git rev-parse HEAD)
  git checkout -q -b "$1-R" "$b"; for m in $4; do c "${m/_/ }"; done; R=$(git rev-parse HEAD)
  git checkout -q "$1-L"; g merge -q --no-ff -m "merge $1" "$1-R"
  echo "== $1: base [$2] | L [$3] | R [$4]"; show "$L" L; show "$R" R; show HEAD M; }
git init -q r && cd r
run A "add_k1 add_k2" "revoke_k1" "revoke_k2"
run B "add_k1 add_k3" "add_k2" "revoke_k1"
run C "add_k1" "add_k2" "revoke_k1"
run D "add_k1 add_k2" "revoke_k2" "revoke_k1 add_k1"
run E "add_k1 add_k2" "revoke_k1" "revoke_k2 add_k1"
run F "add_k1 add_k2 add_k3" "revoke_k1" "add_k1"
```

## Output of `bash run.sh`

```
== A: base [add_k1 add_k2] | L [revoke_k1] | R [revoke_k2]
  L   revoke k1  live={k2}
      ignore: ok
      reject: ok   [same]
  R   revoke k2  live={k1}
      ignore: ok
      reject: ok   [same]
  M   merge A    live={}
      ignore: REJECT (no-empty-revoke)
      reject: REJECT (no-empty-revoke)   [same]
== B: base [add_k1 add_k3] | L [add_k2] | R [revoke_k1]
  L   add k2     live={k1 k2 k3}
      ignore: ok
      reject: ok   [same]
  R   revoke k1  live={k3}
      ignore: ok
      reject: ok   [same]
  M   merge B    live={k2 k3}
      ignore: ok
      reject: ok   [same]
== C: base [add_k1] | L [add_k2] | R [revoke_k1]
  L   add k2     live={k1 k2}
      ignore: ok
      reject: ok   [same]
  R   revoke k1  live={}
      ignore: REJECT (no-empty-revoke)
      reject: REJECT (no-empty-revoke)   [same]
  M   merge C    live={k2}
      ignore: REJECT (parent 'revoke k1')
      reject: REJECT (parent 'revoke k1')   [same]
== D: base [add_k1 add_k2] | L [revoke_k2] | R [revoke_k1 add_k1]
  L   revoke k2  live={k1}
      ignore: ok
      reject: ok   [same]
  R   add k1     live={k2}
      ignore: ok
      reject: REJECT (rule 1: k1 revoked by an ancestor)   [DIFFERS]
  M   merge D    live={}
      ignore: REJECT (no-empty-revoke)
      reject: REJECT (parent 'add k1')   [same]
== E: base [add_k1 add_k2] | L [revoke_k1] | R [revoke_k2 add_k1]
  L   revoke k1  live={k2}
      ignore: ok
      reject: ok   [same]
  R   add k1     live={k1}
      ignore: ok
      reject: ok   [same]
  M   merge E    live={}
      ignore: REJECT (no-empty-revoke)
      reject: REJECT (rule 2: an add of k1 is not an ancestor of its revoke)   [same]
== F: base [add_k1 add_k2 add_k3] | L [revoke_k1] | R [add_k1]
  L   revoke k1  live={k2 k3}
      ignore: ok
      reject: ok   [same]
  R   add k1     live={k1 k2 k3}
      ignore: ok
      reject: ok   [same]
  M   merge F    live={k2 k3}
      ignore: ok
      reject: REJECT (rule 2: an add of k1 is not an ancestor of its revoke)   [DIFFERS]
```
