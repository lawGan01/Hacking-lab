#!/usr/bin/env python3
import os, stat, subprocess, sys

KNOWN_VULN = [
    "nmap", "vim", "nano", "less", "more", "man", "awk", "perl", "python",
    "ruby", "php", "bash", "sh", "cp", "mv", "find", "xargs", "tar", "zip"
]

def scan_suid(search_path="/"):
    print("[*] Hunting SUID/SGID files in: " + search_path)
    print("-" * 60)
    
    try:
        result = subprocess.run(
            ["find", search_path, "-perm", "-4000", "-o", "-perm", "-2000"],
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
        
        is_root = (owner == 0)
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
        else:
            print("[ ] SUID/SGID: " + f)
    
    print("-" * 60)
    print("[*] Total SUID/SGID: " + str(total))
    print("[*] SUID: " + str(suid_count) + ", SGID: " + str(sgid_count))
    print("[*] High-risk candidates: " + str(len(suspicious)))
    
    if suspicious:
        print("\n[!!!] IMMEDIATE ATTENTION:")
        for f in suspicious:
            print("  " + f)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "/"
    scan_suid(path)
