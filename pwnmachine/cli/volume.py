import click
from tabulate import tabulate

@click.group(name="volume")
def cli():
    """Manage Volumes"""


@cli.command()
def ls():
    """list all volumes"""
    print(tabulate([[name] for name in pm.volume_names], headers=["Volume"]))


@cli.command()
@click.argument("volume_names", nargs=-1, type=click.Choice(pm.volume_names))
def backup(volume_names):
    """backup a volume locally"""
    if volume_names is None:
        volume_names = pm.volume_names
    for name in volume_names:
        pm.backup(name)


@cli.command()
def restore():
    """restore a volume backup"""
    exit("NOT IMPLEMENTED")


@cli.command()
@click.argument("volume_name", type=click.Choice(pm.volume_names))
@click.argument(
    "mountpoint", required=False, type=click.Path(exists=True, file_okay=False)
)
def mount(volume_name, mountpoint=None):
    """Mount a remote volume locally, and start a shell.
       The volume is unmounted when the shell is closed. 
       
       If no mountpoint is specified, a tempdir will be created in /tmp
    """
    pm.mount(volume_name, mountpoint)
