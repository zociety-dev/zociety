#!/bin/bash
set -ex

NAME="alice"
ROLE="builder"
GREETING="first agent joining"

DATA=$(jq -nc --arg role "$ROLE" --arg greeting "$GREETING" '{role: $role, greeting: $greeting}')

echo "DATA is: [$DATA]"
echo "Length: ${#DATA}"
echo "Last char: ${DATA: -1}"

# Now call zevent
echo "Calling: bin/zevent join \"$NAME\" \"$GREETING\" \"$DATA\""
