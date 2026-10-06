#!/usr/bin/python3
import subprocess
import sys

def run(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"[OK] {cmd}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {cmd}")
        sys.exit(1)

def main():
    print("Applying iptables rules...")
    # Example iptables rules — replace with your own
    run("iptables -F")
    run("iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT")
    run("iptables -A INPUT -p tcp --dport 22 -j ACCEPT")
    run("iptables -A INPUT -j DROP")

    print("Starting AnonSurf...")
    # ParrotOS / AnonSurf command
    run("anonsurf start")

    print("Firewall + AnonSurf startup complete.")

if __name__ == "__main__":
    main()