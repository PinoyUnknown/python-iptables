import iptc

def setup_firewall():
    table = iptc.Table(iptc.Table.FILTER)
    chain = iptc.Chain(table, "INPUT")

    table.autocommit = False
    chain.flush()

    # Default policy: DROP
    chain.set_policy("DROP")

    # Allow loopback
    rule_lo = iptc.Rule()
    rule_lo.in_interface = "lo"
    rule_lo.target = iptc.Target(rule_lo, "ACCEPT")
    chain.insert_rule(rule_lo)

    # Allow established connections
    rule_est = iptc.Rule()
    match = rule_est.create_match("conntrack")
    match.ctstate = "ESTABLISHED,RELATED"
    rule_est.target = iptc.Target(rule_est, "ACCEPT")
    chain.insert_rule(rule_est)

    # Allow SSH
    rule_ssh = iptc.Rule()
    rule_ssh.protocol = "tcp"
    match = rule_ssh.create_match("tcp")
    match.dport = "22"
    rule_ssh.target = iptc.Target(rule_ssh, "ACCEPT")
    chain.insert_rule(rule_ssh)

    table.commit()
    table.autocommit = True

if __name__ == "__main__":
    setup_firewall()
    print("[iptables] Firewall rules applied.")
