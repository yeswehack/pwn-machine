import subprocess
import shlex
import io
import os
import json
from tqdm import tqdm
from pprint import pprint
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from compose.service import Service
from compose.cli.main import project_from_options, Environment
from collections import ChainMap
import click

def hl(color, s):
    return click.style(s, fg=color)

def check_call(*args, **kwargs):
    try:
        subprocess.run(*args, check=True, **kwargs)
    except subprocess.CalledProcessError:
        return False
    except KeyboardInterrupt:
        return False
    return True


def check_output(*args, **kwargs):
    try:
        return subprocess.check_output(*args, **kwargs).decode("utf8")
    except subprocess.CalledProcessError:
        return None


def slugify(name):
    return name.replace("*.", "wildcard_").replace(".", "-")


def print_stream(stream):
    progress = {}
    for line in stream:
        line = json.loads(line)
        if "stream" in line:
            tqdm.write(line["stream"], end="")
        elif "status" in line:
            if "id" not in line:
                continue
            if line["id"] not in progress:
                progress[line["id"]] = tqdm(leave=False)
            p = progress[line["id"]]
            if "progress" not in line:
                p.display(line["status"])
            else:
                p.set_description(line["status"])
                p.display(line["status"] + ": " + line["progress"])
    for p in progress.values():
        p.close()
    print()


def get_machine_options(machine_name):
    output = check_output(["docker-machine", "config", "--", machine_name])
    if output is None:
        exit(f'Unknow machine "{machine_name}"')
    options = {}
    for quoted_line in output.strip().split("\n"):
        line = shlex.split(quoted_line)[0]
        if "=" in line:
            name, _, value = line.partition("=")
            if name == "-H":
                name = "--host"
            options[name] = value
        else:
            options[line] = True
    return options


def parse_compose_project(project_dir, machine_name, name, compose_files):
    """ Parse the compose files """
    machine_options = get_machine_options(machine_name)
    compose_options = {
        **machine_options,
        "--file": compose_files,
        "--project-name": name,
        "--project-directory": project_dir,
    }

    # out = io.StringIO()
    # with redirect_stderr(out):
    project = project_from_options(project_dir, compose_options)
    return project


@contextmanager
def monkey_patch(module, method_name, replacement):
    original = getattr(module, method_name)

    def handler(*args, **kwargs):
        return replacement(original, *args, **kwargs)

    try:
        setattr(module, method_name, handler)
        yield
    finally:
        setattr(module, method_name, original)


def extra_env(*extra_env):
    """ Add pwn-machine env to the docker-compose project"""

    def new_from_env_file(original, *args, **kwargs):
        env = original(*args, **kwargs)
        for extra in extra_env:
            env.update(extra)
        return env

    return monkey_patch(Environment, "from_env_file", new_from_env_file)


def fixed_relative_context():
    """Fix relative context in service docker-compose file """
    from compose.config import config

    def new_process_config_file(original, *args, **kwargs):
        config = original(*args, **kwargs)
        config_dir = os.path.dirname(config.filename)
        for service in config.config["services"].values():
            if "build" not in service:
                continue
            if isinstance(service["build"], str):
                fixed_path = os.path.join(config_dir, service["build"])
                service["build"] = os.path.realpath(fixed_path)
            elif "context" in service["build"]:
                fixed_path = os.path.join(config_dir, service["build"]["context"])
                service["build"]["context"] = os.path.realpath(fixed_path)
        return config

    return monkey_patch(config, "process_config_file", new_process_config_file)
