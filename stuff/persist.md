# Persist

The root of the persistence chain - writes accumulated state.

```bash
mkdir -p .out
echo "=== Persistence Chain ===" | tee -a .out/log.txt
echo "Run at: $(date)" | tee -a .out/log.txt
echo "By: $(tail -1 members.txt)" | tee -a .out/log.txt
# Call next in chain
sed -n '/^```bash$/,/^```$/p' stuff/count.md | sed '1d;$d' | bash
echo "--- Chain complete ---" | tee -a .out/log.txt
```

## Links
- [[count.md]] - Next in chain
- [[report.md]] - Final output
