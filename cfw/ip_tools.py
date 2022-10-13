"""
    Get and handle socket connections.
"""

import json
import subprocess

import pandas as pd

with open('config.json') as f:
    config = json.load(f)


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
    data = [line.split(' ', 1) for line in text.split("\n")[:-1]]
    data_df = pd.DataFrame(data, columns=['server', 'client'])
    return data_df
