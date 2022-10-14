"""
    Get and handle socket connections.
"""

import yaml
import subprocess

import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler

from .CFWError import ConfigurationCFWError

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

r = subprocess.run(
    "ipset create blacklist hash:ip", 
    shell=True,
    capture_output=True
)
text = r.stdout.decode()


def get_ip() -> pd.DataFrame:
    """
        Get the current socket connection and convert it to a DataFrame.
    """
    r = subprocess.run(
        "ss -Hntu | awk '{print $5,$6}' ", 
        shell=True,
        capture_output=True
    )
    text = r.stdout.decode()
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


def load_config():
    if not config.get("global"):
        raise ConfigurationCFWError(
            "'global' was not found in the yaml file."
        )
    if not config["global"].get("frequency"):
        raise ConfigurationCFWError(
            "'frequency' is not set in 'global'."
        )
    if not config["global"].get("max_num"):
        raise ConfigurationCFWError(
            "'max_num' is not set in 'global'."
        )
    if not config["global"].get("unblock"):
        raise ConfigurationCFWError(
            "'unblock' is not set in 'global'."
        )
    


load_config()