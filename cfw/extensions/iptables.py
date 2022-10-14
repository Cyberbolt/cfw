import subprocess


def block_ip(ips: list):
    r = subprocess.run(
        "ss -Hntu | awk '{print $5,$6}' ", 
        shell=True,
        capture_output=True
    )
    text = r.stdout.decode()