#!/bin/bash
# Credential Hunter - searches common credential patterns
# WARNING: Only run on systems you OWN

TARGET_DIR="${1:-~/storage}"
OUTDIR=~/hacking/labs/cred_hunt_$(date +%Y%m%d_%H%M%S)
mkdir -p $OUTDIR

echo "[*] Hunting credentials in: $TARGET_DIR"
echo "[*] Output: $OUTDIR"

# Patterns
PATTERNS="password|passwd|pwd|secret|token|api_key|apikey|access_key|private_key|ssh_key"

# Search
echo "[+] Searching files..."
find $TARGET_DIR -type f \( -name "*.txt" -o -name "*.conf" -o -name "*.cfg" -o -name "*.ini" -o -name "*.json" -o -name "*.xml" -o -name "*.yaml" -o -name "*.yml" -o -name "*.env" -o -name "*.sh" -o -name "*.py" \) 2>/dev/null | while read f; do
    matches=$(grep -inE "$PATTERNS" "$f" 2>/dev/null)
    if [ ! -z "$matches" ]; then
        echo "[!] HIT: $f"
        echo "=== $f ===" >> $OUTDIR/hits.txt
        echo "$matches" >> $OUTDIR/hits.txt
        echo "" >> $OUTDIR/hits.txt
    fi
done

# Count
count=$(wc -l < $OUTDIR/hits.txt 2>/dev/null || echo 0)
echo "[*] Done. Potential hits logged."
echo "[*] Review: $OUTDIR/hits.txt"
