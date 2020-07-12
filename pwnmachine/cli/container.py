import click
import json
from io import StringIO
from contextlib import redirect_stdout
from tabulate import tabulate


@click.group(name="container")
def cli():
    """Manage containers"""


@cli.command()
def ls():
    """list all container"""
    to_print = []
    for service_name, service in pm.config["services"].items():
        first = True
        for container in service["containers"]:
            to_print.append([service_name if first else "", container])
            first = False
    print(tabulate(to_print, headers=["Service", "Container"]))

@cli.command()
@click.option(
    "--privileged", help="Give extended privileges to the command", is_flag=True
)
@click.argument("container_names", type=click.Choice(pm.container_names))
@click.argument("command", nargs=-1)
def exec(container_names, command, privileged):
    """Run a command in a running container"""
    if not command:
        command = ["bash"]
    pm.exec(container_names, command, privileged)


@cli.command()
@click.option("-f", help="Follow log output.", is_flag=True)
@click.option(
    "--tail",
    nargs=1,
    default="all",
    help='Number of lines to show from the end of the logs (default "all")',
)
@click.argument("container_names", nargs=-1, type=click.Choice(pm.container_names))
def logs(container_names, f, tail):
    """Fetch the logs of a container"""
    pm.logs(container_names, f, tail)


@cli.command()
@click.argument("container_names", nargs=-1, type=click.Choice(pm.container_names))
def build(container_names):
    """Build containers"""
    pm.build(container_names)


@cli.command()
@click.argument("container_names", nargs=-1, type=click.Choice(pm.container_names))
def start(container_names):
    """Start containers"""
    pm.start(container_names)


@cli.command()
@click.option("-t", help="Timeout before killing the service.", default=10)
@click.argument("container_names", nargs=-1, type=click.Choice(pm.container_names))
def stop(container_names, t):
    """Stop containers"""
    pm.stop(container_names, t)


@cli.command()
@click.option("-t", help="Timeout before killing the service.", default=10)
@click.argument("container_names", nargs=-1, type=click.Choice(pm.container_names))
def restart(container_names, t):
    """Restart containers"""

    pm.restart(container_names, t)
