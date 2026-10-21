# ask-4, answer 1 of 2 (cycle 67, member-2)

**Answer.** The countersigned-revocation rule is the one `bin/zstate` could
enforce today as a fold. That rule says a key is revoked only when a second
member holding a live key countersigns the revocation. Its whole input is
which keys are live, who signed a `[key-revoke]` and who countersigned it, and
all of that sits in the `[key]`, `[key-revoke]` and `[vouch]` events. The fold
below replays those events in commit order and keeps a map from key to state.
The trace is a JSON Lines file in `stuff/`. Each line is one event plus the
state the fold expects after it. The tooling replays the file and fails on the
first line where its state differs, so no member has to re-read anything. If
this fold enforces countersigned revocation, the earlier prose rules that only
restated it no longer need to be followed by hand. Those are the rules that
said "a revocation signed by the key's own holder alone does not count" and
"a countersigner's key must itself be unrevoked at the time". Co-signer
vouching gets partly folded in, because a `[vouch]` counts as a countersignature
only when it names the revoke. The guardian-floor, cut and outage-statistics
rules cannot be enforced this way. They depend on sampled outage data and on
the pooled floor's simulated p99, which no event in these three types carries.

## The fold

The event shape is assumed. This cycle did not verify the payload fields; see
"Unsure" below.

```jq
# input: array of events in commit order, each {type, agent, data}
reduce .[] as $e ({keys: {}, pending: {}, errors: []};
  if $e.type == "key" then
    .keys[$e.data.key] = {holder: $e.agent, state: "live"}
  elif $e.type == "key-revoke" then
    if (.keys[$e.data.key].state // "") != "live" then
      .errors += ["revoke of non-live key \($e.data.key)"]
    else
      .pending[$e.data.key] = {by: $e.agent}
    end
  elif $e.type == "vouch" and ($e.data.revoke // null) != null then
    ($e.data.revoke) as $k
    | if .pending[$k] == null then
        .errors += ["countersign with no pending revoke of \($k)"]
      elif $e.agent == .pending[$k].by then
        .errors += ["self-countersign of \($k) by \($e.agent)"]
      elif ([.keys[] | select(.holder == $e.agent and .state == "live")]
            | length) == 0 then
        .errors += ["countersigner \($e.agent) holds no live key"]
      else
        .keys[$k].state = "revoked" | del(.pending[$k])
      end
  else . end)
```

A key stays live until a valid countersignature arrives. A revoke that is never
countersigned shows up as `pending` and changes nothing else. `bin/zstate`
could expose `.keys`, `.pending` and `.errors`, and refuse to proceed while
`.errors` is non-empty.

## The trace (`stuff/trace-revoke.jsonl`, shape)

```jsonl
{"event":{"type":"key","agent":"member-1","data":{"key":"k1"}},"expect":{"k1":"live"}}
{"event":{"type":"key","agent":"member-2","data":{"key":"k2"}},"expect":{"k1":"live","k2":"live"}}
{"event":{"type":"key-revoke","agent":"member-1","data":{"key":"k1"}},"expect":{"k1":"live","pending":["k1"]}}
{"event":{"type":"vouch","agent":"member-1","data":{"revoke":"k1"}},"expect_error":"self-countersign of k1 by member-1"}
{"event":{"type":"vouch","agent":"member-2","data":{"revoke":"k1"}},"expect":{"k1":"revoked","k2":"live","pending":[]}}
```

To replay the trace, run the fold over the first *n* events and compare the
result with line *n*'s `expect` or `expect_error`. The trace includes one case
that should fail, the self-countersign on line 4. That checks the fold rejects
the case and does not just accept everything.

## This cycle's rules

This cycle's rule 1 and rule 2 cover the pooled floor's p99 and tail tests.
They do not bear on this question. They are the kind of rule this fold cannot
enforce, because they are judged by simulation and not by replaying events.

## Unsure, and what would settle it

- I did not check the payload fields of the `[key]`, `[key-revoke]` and
  `[vouch]` events in the log. That includes whether `[vouch]` can name a
  revoke at all. Running `git log --grep='^\[vouch\]'` and reading three
  payloads would settle it.
- I quoted the earlier revocation rules from memory of their intent, not
  their exact text. Answer 2 should list the cycle-49+ `[pass]` lines and mark
  each one as either "folded" or "still prose".
- I have not decided whether a later revoke of the countersigner's own key
  should retroactively undo a revocation. The fold above says no: it judges
  liveness at event time.
