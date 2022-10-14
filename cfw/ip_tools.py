"""
    Get and handle socket connections.
"""

import yaml
import pprint
import subprocess

import pandas as pd

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
pprint.pprint(config)


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
