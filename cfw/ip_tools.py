"""
    Get and handle socket connections.
"""

import ipaddress
import multiprocessing
from typing import Tuple
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler

from .config import config
from .extensions import iptables, shell
from .CFWError import ListCFWError

executor = ThreadPoolExecutor(
    max_workers = multiprocessing.cpu_count() * 2 + 1
)


def get_ss_ip() -> pd.DataFrame:
    """
        Get the current socket connection and convert it to a DataFrame.
    """
    text = shell("ss -Hntu | awk '{print $5,$6}' ")
    data = []
    for line in text.split("\n")[:-1]:
        server, client = line.split(" ")
        server_ip, server_port = server.split(":")
        client_ip, client_port = client.split(":")
        data.append([server_ip, server_port, client_ip, client_port])
    data_df = pd.DataFrame(
        data, 
        columns=["server_ip", "server_port", "client_ip", "client_port"]
    )
    return data_df


def block_blacklist_ip():
    blacklist = iptables.Iplist(config["blacklist"])
    for ip in blacklist:
        r = iptables.block_ip(ip, timeout=0)
        if r.get("message") == "This ip is in the whitelist and cannot be blocked.":
            raise ListCFWError(f"The '{ip}' of the blacklist exists in the whitelist.")
    
    blacklist6 = iptables.Iplist(config["blacklist6"])
    for ip in blacklist6:
        r = iptables.block_ip6(ip, timeout=0)
        if r.get("message") == "This ip is in the whitelist6 and cannot be blocked.":
            raise ListCFWError(f"The '{ip}' of the blacklist6 exists in the whitelist6.")


def block_ss_ip():
    data = get_ss_ip()
    data = data.groupby(["client_ip"], as_index = False)["client_ip"].agg({
        "num": np.size
    }).sort_values(by="num", ascending=False, ignore_index=True)
    ips = []
    for index, row in data.iterrows():
        if row["num"] > config["max_num"]:
            ips.append(row["client_ip"])
    for ip in ips:
        version = ipaddress.ip_address(ip).version
        if version == 4:
            # iptables.block_ip(ip, config["unblock_time"])
            executor.submit(iptables.block_ip, ip, config["unblock_time"])
        elif version == 6:
            # iptables.block_ip6(ip, config["unblock_time"])
            executor.submit(iptables.block_ip6, ip, config["unblock_time"])


def start() -> Tuple[iptables.Rules, iptables.Rules]:
    iptables.cfw_init()
    rules = iptables.Rules()
    rules6 = iptables.Rules(version=6)
    rules.save_rules()
    rules6.save_rules()
    
    block_blacklist_ip()

    sched = BackgroundScheduler(timezone="Asia/Shanghai")
    # ips are banned periodically.
    sched.add_job(
        block_ss_ip, 
        'interval', 
        seconds=config["frequency"],
        id="block_ss_ip"
    )
    # Save an ipset every 60 seconds.
    sched.add_job(
        iptables.ipset_save, 
        'interval', 
        seconds=config["backup_time"],
        id="iptables.ipset_save"
    )
    sched.add_job(
        iptables.ipset6_save, 
        'interval', 
        seconds=config["backup_time"],
        id="iptables.ipset6_save"
    )
    sched.start()
    print("CFW starts running.")
    return rules, rules6
