#!/bin/bash
set -ex

ROLE="builder"
GREETING="first agent joining"

DATA=$(jq -n --arg role "$ROLE" --arg greeting "$GREETING" '{role: $role, greeting: $greeting}')

echo "DATA: $DATA"
echo "Testing argjson with DATA:"
jq -n --argjson data "$DATA" '{data: $data}'
