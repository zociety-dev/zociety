# shellcheck shell=bash
# zroute.sh: sourced by bin/zloop, bin/zevent and bin/zheap-death, never run
# (no exec bit, so bin/zprompt does not list it as a command).
#
# On the host in the zociety repo, git writes must reach the container as
# zociety-dev through bin/shims/git -> bin/zgit: hooks (gitleaks) run there,
# commits are signed with the container's key, and only zociety-dev can push.
# The shim only works first on PATH, and PATH is not ours to trust. A shell
# that put /opt/local/bin ahead of direnv's bin/shims ran cycle 42's last
# turns on the host (2026-10-18): three commits signed with the host's key,
# gitleaks missing for the stuff turns, every push and the PR refused. And
# an agent's Bash tool can re-export PATH from its own shell snapshot, so
# even a loop that fixed PATH for its turns saw one turn commit on the host.
# Every script that writes therefore puts the shim first for itself.
#
# Only for the repo direnv set up (ZOCIETY_ROOT is the cwd) or, without
# direnv, a clone of zociety-dev/zociety. Never in the container, where
# bin/zgit runs git directly, nor in the throwaway repos the test harnesses
# build (their cwd is not ZOCIETY_ROOT and they have no such origin).

zroute() {
  [[ -f /run/.containerenv || -f /.dockerenv || -n "${container:-}" ]] && return 0
  [[ -x bin/shims/git ]] || return 0
  if [[ "${ZOCIETY_ROOT:-}" == "$PWD" ]] \
    || { [[ -z "${ZOCIETY_ROOT:-}" ]] && git remote get-url origin 2>/dev/null | grep -q 'zociety-dev/zociety'; }; then
    export ZOCIETY_ROOT="$PWD"
    export PATH="$PWD/bin/shims:$PATH"
  fi
  return 0
}

zroute
