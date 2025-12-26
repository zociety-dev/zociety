# Report

Generate a summary from persisted data.

```bash
echo "=== Report ===" | tee -a .out/log.txt
if [[ -f .out/member-count.txt ]]; then
  echo "Total members across runs: $(cat .out/member-count.txt)" | tee -a .out/log.txt
fi
echo "Log entries: $(wc -l < .out/log.txt | tr -d ' ')" | tee -a .out/log.txt
```

## Links
- [[count.md]] - Caller
- [[persist.md]] - Chain root
