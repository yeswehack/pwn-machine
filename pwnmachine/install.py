import os
import click
import shutil
import yaml
from .PwnMachine.utils import check_output, check_call
from click._bashcomplete import get_completion_script


PM_COMMENT = "# PWN MACHINE"
PM_COMMENT_END = "# PWN MACHINE END"


def get_pm_offset(content):
    try:
        start = content.index(PM_COMMENT)
        end = content.index(PM_COMMENT_END) + len(PM_COMMENT_END) + 1  # \n
    except ValueError:
        return None
    return [start, end]


def update_rc(file_path, lines):
    with open(file_path, "r") as f:
        filerc = f.read()

    if PM_COMMENT in filerc:
        click.echo(f"pm is already installed in {file_path}")
        if not click.confirm("Do you want to update with the new configuration ?"):
            return

        offset = get_pm_offset(filerc)
        if offset is None:
            click.echo("Unable to find closing comment", err=True)
            raise click.Abort()
        filerc = filerc[: offset[0]] + filerc[offset[1] :]

    if filerc[-1] != "\n":
        filerc += "\n"

    lines = [PM_COMMENT, *lines, PM_COMMENT_END]
    filerc = filerc + "\n".join(lines) + "\n"

    with open(file_path, "w") as f:
        f.write(filerc)


def prepare_bash(pm_path):
    click.echo("bash detected")
    bash_autocomplete_path = os.path.join(pm_path, ".bash-autocomplete.sh")
    with open(bash_autocomplete_path, "w") as f:
        f.write(get_completion_script("pm", "_PM_COMPLETE", "bash"))
    bashrc_path = os.path.expanduser("~/.bashrc")

    lines = [
        f'export PM_PATH="{pm_path}"',
        f". {bash_autocomplete_path}",
    ]

    if click.confirm("Do you want pm to update your bashrc ?"):
        update_rc(bashrc_path, lines)
    else:
        click.echo("Add this to your bashrc to enable pm")
        click.echo("\n".join(lines))


def prepare_zshrc(pm_path):
    click.echo("zsh detected")
    zsh_autocomplete_path = os.path.join(pm_path, ".zsh-autocomplete.sh")
    with open(zsh_autocomplete_path, "w") as f:
        f.write(get_completion_script("pm", "_PM_COMPLETE", "zsh"))

    zshrc_path = os.path.expanduser("~/.zshrc")
    lines = [
        f'export PM_PATH="{pm_path}"',
        f". {zsh_autocomplete_path}",
    ]
    if click.confirm("Do you want pm to update your zshrc ?"):
        update_rc(zshrc_path, lines)
    else:
        click.echo("Add this to your zshrc to enable pm")
        click.echo("\n".join(lines))


def update_unknowrc(pm_path):
    click.echo("Unable to autoconfigure your shell")
    click.echo(f"Please set the env variable PM_PATH={pm_path} in your init file.")


def update_rc_files(pm_path):
    shell = os.environ.get("SHELL")
    if shell.endswith("bash"):
        prepare_bash(pm_path)
    elif shell.endswith("zsh"):
        prepare_zshrc(pm_path)
    # elif shell.endswith("fish")
    #    update_fishrc(pm_path)
    else:
        update_unknowrc(pm_path)


# update_rc_files("/home/bitk/bi.tk/")
# exit()


def get_machine_ip(machine_name):
    """
    run docker-machine ip {machine-name} and return the ip
    abort if the machine is not found
    """
    ip = check_output(["docker-machine", "ip", machine_name])
    if ip is None:
        click.echo(f"No machine with name {machine_name} can be found.", err=True)
        raise click.Abort()
    return ip.strip()


def check_ns(domain, machine_ip):
    """
    Check that the NS for the domain point to the machine_ip
    return True if it match, False if it doesn't
    """
    import dns.resolver

    def lookup():
        for ns_entry in dns.resolver.query(domain, "NS"):
            for a_entry in dns.resolver.query(ns_entry.target, "A"):
                if a_entry.address == machine_ip:
                    return True
        return False

    if not lookup():
        click.echo(
            f"The ip of the docker machine ({machine_ip}) and the nameserver ip for '{domain}' doesn't match."
        )
        click.confirm("Are you sure you want to continue ?", abort=True)


def copy_skel(pm_path):
    """
    copy default services to the destination folder
    """
    click.echo(f"Copying skel to {pm_path}")
    try:
        current_folder = os.path.dirname(__file__)
        shutil.copytree(os.path.join(current_folder, "skel"), pm_path)
    except Exception as e:
        click.echo(str(e), err=True)
        raise click.Abort()


def write_default_config(pm_path, config):
    """
    Write the yaml configuration file
    """
    config_path = os.path.join(pm_path, "config.yml")
    click.echo(f"Writing configuration file to {config_path}")
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def ask_config_info():
    pm_path = os.path.expanduser(
        click.prompt(
            "Where do you want to install PwnMachine ?",
            default="~/pwn-machine",
            type=click.Path(exists=False, writable=True),
        )
    )

    machine_name = click.prompt(
        "Please enter the name of your docker-machine.", default="pm"
    )
    machine_ip = click.prompt("Please enter your server public ip")
    domain = click.prompt("Please enter your domain name")
    check_ns(domain, machine_ip)
    email = click.prompt("Please enter the email address to use with Let's encrypt")

    config = {
        "version": 1.1,
        "docker-machine": machine_name,
        "domains": {domain: machine_ip},
        "environment": {
            "PDNS_API_KEY": os.urandom(16).hex(),
            "EMAIL": email,
            "LETSENCRYPT_URL": "https://acme-v02.api.letsencrypt.org/directory",
        },
        "services": {
            "traefik": {},
            "dns": {},
            "web": {
                "https": {"domains": [f"*.{domain}"]},
                "http": {"domains": [f"unsafe.{domain}"]},
            },
        },
    }
    return pm_path, config


def install_pwn_machine():
    pm_path, config = ask_config_info()
    copy_skel(pm_path)
    write_default_config(pm_path, config)
    update_rc_files(pm_path)
    click.echo(
        "PWN Machine is now installed, spawn new shell or set PM_PATH to get started."
    )

