#!/bin/bash
# Recon Pipeline - Week 1 Day 3
# One target, one command, full intelligence

TARGET=$1
if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target.com>"
    exit 1
fi

OUTDIR=~/hacking/labs/recon_$(echo $TARGET | tr '.' '_')_$(date +%Y%m%d_%H%M%S)
mkdir -p $OUTDIR

echo "[*] Target: $TARGET"
echo "[*] Output: $OUTDIR"
echo "[*] Started: $(date)"
echo "=================================================="

# 1. DNS
echo "[+] DNS Records"
host $TARGET > $OUTDIR/dns.txt 2>&1
dig +short $TARGET >> $OUTDIR/dns.txt 2>&1
cat $OUTDIR/dns.txt

# 2. Whois
echo ""
echo "[+] Whois"
whois $TARGET > $OUTDIR/whois.txt 2>&1
head -20 $OUTDIR/whois.txt

# 3. HTTP Headers
echo ""
echo "[+] HTTP Headers"
curl -I -s --max-time 10 http://$TARGET > $OUTDIR/headers_http.txt 2>&1
curl -I -s --max-time 10 https://$TARGET > $OUTDIR/headers_https.txt 2>&1
echo "--- HTTP ---"
cat $OUTDIR/headers_http.txt
echo "--- HTTPS ---"
cat $OUTDIR/headers_https.txt

# 4. Subdomains via crt.sh
echo ""
echo "[+] Subdomains (crt.sh)"
curl -s "https://crt.sh/?q=%.$TARGET&output=json" 2>/dev/null | \
    python3 -c "import sys,json; [print(r['name_value']) for r in json.load(sys.stdin)]" 2>/dev/null | \
    sort -u > $OUTDIR/subdomains.txt
wc -l $OUTDIR/subdomains.txt | awk '{print "[*] Found: " $1 " subdomains"}'

# 5. Port Scan (top 100)
echo ""
echo "[+] Port Scan (top 100)"
nmap -sT --top-ports 100 --open $TARGET > $OUTDIR/nmap.txt 2>&1
cat $OUTDIR/nmap.txt

echo ""
echo "=================================================="
echo "[*] Recon complete. Results in: $OUTDIR"
echo "[*] Files:"
ls -la $OUTDIR
