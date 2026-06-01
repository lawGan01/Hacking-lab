#!/usr/bin/env python3
import os, stat, subprocess, sys

KNOWN_VULN = [
    "nmap", "vim", "nano", "less", "more", "man", "awk", "perl", "python",
    "ruby", "php", "bash", "sh", "cp", "mv", "find", "xargs", "tar", "zip"
]

def scan_suid():
    print("[*] Hunting SUID/SGID files...")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            ["find", "/", "-perm", "-4000", "-o", "-perm", "-2000"],
            capture_output=True, text=True, timeout=60
        )
        files = [f for f in result.stdout.strip().split("\n") if f]
    except Exception as e:
        print("[-] find command failed: " + str(e))
        return
    
    total = len(files)
    suid_count = 0
    sgid_count = 0
    suspicious = []
    
    for f in files:
        if not os.path.exists(f):
            continue
            
        mode = os.stat(f).st_mode
        owner = os.stat(f).st_uid
        
        # Check if root-owned
        is_root = (owner == 0)
        
        # Check for known vulnerable binaries
        basename = os.path.basename(f)
        is_known = basename in KNOWN_VULN
        
        if mode & stat.S_ISUID:
            suid_count += 1
        if mode & stat.S_ISGID:
            sgid_count += 1
            
        if is_root and is_known:
            suspicious.append(f)
            print("[!!!] ROOT-OWNED + KNOWN VULN: " + f)
        elif is_root:
            print("[!] Root-owned SUID: " + f)
        elif is_known:
            print("[*] Known binary (not root): " + f)
    
    print("-" * 60)
    print("[*] Total SUID/SGID: " + str(total))
    print("[*] SUID: " + str(suid_count) + ", SGID: " + str(sgid_count))
    print("[*] High-risk candidates: " + str(len(suspicious)))
    
    if suspicious:
        print("\n[!!!] IMMEDIATE ATTENTION:")
        for f in suspicious:
            print("  " + f)

if __name__ == "__main__":
    scan_suid()
