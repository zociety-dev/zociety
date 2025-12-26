#!/bin/bash
set -ex

NAME="alice"
ROLE="builder"
GREETING="first agent joining"

echo "=== Creating DATA ==="
DATA=$(jq -n --arg role "$ROLE" --arg greeting "$GREETING" '{role: $role, greeting: $greeting}')
echo "DATA=$DATA"

echo "=== Getting state ==="
CURRENT=$(bin/zstate)
CYCLE=$(echo "$CURRENT" | jq -r '.cycle')
SEQ=$(echo "$CURRENT" | jq -r '.seq + 1')
echo "CYCLE=$CYCLE"
echo "SEQ=$SEQ"

echo "=== Building full event JSON ==="
TYPE="join"
AGENT="$NAME"
MEMBERS=1
RULES=0
STUFF=0
COMPLETE="false"

EVENT=$(jq -n \
  --arg type "$TYPE" \
  --arg agent "$AGENT" \
  --argjson cycle "$CYCLE" \
  --argjson seq "$SEQ" \
  --argjson members "$MEMBERS" \
  --argjson rules "$RULES" \
  --argjson stuff "$STUFF" \
  --argjson data "$DATA" \
  --arg complete "$COMPLETE" \
  '{
    z: 1,
    event: $type,
    cycle: $cycle,
    seq: $seq,
    agent: $agent,
    ts: (now | todate),
    state: {
      members: $members,
      rules: $rules,
      stuff: $stuff,
      complete: ($complete == "true")
    },
    data: $data
  }')

echo "EVENT=$EVENT"
