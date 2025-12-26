#!/bin/bash
set -ex

CURRENT=$(bin/zstate)
echo "CURRENT: $CURRENT"

CYCLE=$(echo "$CURRENT" | jq -r '.cycle')
SEQ=$(echo "$CURRENT" | jq -r '.seq + 1')

echo "CYCLE: '$CYCLE'"
echo "SEQ: '$SEQ'"

echo "Testing argjson with these values:"
jq -n --argjson cycle "$CYCLE" --argjson seq "$SEQ" '{cycle: $cycle, seq: $seq}'
