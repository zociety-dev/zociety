# Depth

Measure how deep the focus experiment goes.

## Depth Levels
1. Surface - first cycle, just setting up
2. Shallow - patterns starting to repeat
3. Medium - themes developing
4. Deep - unexpected connections
5. Profound - fundamental insights

```bash
echo "=== Depth Check ==="
DEPTH=$(cat .out/focus-depth.txt 2>/dev/null || echo 0)
echo "Current depth: $DEPTH"
LEVELS=("Surface" "Shallow" "Medium" "Deep" "Profound")
if [[ $DEPTH -lt 5 ]]; then
  echo "Level: ${LEVELS[$DEPTH]}"
else
  echo "Level: Beyond Profound"
fi
```

## Links
- [[focus.md]] - Focus tracker
- [[insight.md]] - What we've learned
