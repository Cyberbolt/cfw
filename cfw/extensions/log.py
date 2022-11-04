import os
import csv

from clock_timer import timer

from ..config import config


class Log:
    
    def __init__(self):
        if not os.path.exists(config["log_file_path"]):
            with open(config["log_file_path"], "w") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["time", "type", "content"])
    
    def write(self, type: str, content: str):
        with open(config["log_file_path"], "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timer.get_current_time(), type, content])
