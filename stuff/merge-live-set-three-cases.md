# Live set at a disagreeing merge: three throwaway-repo cases

Answer to the cycle-46 direction. The live set at a merge is keys added in any
ancestor minus keys revoked in any ancestor (`git log X`, every commit, not
`--first-parent`). The no-empty-revoke check must run again at the merge:
case A has two parents that each pass alone and a merge whose own live set is
empty. The per-parent rule (cycle 45) is still needed beside it: in case C the
merged set is `{k2}`, non-empty, and only the per-parent check rejects it.

| case | L parent | R parent | merge live set | merge verdict | which check |
|------|----------|----------|----------------|---------------|-------------|
| A two revokes | `{k2}` ok | `{k1}` ok | `{}` | REJECT | merged-set rerun of no-empty-revoke |
| B add vs revoke | `{k1 k2 k3}` ok | `{k3}` ok | `{k2 k3}` | ok | none; k1 stays dead though L never revoked it |
| C add vs emptying revoke | `{k1 k2}` ok | `{}` REJECT | `{k2}` | REJECT | per-parent (R already rejected) |

A first-parent fold gets every merge wrong: `{k2}` at A (accepts an empty
set), `{k1 k2 k3}` at B (k1 revived), `{k1 k2}` at C (k1 revived, rejected
parent not seen).

## live.sh

```bash
g() { git -c commit.gpgsign=false -c user.name=t -c user.email=t@t "$@"; }
c() { g commit -q --allow-empty -m "$1"; }
# live set at X: keys added in any ancestor minus keys revoked in any ancestor (all of rev-list X, not --first-parent)
live() { git log --format=%s "$1" | awk '/^add /{a[$2]=1} /^revoke /{r[$2]=1} END{for(k in a) if(!(k in r)) print k}' | sort | tr '\n' ' '; }
# own check: a revoke or a merge must leave its live set non-empty (no-empty-revoke, rerun at merges)
own() { s=$(git log -1 --format=%s "$1"); n=$(git log -1 --format=%P "$1" | wc -w); l=$(live "$1")
  if { [ "${s#revoke}" != "$s" ] || [ "$n" -gt 1 ]; } && [ -z "${l// }" ]; then echo "no-empty-revoke: own live set empty"; else echo ok; fi; }
verdict() { for p in $(git log -1 --format=%P "$1"); do [ "$(verdict "$p")" = ok ] || { echo "REJECT by per-parent: parent '$(git log -1 --format=%s "$p")' rejected"; return; }; done
  o=$(own "$1"); [ "$o" = ok ] && echo ok || echo "REJECT by $o"; }
show() { printf '%-12s live={%s} %s\n' "$(git log -1 --format=%s "$1")" "$(live "$1")" "$(verdict "$1")"; }
```

## run.sh

```bash
#!/usr/bin/env bash
# Throwaway repo: each commit's subject is "add kN" or "revoke kN".
set -e
rm -rf r && git init -q r && cd r
. ../live.sh
run() { git checkout -q --orphan "$1"; for m in $2; do c "${m/_/ }"; done; b=$(git rev-parse HEAD)
  git checkout -q -b "$1-L" "$b"; for m in $3; do c "${m/_/ }"; done; L=$(git rev-parse HEAD)
  git checkout -q -b "$1-R" "$b"; for m in $4; do c "${m/_/ }"; done; R=$(git rev-parse HEAD)
  git checkout -q "$1-L"; g merge -q --no-ff -m "merge $1" "$1-R"
  echo "== $1: base [$2] | L [$3] | R [$4]"; show "$b"; show "$L"; show "$R"; show HEAD
  echo "   first-parent fold: {$(git log --first-parent --format=%s HEAD | awk '/^add /{a[$2]=1} /^revoke /{r[$2]=1} END{for(k in a) if(!(k in r)) print k}' | sort | tr '\n' ' ')}"; }
run A "add_k1 add_k2" "revoke_k1" "revoke_k2"
run B "add_k1 add_k3" "add_k2" "revoke_k1"
run C "add_k1" "add_k2" "revoke_k1"
```

## Output of `bash run.sh 2>/dev/null`

```
== A: base [add_k1 add_k2] | L [revoke_k1] | R [revoke_k2]
add k2       live={k1 k2 } ok
revoke k1    live={k2 } ok
revoke k2    live={k1 } ok
merge A      live={} REJECT by no-empty-revoke: own live set empty
   first-parent fold: {k2 }
== B: base [add_k1 add_k3] | L [add_k2] | R [revoke_k1]
add k3       live={k1 k3 } ok
add k2       live={k1 k2 k3 } ok
revoke k1    live={k3 } ok
merge B      live={k2 k3 } ok
   first-parent fold: {k1 k2 k3 }
== C: base [add_k1] | L [add_k2] | R [revoke_k1]
add k1       live={k1 } ok
add k2       live={k1 k2 } ok
revoke k1    live={} REJECT by no-empty-revoke: own live set empty
merge C      live={k2 } REJECT by per-parent: parent 'revoke k1' rejected
   first-parent fold: {k1 k2 }
```
