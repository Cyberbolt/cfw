import os
# Specify the interpreter running path as the cfw project directory.
current_path = os.path.dirname(__file__)
os.chdir(current_path)

import httpx
import click
import pandas as pd

from cfw import cmd, config, ParameterCFWError

# Show all columns and rows.
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.colheader_justify', 'center')


@click.group()
def cli():
    pass


"""
    ipv4 block / unblock
"""
@cli.command(help="Manually block a single ipv4.")
@click.argument("ip", type=str)
@click.option("-t", "--timeout", default=600, type=int)
def block(ip: str, timeout: int):
    if timeout > 2000000:
        raise ParameterCFWError("The maximum ban time cannot exceed 2,000,000 seconds. If you want to ban permanently, please use 0 instead.")
    r = httpx.get(f"http://127.0.0.1:{config['port']}/block_ip", 
                  params={"ip": ip, "timeout": timeout})
    if r.json()["code"]:
        pass
    else:
        print(r.json()["message"])
        

@cli.command(help="Manually unblock a single ipv4.")
@click.argument("ip", type=str)
def unblock(ip: str):
    r = httpx.get(f"http://127.0.0.1:{config['port']}/unblock_ip", 
                  params={"ip": ip})
    if r.json()["code"]:
        pass
    else:
        print(r.json()["message"])


@cli.command(help="View ipv4 blacklist.")
def blacklist():
    r = httpx.get(f"http://127.0.0.1:{config['port']}/blacklist")
    text = r.json()["message"]
    ips = []
    elements = text.split("Members:\n")[1].strip().split("\n")
    if elements[0] == '':
        return
    for element in elements:
        ip, timeout = element.split(" timeout ")
        ips.append([ip, timeout])
    data = pd.DataFrame(ips, columns=["blacklist", "timeout"])
    print(data.to_string(index=False))


"""
    ipv6 block / unblock
"""
@cli.command(help="Manually block a single ipv6.")
@click.argument("ip", type=str)
@click.option("-t", "--timeout", default=600, type=int)
def block6(ip: str, timeout: int):
    if timeout > 2000000:
        raise ParameterCFWError("The maximum ban time cannot exceed 2,000,000 seconds. If you want to ban permanently, please use 0 instead.")
    r = httpx.get(f"http://127.0.0.1:{config['port']}/block_ip6", 
                  params={"ip": ip, "timeout": timeout})
    if r.json()["code"]:
        pass
    else:
        print(r.json()["message"])
        

@cli.command(help="Manually unblock a single ipv6.")
@click.argument("ip", type=str)
def unblock6(ip: str):
    r = httpx.get(f"http://127.0.0.1:{config['port']}/unblock_ip6", 
                  params={"ip": ip})
    if r.json()["code"]:
        pass
    else:
        print(r.json()["message"])


@cli.command(help="View ipv6 blacklist.")
def blacklist6():
    r = httpx.get(f"http://127.0.0.1:{config['port']}/blacklist6")
    text = r.json()["message"]
    ips = []
    elements = text.split("Members:\n")[1].strip().split("\n")
    if elements[0] == '':
        return
    for element in elements:
        ip, timeout = element.split(" timeout ")
        ips.append([ip, timeout])
    data = pd.DataFrame(ips, columns=["blacklist6", "timeout"])
    print(data.to_string(index=False))


"""
    ipv4 port
"""
@cli.command(help="Allow ipv4 port.")
@click.argument("port", type=str)
def allow(port: str):
    try:
        if int(port) < 0 and int(port) > 65535:
            raise ParameterCFWError("The port number range can only be 0 to 65535.")
        r = httpx.get(f"http://127.0.0.1:{config['port']}/allow_port", 
                  params={"port": port, "protocol": "all"})
    except ValueError:
        try:
            port, protocol = port.split("/")
            if int(port) < 0 and int(port) > 65535:
                raise ParameterCFWError("The port number range can only be 0 to 65535.")
            if protocol != "tcp" and protocol != "udp":
                raise ParameterCFWError("The port protocol can only be tcp or udp.")
            r = httpx.get(f"http://127.0.0.1:{config['port']}/allow_port", 
                      params={"port": port, "protocol": protocol})
        except ValueError:
            raise ParameterCFWError("'cfw allow' syntax error.")
    if r.json()["code"]:
        pass
    else:
        print(r.json()["message"])


@cli.command(help="Block ipv4 port.")
@click.argument("port", type=str)
def deny(port: str):
    try:
        if int(port) < 0 and int(port) > 65535:
            raise ParameterCFWError("The port number range can only be 0 to 65535.")
        r = httpx.get(f"http://127.0.0.1:{config['port']}/deny_port", 
                  params={"port": port, "protocol": "all"})
    except ValueError:
        try:
            port, protocol = port.split("/")
            if int(port) < 0 and int(port) > 65535:
                raise ParameterCFWError("The port number range can only be 0 to 65535.")
            if protocol != "tcp" and protocol != "udp":
                raise ParameterCFWError("The port protocol can only be tcp or udp.")
            r = httpx.get(f"http://127.0.0.1:{config['port']}/deny_port", 
                      params={"port": port, "protocol": protocol})
        except ValueError:
            raise ParameterCFWError("'cfw deny' syntax error.")
    if r.json()["code"]:
        pass
    else:
        print(r.json()["message"])


@cli.command(help="View all allowed ipv4 ports.")
def status():
    r = httpx.get(f"http://127.0.0.1:{config['port']}/status")
    data = r.json()["message"]
    if not data:
        return
    data = pd.DataFrame(data, columns=["port", "protocol"])
    print(data.sort_values("port").to_string(index=False))


"""
    ipv6 port
"""
@cli.command(help="Allow ipv6 port.")
@click.argument("port", type=str)
def allow6(port: str):
    try:
        if int(port) < 0 and int(port) > 65535:
            raise ParameterCFWError("The port number range can only be 0 to 65535.")
        r = httpx.get(f"http://127.0.0.1:{config['port']}/allow_port6", 
                  params={"port": port, "protocol": "all"})
    except ValueError:
        try:
            port, protocol = port.split("/")
            if int(port) < 0 and int(port) > 65535:
                raise ParameterCFWError("The port number range can only be 0 to 65535.")
            if protocol != "tcp" and protocol != "udp":
                raise ParameterCFWError("The port protocol can only be tcp or udp.")
            r = httpx.get(f"http://127.0.0.1:{config['port']}/allow_port6", 
                      params={"port": port, "protocol": protocol})
        except ValueError:
            raise ParameterCFWError("'cfw allow' syntax error.")
    if r.json()["code"]:
        pass
    else:
        print(r.json()["message"])


@cli.command(help="Block ipv6 port.")
@click.argument("port", type=str)
def deny6(port: str):
    try:
        if int(port) < 0 and int(port) > 65535:
            raise ParameterCFWError("The port number range can only be 0 to 65535.")
        r = httpx.get(f"http://127.0.0.1:{config['port']}/deny_port6", 
                  params={"port": port, "protocol": "all"})
    except ValueError:
        try:
            port, protocol = port.split("/")
            if int(port) < 0 and int(port) > 65535:
                raise ParameterCFWError("The port number range can only be 0 to 65535.")
            if protocol != "tcp" and protocol != "udp":
                raise ParameterCFWError("The port protocol can only be tcp or udp.")
            r = httpx.get(f"http://127.0.0.1:{config['port']}/deny_port6", 
                      params={"port": port, "protocol": protocol})
        except ValueError:
            raise ParameterCFWError("'cfw deny' syntax error.")
    if r.json()["code"]:
        pass
    else:
        print(r.json()["message"])


@cli.command(help="View all allowed ipv6 ports.")
def status6():
    r = httpx.get(f"http://127.0.0.1:{config['port']}/status6")
    data = r.json()["message"]
    if not data:
        return
    data = pd.DataFrame(data, columns=["port", "protocol"])
    print(data.sort_values("port").to_string(index=False))


"""
    Log
"""
@cli.command(help="Dynamic query log.")
@click.argument("num", type=str)
def log(num: int = 1000):
    cmd(f"tail -f -n {num} {config['log_file_path']}")


if __name__ == '__main__':
    cli(obj={})
