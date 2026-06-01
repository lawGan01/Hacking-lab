#!/usr/bin/env python3
import sys, stat, os

def decode_mode(path):
    mode = os.stat(path).st_mode
    perms = stat.filemode(mode)
    print(path + " -> " + perms)
    
    # Decode numeric
    numeric = oct(mode)[-3:]
    print("  Numeric: " + numeric)
    
    # Special bits
    if mode & stat.S_ISUID: print("  [SETUID] - potential privesc vector")
    if mode & stat.S_ISGID: print("  [SETGID]")
    if mode & stat.S_ISVTX: print("  [STICKY]")
    
    # Writable by others = DANGER
    if mode & stat.S_IWOTH:
        print("  [WARNING] World-writable!")

if len(sys.argv) < 2:
    print("Usage: python " + sys.argv[0] + " <file_or_dir>")
    sys.exit(1)

for p in sys.argv[1:]:
    if os.path.exists(p):
        decode_mode(p)
    else:
        print("[-] Not found: " + p)
