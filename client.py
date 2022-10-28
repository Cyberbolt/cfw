import httpx
import click

from cfw import shell, config, ParameterCFWError


@click.group()
def cli():
    pass


@cli.command(help="foreground running cfw (blocking)")
@click.option("--port", "-p", default=6680, help="cfw run port")
def run(port):
    shell(f"uvicorn server:app --port {port}")


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
    data.sort()
    for element in data:
        print(element)


if __name__ == '__main__':
    cli(obj={})
