# """
#     Get and handle socket connections.
# """

# import time
# import yaml

# import numpy as np
# import pandas as pd
# from apscheduler.schedulers.background import BackgroundScheduler

# from .extensions import iptables, shell
# from .CFWError import ConfigurationCFWError

# with open("config.yaml") as f:
#     config = yaml.load(f, Loader=yaml.FullLoader)


# def get_ip() -> pd.DataFrame:
#     """
#         Get the current socket connection and convert it to a DataFrame.
#     """
#     text = shell("ss -Hntu | awk '{print $5,$6}' ")
#     data = []
#     for line in text.split("\n")[:-1]:
#         server, client = line.split(" ")
#         server_ip, server_port = server.split(":")
#         client_ip, client_port = client.split(":")
#         data.append([server_ip, server_port, client_ip, client_port])
#     data_df = pd.DataFrame(
#         data, 
#         columns=["server_ip", "server_port", "client_ip", "client_port"]
#     )
#     return data_df


# def load_config():
#     if not config.get("global"):
#         raise ConfigurationCFWError(
#             "'global' was not found in the yaml file."
#         )
#     if not config["global"].get("frequency"):
#         raise ConfigurationCFWError(
#             "'frequency' is not set in 'global'."
#         )
#     if not config["global"].get("max_num"):
#         raise ConfigurationCFWError(
#             "'max_num' is not set in 'global'."
#         )
#     if not config["global"].get("unblock"):
#         raise ConfigurationCFWError(
#             "'unblock' is not set in 'global'."
#         )


# def block_ips_run():
#     data = get_ip()
#     data = data.groupby(["client_ip"], as_index = False)["client_ip"].agg({
#         "num": np.size
#     }).sort_values(by="num", ascending=False, ignore_index=True)
#     ips = []
#     for index, row in data.iterrows():
#         if row["num"] > config["global"]["max_num"]:
#             ips.append(row["client_ip"])
#     for ip in ips:
#         iptables.block_ip(ip)


# load_config()

# sched = BackgroundScheduler(timezone="Asia/Shanghai")
# sched.add_job(
#     block_ips_run, 
#     'interval', 
#     seconds=config["global"]["frequency"]
# )
# sched.start()
