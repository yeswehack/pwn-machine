#!/usr/bin/env python3
import click
import os
import subprocess
import shlex
import yaml
import sys
import click
import json
import os
import shutil
from glob import glob
from textwrap import dedent
from pprint import pprint
from .PwnMachine.PwnMachine import PwnMachine
from .PwnMachine.utils import hl, check_output
from .install import install_pwn_machine
import dns.resolver

base_plugin_folder = os.path.join(os.path.dirname(__file__), "cli")


class PluginLoader(click.MultiCommand):
    def __init__(self, *plugin_folders):
        super().__init__()
        self.plugin_folders = plugin_folders

    def list_commands(self, ctx):
        commands = []
        for plugin_folder in self.plugin_folders:
            commands.extend(
                os.path.basename(filename)[:-3]
                for filename in glob(os.path.join(plugin_folder, "*.py"))
            )
        return sorted(commands)

    def find_first_match(self, name):
        for plugin_folder in self.plugin_folders:
            fn = os.path.join(plugin_folder, name + ".py")
            if os.path.isfile(fn):
                return fn
        return None

    def get_command(self, ctx, name):
        ns = {"pm": pm}
        fn = self.find_first_match(name)
        if not fn:
            exit(f"ERROR: Invalid command {name}")
        try:
            with open(fn) as f:
                code = compile(f.read(), fn, "exec")
                eval(code, ns, ns)
        except FileNotFoundError:
            exit(f"ERROR: Invalid command {name}")
        if "cli" not in ns:
            click.echo(f"Error while loading {fn}, cli not found", err=True)
            raise click.Abort()
        return ns["cli"]


@click.group()
def setup_only():
    pass


@click.group()
def main_cli():
    pass


@setup_only.command()
def version():
    from . import __version__   
    click.echo(__version__)


@setup_only.command()
def setup():
    """Setup pwn machine"""
    try:
        install_pwn_machine()
    except click.Abort:
        click.echo("Aborting", err=True)
        exit(1)


@main_cli.command()
def setup():
    """Setup pwn machine"""
    try:
        install_pwn_machine()
    except click.Abort:
        click.echo("Aborting", err=True)
        exit(1)


@main_cli.command()
def version():
    from . import __version__
    click.echo(__version__)


@main_cli.command()
def env():
    """Display the commands to set up the environment for the Docker client"""
    pm.env()


@main_cli.command()
@click.argument("command", nargs=-1)
def ssh(command):
    """SSH to the host"""
    pm.ssh([] if command is None else command)


if os.environ["PM_PATH"]:
    pm = PwnMachine(os.environ["PM_PATH"])

    @main_cli.command()
    @click.argument("services", nargs=-1, type=click.Choice(pm.service_names))
    @click.pass_context
    def ps(context, services):
        """List services"""
        pm.ps(services)

    plugin_folder = os.path.join(os.environ["PM_PATH"], "cli")
    cli = click.CommandCollection(
        sources=[main_cli, PluginLoader(base_plugin_folder, plugin_folder)]
    )
else:
    cli = setup_only


if __name__ == "__main__":
    if "PM_PATH" in os.environ and os.environ["PM_PATH"]:
        cli()
    else:
        click.echo("PM_PATH is not present is the environment.")
        if click.confirm(
            "Do you want to install pwn-machine ?", abort=True, default=True
        ):
            setup()
