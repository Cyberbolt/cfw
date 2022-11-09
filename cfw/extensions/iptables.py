"""
    Call the Linux iptables API.
"""

import os
import sys
import shutil
import pickle
import threading
import ipaddress
import subprocess

from .log import Log
from ..config import config
from ..CFWError import *

lock = threading.RLock()


def cmd(cmd: str):
    try:
        subprocess.run(
            cmd, 
            shell=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        sys.exit(1)


def shell(cmd: str) -> str:
    """
        Execute a shell statement and return the output.
    """
    r = subprocess.run(
        cmd, 
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return r.stdout.decode()


class Rules(list):
    """
        Data structure for storing iptables rules
    """
    
    version = ''
    
    def __init__(self, version: int = 4):
        self.data = []
        if version == 6:
            self.version = '6'
        elif version != 4:
            raise ParameterCFWError("The version number can only be 4 or 6.")
        # If rules.list exists, load the previous configuration file.
        if os.path.exists(f"cfw/data/rules{self.version}.list"):
            with open(f"cfw/data/rules{self.version}.list", "rb") as f:
                self.data = pickle.load(f)
            return
        # New configuration file
        ssh_port = shell("netstat -anp | grep ssh | awk '{print $4}' | awk 'NR==1{print}' | awk -F : '{print $2}'").rstrip()
        
        if ssh_port == '\n':
            ssh_port = None
        if ssh_port:
            self.data.append(f"-A INPUT -p tcp --dport {ssh_port} -j ACCEPT")
            self.data.append(f"-A OUTPUT -p tcp --sport {ssh_port} -j ACCEPT")
        self.data.append(f"-A INPUT -p tcp -m multiport -s 0.0.0.0 --dports 0:65535 -j DROP")
        self.data.append(f"-A OUTPUT -p tcp -m multiport -s 0.0.0.0 --dports 0:65535 -j DROP")
        self.data.append(f"-A INPUT -p udp -m multiport -s 0.0.0.0 --dports 0:65535 -j DROP")
        self.data.append(f"-A OUTPUT -p udp -m multiport -s 0.0.0.0 --dports 0:65535 -j DROP")
        # self.data.append(f"-P INPUT DROP")
        # self.data.append(f"-P FORWARD DROP")
        # self.data.append(f"-P OUTPUT DROP")
        
        self.data.append(f"-I INPUT -m set --match-set blacklist{self.version} src -j DROP")
        
    def add_tcp_port(self, port: str) -> bool:
        if f"-A INPUT -p tcp --dport {port} -j ACCEPT" in self.data:
            return False
        self.data.insert(0, f"-A INPUT -p tcp --dport {port} -j ACCEPT")
        self.data.insert(0, f"-A OUTPUT -p tcp --sport {port} -j ACCEPT")
        return True
        
    def rm_tcp_port(self, port: str) -> bool:
        if f"-A INPUT -p tcp --dport {port} -j ACCEPT" not in self.data:
            return False
        self.data.remove(f"-A INPUT -p tcp --dport {port} -j ACCEPT")
        self.data.remove(f"-A OUTPUT -p tcp --sport {port} -j ACCEPT")
        return True
        
    def add_udp_port(self, port: str) -> bool:
        if f"-A INPUT -p udp --dport {port} -j ACCEPT" in self.data:
            return False
        self.data.insert(0, f"-A INPUT -p udp --dport {port} -j ACCEPT")
        self.data.insert(0, f"-A OUTPUT -p udp --sport {port} -j ACCEPT")
        return True
        
    def rm_udp_port(self, port: str) -> bool:
        if f"-A INPUT -p udp --dport {port} -j ACCEPT" not in self.data:
            return False
        self.data.remove(f"-A INPUT -p udp --dport {port} -j ACCEPT")
        self.data.remove(f"-A OUTPUT -p udp --sport {port} -j ACCEPT")
        return True
        
    def save_rules(self):
        start = "*filter\n"
        end = "COMMIT\n"
        content = ''
        for line in self.data:
            content += line + '\n'
        rules = start + content + end
        with open(f"cfw/data/rules{self.version}-backup.list", "wb") as f:
            pickle.dump(self.data, f)
        shutil.move(f"cfw/data/rules{self.version}-backup.list", 
                    f"cfw/data/rules{self.version}.list")
        with open(f"cfw/data/ip{self.version}tables-cfw-backup", "w") as f:
            f.write(rules)
        shutil.move(f"cfw/data/ip{self.version}tables-cfw-backup", 
                    f"cfw/data/ip{self.version}tables-cfw")
        shell(f"ip{self.version}tables-restore < cfw/data/ip{self.version}tables-cfw")


class Iplist(list):
    
    version = ''
    
    def __init__(self, path: str, version: int = 4):
        """
            path: Path to the whitelist file
        """
        if version == 6:
            self.version = 6
        elif version == 4:
            self.version = 4
        else:
            raise ParameterCFWError("The version number can only be 4 or 6.")
        self.load(path)
        
    def load(self, path: str):
        """
            Load the black and white list.
        """
        with open(path, 'r') as f:
            text = f.read()
        for ip in text.splitlines():
            if self.version == 4:
                try:
                    ip = str(ipaddress.IPv4Address(ip))
                except ipaddress.AddressValueError:
                    try:
                        ip = str(ipaddress.IPv4Network(ip))
                    except ipaddress.NetmaskValueError:
                        raise ListCFWError("The ip format is incorrect.")
                self.append(ip)
            elif self.version == 6:
                try:
                    ip = str(ipaddress.IPv6Address(ip))
                except ipaddress.AddressValueError:
                    try:
                        ip = str(ipaddress.IPv6Network(ip))
                    except ipaddress.NetmaskValueError:
                        raise ListCFWError("The ip format is incorrect.")
                self.append(ip)


whitelist = Iplist(config["whitelist"])
whitelist6 = Iplist(config["whitelist6"], version=6)
log = Log()


def block_ip(ip: str, timeout: int = 600, type: str = 'cfw'):
    for ip_w in whitelist:
        if ipaddress.IPv4Address(ip) in ipaddress.IPv4Network(ip_w):
            return {
                "code": 0,
                "message": "This ip is in the whitelist and cannot be blocked."
            }
    r = shell(f"ipset add blacklist {ip} timeout {timeout}")
    if r != '':
        return {
            "code": 0,
            "message": "This ip has been blocked."
        }
    log.write(type, f"block {ip}")
    return {
        "code": 1
    }


def unblock_ip(ip: str, type: str = 'cfw'):
    r = shell(f"ipset del blacklist {ip}")
    if r != '':
        return {
            "code": 0,
            "message": "The ip is not blocked."
        }
    log.write(type, f"unblock {ip}")
    return {
        "code": 1
    }


def block_ip6(ip: str, timeout: int = 600, type: str = 'cfw'):
    for ip_w in whitelist6:
        if ipaddress.IPv6Address(ip) in ipaddress.IPv6Network(ip_w):
            return {
                "code": 0,
                "message": "This ip is in the whitelist and cannot be blocked."
            }
    r = shell(f"ipset add blacklist6 {ip} timeout {timeout}")
    if r != '':
        return {
            "code": 0,
            "message": "This ip has been blocked."
        }
    log.write(type, f"block {ip}")
    return {
        "code": 1
    }


def unblock_ip6(ip: str, type: str = 'cfw'):
    r = shell(f"ipset del blacklist6 {ip}")
    if r != '':
        return {
            "code": 0,
            "message": "The ip is not blocked."
        }
    log.write(type, f"unblock {ip}")
    return {
        "code": 1
    }


def ipset_save():
    lock.acquire()
    shell("ipset save blacklist -f cfw/data/ipset_blacklist-backup.txt")
    lock.release()
    shell("mv cfw/data/ipset_blacklist-backup.txt cfw/data/ipset_blacklist.txt")
    

def ipset6_save():
    lock.acquire()
    shell("ipset save blacklist6 -f cfw/data/ipset_blacklist6-backup.txt")
    lock.release()
    shell("mv cfw/data/ipset_blacklist6-backup.txt cfw/data/ipset_blacklist6.txt")


def cfw_init():
    if not os.path.exists("cfw/data/ipset_blacklist.txt"):
        shell("ipset create blacklist hash:net timeout 2147483")
    else:
        shell("ipset restore -f cfw/data/ipset_blacklist.txt")
        
    if not os.path.exists("cfw/data/ipset_blacklist6.txt"):
        shell("ipset create blacklist6 hash:net family inet6 timeout 2147483")
    else:
        shell("ipset restore -f cfw/data/ipset_blacklist6.txt")
