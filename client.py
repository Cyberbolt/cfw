import httpx
import click

from cfw import shell, config


@click.group()
def cli():
    pass


@cli.command(help="foreground running cfw (blocking)")
@click.option("--port", "-p", default=6680, help="cfw run port")
def run(port):
    shell(f"uvicorn server:app --port {port}")


@cli.command()
def start():
    pass


@cli.command(help="restart cfw")
def restart():
    r = httpx.get(f"http://127.0.0.1:{config['port']}/restart")
    print(r)


if __name__ == '__main__':
    cli(obj={})
