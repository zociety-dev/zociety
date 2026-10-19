#!/usr/bin/env bash
# Build a throwaway repo of N synthetic zevent-shaped commits, then time
# zstate's scan (git log -n W | jq) at W=1000 and W=10000.
set -e
N=${1:-12000}; d=$(mktemp -d); cd "$d"; git init -q
{ for i in $(seq 1 "$N"); do
    m="[stuff] member-1: s$i
{\"z\":1,\"event\":\"stuff\",\"cycle\":$((i/12)),\"agent\":\"member-1\",\"data\":{\"file\":\"stuff/s$i.md\"}}"
    printf 'commit refs/heads/main\ncommitter t <t@t> %d +0000\ndata %d\n%s\n' "$((1700000000+i))" "$(( ${#m} + 1 ))" "$m"
    printf '\n'
  done; } | git fast-import --quiet
git checkout -q main
scan() { git log --format='%x1e%H%n%B' -n "$1" | jq -R -s -c 'split("\u001e")[1:]|map(split("\n")[1:]|map(select(startswith("{")))|first|fromjson?)|length'; }
for w in 1000 10000; do
  s=$(python3 -c "import time;print(time.time())")
  for r in 1 2 3; do c=$(scan "$w"); done
  e=$(python3 -c "import time;print(round((time.time()-$s)/3,3))")
  echo "window=$w events=$c avg_s=$e"
done
rm -rf "$d"
