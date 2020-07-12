import click
import json
from io import StringIO
from contextlib import redirect_stdout
from tabulate import tabulate


@click.group(name="service")
def cli():
    """Manage Services"""

@cli.command()
def ls():
    """list all services"""
    print(tabulate([[name] for name in pm.service_names], headers=["Service"]))

@cli.command()
@click.argument("service_names", nargs=-1, type=click.Choice(pm.service_names))
def build(service_names):
    """Build services"""
    if not service_names:
        service_names = pm.service_names
    pm.build(pm.get_container_names_for_services(service_names))


@cli.command()
@click.argument("service_names", nargs=-1, type=click.Choice(pm.service_names))
def start(service_names):
    """Start services"""
    pm.start(pm.get_container_names_for_services(service_names))


@cli.command()
@click.option("-t", help="Timeout before killing the service.", default=10)
@click.argument("service_names", nargs=-1, type=click.Choice(pm.service_names))
def stop(service_names, t):
    """Stop services"""
    pm.stop(pm.get_container_names_for_services(service_names), t)


@cli.command()
@click.option("-t", help="Timeout before killing the service.", default=10)
@click.argument("service_names", nargs=-1, type=click.Choice(pm.service_names))
def restart(service_names, t):
    """Restart services"""

    pm.restart(pm.get_container_names_for_services(service_names), t)


@cli.command()
@click.option("-f", help="Follow log output.", is_flag=True)
@click.option(
    "--tail",
    nargs=1,
    default="all",
    help='Number of lines to show from the end of the logs (default "all")',
)
@click.argument("service_names", nargs=-1, type=click.Choice(pm.service_names))
def logs(service_names, f, tail):
    """Fetch the logs of a service"""
    pm.logs(pm.get_container_names_for_services(service_names), f, tail)
