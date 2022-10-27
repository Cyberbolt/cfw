"""
    Call the Linux iptables API.
"""

import os
import pickle
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


class Rules(list):
    """
        Data structure for storing iptables rules
    """
    
    def __init__(self):
        # If rules.list exists, load the previous configuration file.
        if os.path.exists("cfw/data/rules.list"):
            with open("cfw/data/rules.list", "rb") as f:
                self = pickle.load(f)
            return
        # New configuration file
        ssh_port = shell("netstat -anp | grep ssh | awk '{print $4}' | awk 'NR==1{print}' | awk -F : '{print $2}'")
        if ssh_port == '\n':
            ssh_port = None
        if ssh_port:
            self.append(f"iptables -A INPUT -p tcp --dport {ssh_port} -j ACCEPT")
            self.append(f"iptables -A OUTPUT -p tcp --dport {ssh_port} -j ACCEPT")
            self.append(f"iptables -A INPUT -i lo -j ACCEPT")
            self.append(f"iptables -A OUTPUT -o lo -j ACCEPT")
            self.append(f"iptables -P INPUT DROP")
            self.append(f"iptables -P FORWARD DROP")
            self.append(f"iptables -P OUTPUT DROP")
        else:
            self.append(f"iptables -A INPUT -i lo -j ACCEPT")
            self.append(f"iptables -A OUTPUT -o lo -j ACCEPT")
            self.append(f"iptables -P INPUT DROP")
            self.append(f"iptables -P FORWARD DROP")
            self.append(f"iptables -P OUTPUT DROP")
        self.append("iptables -I INPUT -m set --match-set blacklist src -j DROP")
        
    def add_tcp_port(self, port: str) -> bool:
        if f"iptables -A INPUT -p tcp --dport {port} -j ACCEPT" in self:
            return False
        self.insert(0, f"iptables -A INPUT -p tcp --dport {port} -j ACCEPT")
        self.insert(0, f"iptables -A OUTPUT -p tcp --dport {port} -j ACCEPT")
        return True
        
    def rm_tcp_port(self, port: str) -> bool:
        if f"iptables -A INPUT -p tcp --dport {port} -j ACCEPT" not in self:
            return False
        self.remove(f"iptables -A INPUT -p tcp --dport {port} -j ACCEPT")
        self.remove(f"iptables -A OUTPUT -p tcp --dport {port} -j ACCEPT")
        return True
        
    def add_udp_port(self, port: str) -> bool:
        if f"iptables -A INPUT -p udp --dport {port} -j ACCEPT" in self:
            return False
        self.insert(0, f"iptables -A INPUT -p udp --dport {port} -j ACCEPT")
        self.insert(0, f"iptables -A OUTPUT -p udp --dport {port} -j ACCEPT")
        return True
        
    def rm_udp_port(self, port: str) -> bool:
        if f"iptables -A INPUT -p udp --dport {port} -j ACCEPT" not in self:
            return False
        self.remove(f"iptables -A INPUT -p udp --dport {port} -j ACCEPT")
        self.remove(f"iptables -A OUTPUT -p udp --dport {port} -j ACCEPT")
        return True
        
    def save_rules(self):
        start = "*filter\n:INPUT ACCEPT [0:0]\n:FORWARD ACCEPT [0:0]\n:OUTPUT ACCEPT [0:0]\n"
        end = "COMMIT"
        content = ''
        for line in self:
            content += line + '\n'
        rules = start + content + end
        with open("cfw/data/rules.list", "wb") as f:
            pickle.dump(self, f)
        with open("/etc/iptables-cfw", "w") as f:
            f.write(rules)
        shell("iptables-restore < /etc/iptables-cfw")


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


def ipset_save():
    shell("ipset save blacklist -f cfw/data/ipset_blacklist.txt")


def cfw_init():
    shell("ipset create blacklist hash:net timeout 2147483")
    shell("ipset restore -f cfw/data/ipset_blacklist.txt")
