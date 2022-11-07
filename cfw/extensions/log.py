import os
import csv
import subprocess

from clock_timer import timer

from ..config import config


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


class Log:
    
    def __init__(self):
        if not os.path.exists(config["log_file_path"]):
            path = config["log_file_path"].rsplit("/", 1)
            if len(path) > 1:
                dir, file_name = path
                os.mkdir(dir)
            with open(config["log_file_path"], "w") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["time", "type", "content"])
    
    def write(self, type: str, content: str):
        if config["log_max_lines"] != 0:
            lines_num = int(shell(f'wc -l {config["log_file_path"]}').split(' ', 1)[0])
            if lines_num > config["log_max_lines"]:
                shell(f'sed -i "2d" {config["log_file_path"]}')
        with open(config["log_file_path"], "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timer.get_current_time(), type, content])
