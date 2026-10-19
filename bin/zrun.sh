# shellcheck shell=bash
# shellcheck disable=SC2034  # the ZRUN_* paths are read by the sourcing scripts
# zrun.sh: a run's bounds and its record, sourced by bin/zloop, bin/zloop-ctl
# and bin/zask (all run from the repo root).
#
#   zrun_secs DURATION  seconds in DURATION: 90, 90s, 45m, 8h, 3d, 1h30m
#                       (a bare number is seconds); exit 1 if malformed
#   zrun_fmt SECS       the short form: 42s, 12m05s, 5m, 1h05m, 8h, 3d4h
#   zrun_clock EPOCH    local time of EPOCH: "Tue 04:15"
#   zrun_live_pid       pid of the run going in this worktree on this host,
#                       from its record; exit 1 if there is none
#
# The record: bin/zloop writes .zociety/run.json when a run starts and
# rewrites it every iteration (pid, host, bounds, iteration, spend), and
# moves it to .zociety/run.last.json, with the reason it ended, on exit.
# .zociety/run.stop asks the run to stop before its next turn (bin/zloop
# stop); .zociety/asks.inbox holds asks made while it runs (bin/zask), which
# it records between turns.

ZRUN_RECORD=.zociety/run.json
ZRUN_LAST=.zociety/run.last.json
ZRUN_STOP=.zociety/run.stop
ZRUN_INBOX=.zociety/asks.inbox
ZRUN_LOGS=.zociety/runs

zrun_secs() {
  local s="$1" total=0 n
  if [[ "$s" =~ ^[0-9]+$ ]]; then
    echo $((10#$s))
    return 0
  fi
  [[ "$s" =~ ^([0-9]+[smhd])+$ ]] || return 1
  while [[ "$s" =~ ^([0-9]+)([smhd])(.*)$ ]]; do
    n=$((10#${BASH_REMATCH[1]}))
    case "${BASH_REMATCH[2]}" in
      m) n=$((n * 60)) ;;
      h) n=$((n * 3600)) ;;
      d) n=$((n * 86400)) ;;
    esac
    total=$((total + n))
    s="${BASH_REMATCH[3]}"
  done
  echo "$total"
}

zrun_fmt() {
  local s="$1"
  if [[ $s -ge 86400 ]]; then
    if [[ $((s % 86400 / 3600)) -eq 0 ]]; then printf '%dd' $((s / 86400))
    else printf '%dd%dh' $((s / 86400)) $((s % 86400 / 3600)); fi
  elif [[ $s -ge 3600 ]]; then
    if [[ $((s % 3600 / 60)) -eq 0 ]]; then printf '%dh' $((s / 3600))
    else printf '%dh%02dm' $((s / 3600)) $((s % 3600 / 60)); fi
  elif [[ $s -ge 60 ]]; then
    if [[ $((s % 60)) -eq 0 ]]; then printf '%dm' $((s / 60))
    else printf '%dm%02ds' $((s / 60)) $((s % 60)); fi
  else
    printf '%ds' "$s"
  fi
}

# BSD date reads an epoch with -r; GNU date takes -r as a file and fails over
# to -d @EPOCH.
zrun_clock() {
  date -r "$1" '+%a %H:%M' 2>/dev/null || date -d "@$1" '+%a %H:%M'
}

# A record whose pid is gone, or now belongs to some other program, is stale:
# the run died without its EXIT trap (SIGKILL, a reboot).
zrun_live_pid() {
  local host pid
  [[ -f "$ZRUN_RECORD" ]] || return 1
  host=$(jq -r '.host // empty' "$ZRUN_RECORD" 2>/dev/null) || return 1
  pid=$(jq -r '.pid // empty' "$ZRUN_RECORD" 2>/dev/null) || return 1
  [[ -n "$pid" && "$host" == "$(hostname)" ]] || return 1
  kill -0 "$pid" 2>/dev/null || return 1
  ps -p "$pid" -o command= 2>/dev/null | grep -q zloop || return 1
  echo "$pid"
}
