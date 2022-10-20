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
            print('sadasdasddsa')
            return False
    shell(f"ipset add blacklist {ip}")
    return True
    

def unblock_ip(ip: str):
    pass


shell("ipset create blacklist hash:net")
shell("iptables -I INPUT -m set --match-set blacklist src  -p tcp -j DROP")
