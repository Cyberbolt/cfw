"""
    Call the Linux iptables API.
"""

# import ipaddress
# import subprocess

# from ..CFWError import WhitelistCFWError


# def shell(cmd: str) -> str:
#     """
#         Execute a shell statement and return the output.
#     """
#     r = subprocess.run(
#         cmd, 
#         shell=True,
#         capture_output=True
#     )
#     return r.stdout.decode()


# class Whitelist(list):
    
#     def __init__(self, path: str):
#         """
#             path: Path to the whitelist file
#         """
#         with open(path, 'r') as f:
#             text = f.read()
#         for ip in text.splitlines():
#             try:
#                 ip = str(ipaddress.IPv4Address(ip))
#             except ipaddress.AddressValueError:
#                 try:
#                     ip = str(ipaddress.IPv4Network(ip))
#                 except ipaddress.NetmaskValueError:
#                     raise WhitelistCFWError("The whitelist ip format is incorrect.")
#             self.append(ip)

# whitelist = Whitelist("whitelist.txt")


# def block_ip(ip: str):
#     for ip_w in whitelist:
#         if ipaddress.IPv4Address(ip) in ipaddress.IPv4Network(ip_w):
#             print('sadasdasddsa')
#             return
#     shell(f"ipset add blacklist {ip}")


# shell("ipset create blacklist hash:net")
# shell("iptables -I INPUT -m set --match-set blacklist src  -p tcp -j DROP")


import subprocess


def shell(cmd: str) -> str:
    """
        Execute a shell statement and return the output.
    """
    r = subprocess.run(
        cmd, 
        shell=True,
        # capture_output=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"
    )
    # return r.stdout.decode()
    return r

def cfw_init():
    """
    cfw initialization, open port 22 and loopback address by default.
    """
    shell("iptables -A INPUT -p tcp --dport  22 -j ACCEPT")
    shell("iptables -P INPUT DROP")
    shell("iptables -P FORWARD DROP")
    shell("iptables -P OUTPUT DROP")
    shell("iptables -A INPUT -i lo -j ACCEPT")
    shell("iptables -A OUTPUT -o lo -j ACCEPT")
    shell("iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT")
    
def close_22():
    """
    close port 22
    """
    try:
        shell("iptables -D INPUT -p tcp --dport  22 -j ACCEPT")
        shell("iptables -A INPUT -p tcp --dport  22 -j DROP")
    except:
        pass

def open_22():
    """
    open port 22
    """
    try:
        shell("iptables -D INPUT -p tcp --dport  22 -j DROP")
        shell("iptables -A INPUT -p tcp --dport  22 -j ACCEPT")
    except:
        pass

def ddos_protection():
    """
    Use cfw for ddos protection.
    """
    # DOS
    shell("iptables -A INPUT -i eth0 -p tcp --syn -m connlimit --connlimit-above 15 -j DROP")
    shell("iptables -A INPUT -p tcp -m state --state ESTABLISHED,RELATED -j ACCEPT")
    
    # DDOS
    shell("iptables -A INPUT  -p tcp --syn -m limit --limit 12/s --limit-burst 24 -j DROP")  
    shell("iptables -A FORWARD -p tcp --syn -m limit --limit 1/s -j ACCEPT ")