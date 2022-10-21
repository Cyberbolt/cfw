"""
    Call the Linux iptables API.
"""

import ipaddress
import subprocess

from ..CFWError import *


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


class Iplist(list):
    
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
                    raise ListCFWError("The ip format is incorrect.")
            self.append(ip)

whitelist = Iplist("whitelist.txt")


def block_ip(ip: str):
    for ip_w in whitelist:
        if ipaddress.IPv4Address(ip) in ipaddress.IPv4Network(ip_w):
            return False
    r = shell(f"ipset add blacklist {ip}")
    if r != '':
        return False
    return True


def unblock_ip(ip: str):
    r = shell(f"ipset del blacklist {ip}")
    if r != '':
        return False
    return True


def cfw_init():
    if 'blacklist' in shell("iptables -L"):
        return False
    shell("iptables -F")
    port = shell("netstat -anp | grep ssh | awk '{print $4}' | awk 'NR==1{print}' | awk -F : '{print $2}'")
    if port != '\n':
        shell(f"iptables -A INPUT -p tcp --dport {port} -j ACCEPT")
        shell(f"iptables -A OUTPUT -p tcp --dport {port} -j ACCEPT")
        shell(f"iptables -A INPUT -p tcp -m multiport -s 0.0.0.0 --dports 0:{port-1}, {port+1}:65535 -j DROP")
        shell(f"iptables -A OUTPUT -p tcp -m multiport -s 0.0.0.0 --dports 0:{port-1}, {port+1}:65535 -j DROP")
        shell(f"iptables -A INPUT -p udp -m multiport -s 0.0.0.0 --dports 0:{port-1}, {port+1}:65535 -j DROP")
        shell(f"iptables -A OUTPUT -p udp -m multiport -s 0.0.0.0 --dports 0:{port-1}, {port+1}:65535 -j DROP")
    else:
        shell(f"iptables -A INPUT -p tcp -m multiport -s 0.0.0.0 --dports 0:65535 -j DROP")
        shell(f"iptables -A OUTPUT -p tcp -m multiport -s 0.0.0.0 --dports 0:65535 -j DROP")
        shell(f"iptables -A INPUT -p udp -m multiport -s 0.0.0.0 --dports 0:65535 -j DROP")
        shell(f"iptables -A OUTPUT -p udp -m multiport -s 0.0.0.0 --dports 0:65535 -j DROP")
    shell("ipset create blacklist hash:net timeout 2147483")
    shell("iptables -I INPUT -m set --match-set blacklist src -j DROP")
    shell("ipset restore -f cfw/data/ipset_blacklist.txt")
    return True
