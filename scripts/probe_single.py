#!/usr/bin/env python3
import socket, sys

PORTS = [21,22,23,25,53,80,110,143,443,445,3306,3389,8080,8443]

if len(sys.argv) != 2:
    print("Usage: python "+sys.argv[0]+" <ip>"); sys.exit(1)

ip = sys.argv[1]
print("[*] Probing "+ip+" ...")

for p in PORTS:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            if s.connect_ex((ip, p)) == 0:
                try:
                    banner = s.recv(1024).decode('utf-8', errors='ignore').strip()[:100]
                except:
                    banner = "[no banner]"
                print("[+] Port "+str(p)+" OPEN - "+banner)
    except Exception as e:
        print("[-] Port "+str(p)+" error: "+str(e))

print("[*] Done.")
