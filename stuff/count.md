# Count

Count things and persist the result.

```bash
MEMBERS=$(wc -l < members.txt | tr -d ' ')
STUFF=$(ls stuff/ | wc -l | tr -d ' ')
echo "Members: $MEMBERS" | tee -a .out/log.txt
echo "Stuff: $STUFF" | tee -a .out/log.txt
# Store counts for later
echo "$MEMBERS" > .out/member-count.txt
echo "$STUFF" > .out/stuff-count.txt
# Call next in chain
sed -n '/^```bash$/,/^```$/p' stuff/report.md | sed '1d;$d' | bash
```

## Links
- [[persist.md]] - Chain root
- [[report.md]] - Next in chain
