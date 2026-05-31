#!/usr/bin/env python3
import socket, sys, concurrent.futures, os
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
    print("Usage: python "+sys.argv[0]+" <network> [start] [end]")
    print("Examples:")
    print("  python "+sys.argv[0]+" 192.168.1       # scans .1 to .254")
    print("  python "+sys.argv[0]+" 10.143.199 1 50 # scans .1 to .50")
    sys.exit(1)

net = sys.argv[1]
start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
end = int(sys.argv[3]) if len(sys.argv) > 3 else 254

print("[*] Scanning "+net+"."+str(start)+" to "+net+"."+str(end))
print("[*] Time: "+datetime.now().isoformat())
print("-"*50)

live = []
with concurrent.futures.ThreadPoolExecutor(50) as ex:
    futures = {ex.submit(scan, net+"."+str(i)): i for i in range(start, end+1)}
    for f in concurrent.futures.as_completed(futures):
        r = f.result()
        if r:
            print("[+] LIVE: "+r[0]+" (port "+str(r[1])+")")
            live.append(r)

print("-"*50)
print("[*] Done: "+str(len(live))+" hosts")

od = os.path.expanduser("~/hacking/labs/"+net+"_"+str(start)+"_"+str(end))
os.makedirs(od, exist_ok=True)
with open(od+"/live_hosts.txt","w") as f:
    f.write("# Host Discovery - "+net+"."+str(start)+"-"+str(end)+"\n")
    f.write("# "+datetime.now().isoformat()+"\n")
    for ip,p in live: f.write(ip+":"+str(p)+"\n")
print("[*] Saved: "+od+"/live_hosts.txt")
