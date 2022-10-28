import httpx
import click
import pandas as pd

from cfw import shell, config, ParameterCFWError

# Show all columns and rows.
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.colheader_justify', 'center')


@click.group()
def cli():
    pass


"""
    ipv4
"""
@cli.command(help="allow port")
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


@cli.command(help="deny port")
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


@cli.command(help="status port")
def status():
    r = httpx.get(f"http://127.0.0.1:{config['port']}/status")
    data = r.json()["message"]
    if not data:
        return
    data = pd.DataFrame(data, columns=["port", "protocol"])
    print(data.sort_values("port").to_string(index=False))


"""
    ipv6
"""
@cli.command(help="allow port")
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


@cli.command(help="deny port")
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


@cli.command(help="status port")
def status6():
    r = httpx.get(f"http://127.0.0.1:{config['port']}/status6")
    data = r.json()["message"]
    if not data:
        return
    data = pd.DataFrame(data, columns=["port", "protocol"])
    print(data.sort_values("port").to_string(index=False))


if __name__ == '__main__':
    cli(obj={})
