#!/usr/bin/env python3
import socket, sys, concurrent.futures
from datetime import datetime

PORTS = [21,22,23,25,53,80,110,143,443,445,3306,3389,8080,8443]

def probe(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex((ip, port)) == 0
    except: return False

def scan(ip):
    for p in PORTS:
        if probe(ip, p): return ip, p
    return None

if len(sys.argv) != 2:
    print("Usage: python "+sys.argv[0]+" <network_prefix>"); sys.exit(1)

net = sys.argv[1]
print("[*] Scanning "+net+".0/24 ..."); print("-"*50)

live = []
with concurrent.futures.ThreadPoolExecutor(50) as ex:
    futures = {ex.submit(scan, net+"."+str(i)): i for i in range(1,255)}
    for f in concurrent.futures.as_completed(futures):
        r = f.result()
        if r:
            print("[+] LIVE: "+r[0]+" (port "+str(r[1])+")")
            live.append(r)

print("-"*50); print("[*] Done: "+str(len(live))+" hosts")

import os
od = os.path.expanduser("~/hacking/labs/"+net+"_0_24")
os.makedirs(od, exist_ok=True)
with open(od+"/live_hosts.txt","w") as f:
    f.write("# Host Discovery - "+net+".0/24\n# "+datetime.now().isoformat()+"\n")
    for ip,p in live: f.write(ip+":"+str(p)+"\n")
print("[*] Saved: "+od+"/live_hosts.txt")
