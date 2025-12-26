#!/bin/bash
CURRENT=$(bin/zstate)
MEMBERS=$(echo "$CURRENT" | jq -r '.genesis.members')
TYPE="join"
case "$TYPE" in
  join) MEMBERS=$((MEMBERS + 1)) ;;
esac

echo "After increment, MEMBERS=$MEMBERS"
echo "Testing with argjson:"
jq -n --argjson members "$MEMBERS" '{members: $members}'
