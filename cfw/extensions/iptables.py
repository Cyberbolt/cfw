"""
    Call the Linux iptables API.
"""

import ipaddress
import subprocess

from ..CFWError import WhitelistCFWError


def shell(cmd: str) -> str:
    """
        Execute a shell statement and return the output.
    """
    r = subprocess.run(
        cmd, 
        shell=True,
        capture_output=True
    )
    return r.stdout.decode()


class Whitelist(list):
    
    def __init__(self, path: str):
        """
            path: Path to the whitelist file
        """
        with open(path, 'r') as f:
            text = f.read()
        for ip in text.splitlines():
            try:
                ip = str(ipaddress.IPv4Address(ip))
            except ipaddress.AddressValueError:
                try:
                    ip = str(ipaddress.IPv4Network(ip))
                except ipaddress.NetmaskValueError:
                    raise WhitelistCFWError("The whitelist ip format is incorrect.")
            self.append(ip)

whitelist = Whitelist("whitelist.txt")


def block_ip(ip: str):
    for ip_w in whitelist:
        if ipaddress.IPv4Address(ip) in ipaddress.IPv4Network(ip_w):
            return False
    r = shell(f"ipset add blacklist {ip}")
    if r:
        print(r)
    return True
    

def unblock_ip(ip: str):
    r = shell(f"ipset del blacklist {ip}")
    if r:
        print(r)
    return True

# cfw init
port = shell("netstat -anp | grep ssh | awk '{print $4}' | awk 'NR==1{print}' | awk -F : '{print $2}'")
shell(f"iptables -A INPUT -p tcp --dport {port} -j ACCEPT")
shell(f"iptables -A OUTPUT -p tcp --dport {port} -j ACCEPT")
shell("iptables -P INPUT DROP")
shell("iptables -P FORWARD DROP")
shell("iptables -P OUTPUT DROP")
shell("iptables -A INPUT -i lo -j ACCEPT")
shell("iptables -A OUTPUT -o lo -j ACCEPT")
shell("iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT")

shell("ipset create blacklist hash:net timeout 2147483")
shell("iptables -F")
shell("iptables -I INPUT -m set --match-set blacklist src -j DROP")
shell("ipset restore -f cfw/data/ipset_blacklist.txt")
