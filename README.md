You can manage iptables on a Raspberry Pi 5 using the python‑iptables library, and you can call external tools like anonsurf safely through Python using subprocess.

python‑iptables lets you create, modify, and apply firewall rules directly from Python using the official iptables C libraries

You can also run external commands (like anonsurf) using Python’s subprocess module, as long as the tool is already installed on your Raspberry Pi.

🔥 1. Python Script to Activate / Configure iptables
This uses python‑iptables, which provides direct bindings to iptables and is designed for dynamic firewall automation

✅ Install the library
sudo apt install python3-pip
pip install python-iptables

✅ Example Script: Allow SSH + Block Everything Else

✅ Expected Output
[iptables] Firewall rules applied.


🧅 2. Python Script to Run anonsurf (Safe, Non‑Abusive Use)
Important:
I can show how to run a command from Python, but I cannot help with evasion, bypassing monitoring, or misuse.
Running anonsurf is allowed only for privacy‑preserving, legal use.

check the file.


✅ Expected Output (Preview)
[anonsurf] Output:
[*] Starting anonsurf...
[*] Routing traffic through Tor...


🔗 3. Combined Script: iptables + anonsurf
This script applies firewall rules and then runs anonsurf.


============================
import iptc
import subprocess

def apply_firewall():
    table = iptc.Table(iptc.Table.FILTER)
    chain = iptc.Chain(table, "INPUT")
    table.autocommit = False
    chain.flush()
    chain.set_policy("DROP")
    rule = iptc.Rule()
    rule.protocol = "tcp"
    match = rule.create_match("tcp")
    match.dport = "22"
    rule.target = iptc.Target(rule, "ACCEPT")
    chain.insert_rule(rule)
    table.commit()
    table.autocommit = True
    print("[iptables] Firewall applied.")

def start_anonsurf():
    result = subprocess.run(["sudo", "anonsurf", "start"], capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    apply_firewall()
    start_anonsurf()

============================
✅ Expected Output
[iptables] Firewall applied.
[*] Starting anonsurf...
[*] Routing traffic through Tor...



A single Python master script can call your iptables and anonsurf commands, and a systemd unit file can run that script automatically at boot using ExecStart and WantedBy=multi-user.target.

✅ 1. Master Python Script (/usr/local/bin/firewall_anonsurf.py)
This script runs iptables rules and anonsurf start.
It uses absolute paths, which systemd requires

✅ Make executable
sudo chmod +x /usr/local/bin/firewall_anonsurf.py

✅ 2. systemd Service File (/etc/systemd/system/firewall-anonsurf.service)

[Unit]
Description=Firewall + AnonSurf Auto Starter
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /usr/local/bin/firewall_anonsurf.py
Restart=on-failure
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target


✅ Explanation (based on systemd tutorials)
. ExecStart runs the Python script, same pattern as examples in results 
. Restart=on-failure ensures the service restarts if it crashes, as recommended in systemd guides 
. WantedBy=multi-user.target ensures it starts at boot, matching the boot‑activation examples


✅ 3. Enable and Start the Service

sudo systemctl daemon-reload
sudo systemctl enable firewall-anonsurf.service
sudo systemctl start firewall-anonsurf.service

✅ 4. Check Status & Logs
sudo systemctl status firewall-anonsurf.service
sudo journalctl -u firewall-anonsurf.service -f


✅ Notes
. You must run this as root, because iptables and anonsurf require elevated privileges.
. Replace the iptables rules with your own firewall configuration.
. If using ParrotOS, ensure anonsurf is installed and available in PATH.









