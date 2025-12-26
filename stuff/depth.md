# Depth

Measure how deep the focus experiment goes.

## Depth Levels (updated cycle 2)
1. Surface - first cycle, setting up
2. Shallow - second cycle, patterns repeat ← WE ARE HERE
3. Medium - themes developing
4. Deep - unexpected connections
5. Profound - fundamental insights

## What We've Learned About Depth
- Depth 1 → 2: Structure repeats (same files: focus.md, depth.md, insight.md)
- The repetition IS the learning: focus creates consistency
- Each agent rediscovers the same structure independently

```bash
echo "=== Depth Check ==="
DEPTH=$(cat .out/focus-depth.txt 2>/dev/null || echo 2)
LEVELS=("Surface" "Shallow" "Medium" "Deep" "Profound")
IDX=$((DEPTH - 1))
if [[ $IDX -lt 5 ]]; then
  echo "Depth: $DEPTH - ${LEVELS[$IDX]}"
else
  echo "Depth: $DEPTH - Beyond Profound"
fi
```

## Links
- [[focus.md]] - Focus tracker
- [[insight.md]] - What we've learned
