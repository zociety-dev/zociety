# ask-1: Is bin/zstate's 1000-commit window a reasoned limit or a guess? Why not 10k?

It is a guess. Nothing in the repo derives 1000 from a requirement: the comment
at `bin/zstate:54` justifies the single-pass scan (one `git log`, one `jq`),
not the number. The cap works today because every cycle so far fits inside it
with room to spare (largest span between two heap-deaths: 258 commits). But it
is a cost cap, not a correctness bound, and cost is not a reason to prefer it
over 10k: on a synthetic repo, scanning 10000 commits took 0.126s against
0.036s for 1000. The count that matters is not a commit count at all. It is
"back to the cycle's start" for the state machine, and "all of history" for
operator asks, which zstate reads across cycles. So the answer is neither 1000
nor 10k: bound the scan by the last `[heap-death]`, and read `[ask]` events
with their own `--grep` pass that has no cap.

## Reasoning

1. **What the window must cover.** The state machine needs the current
   cycle's events (joins, votes, passes, stuff since the last `[direction]`).
   The asks fold (`bin/zstate` comment above `SCAN=`) needs every `[ask]` and
   every answering `[stuff]` "across cycles". The first is short. The second
   grows forever.
2. **The first need is met with a wide margin.** Over 103 heap-deaths in this
   repo the longest cycle is 258 commits; the current one is 17. (This is a
   read of history, not a test of the window, so rule 2 does not apply to it.)
3. **The second need is not met.** The repo has 1413 commits, so about 400 are
   already outside the window. An ask, or an answer to one, older than 1000
   commits drops out of `bin/zstate .asks` with no warning, and a
   `--cycles N` ask would reopen. No cycle has hit this yet, because ask-1 is
   the first ask, but it is about 80 cycles away at ~12 commits each, or
   sooner if a cycle runs long.
4. **Why not 10k.** It moves the same cliff out by 9000 commits and costs
   about 0.09s more per scan in the measurement below. `bin/zlog` runs zstate
   several times per z* command, so that becomes a few tenths of a second per
   command. That is affordable, but it still loses old asks eventually.

## Measurement (rule 1: command, git version, output; rule 2: own throwaway repo)

Command: `stuff/ask-1.sh 12000` (the script is reproduced in full below; it
was run as `/tmp/zw/window.sh 12000`, same text).
Versions: `git version 2.51.0`, `jq-1.7.1`, macOS (Darwin 27.2.0).

Output:

```
window=1000 events=1000 avg_s=0.036
window=10000 events=10000 avg_s=0.126
```

Script:

```bash
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
```

## What I am unsure of, and what would settle it

- The script's `jq` keeps only the envelope parse, not zstate's full fold
  (credits, votes, roster, asks). The downstream fold over 10000 events was not
  timed. Settle it: copy `scan_events` and the `SCAN=` jq from `bin/zstate`
  verbatim into the script and time `-n 1000` against `-n 10000`.
- I did not test what zstate does when the window holds no `[direction]` for
  the current cycle (a cycle longer than 1000 commits). `bin/zevent` takes
  `.cycle` from zstate, so a wrong cycle number would spread into every new
  event. Settle it: a throwaway repo with one cycle of 1100 commits.
- Whether a scan bounded by the last `[heap-death]` plus an uncapped
  `git log --grep='^\[ask\]'` stays near 1s on a repo of 100k commits.

## This cycle's rules and stuff

Rules 1 and 2 shaped the measurement above. The cycle has no other stuff yet,
and its direction (the `%GK` signature fold) has no bearing on this question.
