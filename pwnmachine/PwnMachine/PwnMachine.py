import yaml
import os
import sys
import json
from datetime import datetime
import tempfile
from pprint import pprint
from .utils import (
    check_call,
    check_output,
    parse_compose_project,
    fixed_relative_context,
    extra_env,
    get_machine_options,
    slugify,
)
from compose.service import Service
from compose.cli.main import (
    project_from_options,
    TopLevelCommand,
    log_printer_from_project,
    ConvergenceStrategy,
    BuildAction,
)
import docker
from compose.cli import signals
from compose.service import BuildError
from compose.cli.command import Environment
from .Pipeline import Pipelines
from compose.container import Container
from compose.config.errors import ConfigurationError
from contextlib import contextmanager
from .Config import parse_config
from .traefik import get_traefik_rules
from io import StringIO
from contextlib import redirect_stdout
import dockerpty
from dockerpty.pty import PseudoTerminal, RunOperation, ExecOperation


class DockerClient(docker.DockerClient):
    def __init__(self, api):
        self.api = api


class EmptyPwnMachine:
    pass


class PwnMachine:
    _project = None
    _cmd = None
    _client = None

    def __init__(self, pm_path):
        self.config_dir = pm_path
        config_file = os.path.join(pm_path, "config.yml")
        self.config = parse_config(self.config_dir, config_file)
        self.name = "pm"
        self.compose_files = [
            service["compose-file"] for service in self.config["services"].values()
        ]

    @property
    def client(self):
        if self._client is None:
            self._client = DockerClient(self.project.client)
        return self._client

    @property
    def project(self):
        if self._project is None:
            try:
                self._project = self.get_project(self.compose_files)
                self.apply_traefik_rules()
            except ConfigurationError as e:
                exit(e.msg)
        return self._project

    @property
    def cmd(self):
        if self._cmd is None:
            p = self.project
            cmd_options = {
                "--tlsverify": True,
                "--tlscacert": p.client.verify,
                "--tlscert": p.client.cert[0],
                "--tlskey": p.client.cert[1],
                "--host": p.client.base_url.replace("https", "tcp"),
                "--file": self.compose_files,
                "--project-name": self.name,
            }
            self._cmd = TopLevelCommand(p, cmd_options)
        return self._cmd

    @property
    def machine_name(self):
        return self.config["docker-machine"]

    @property
    def container_names(self):
        names = []
        for service in self.config["services"].values():
            names += service["containers"]
        return names

    @property
    def service_names(self):
        return list(self.config["services"].keys())

    @property
    def volume_names(self):
        names = []
        for service in self.config["services"].values():
            names += service["volumes"]
        return names

    @property
    def volumes(self):
        return self.project.volumes.volumes

    def get_project(self, compose_files):
        """ Parse the compose files """

        domains_env = {"PM_DOMAINS": json.dumps(self.config["domains"])}

        with extra_env(self.config["environment"], domains_env), fixed_relative_context():
            project = parse_compose_project(
                self.config_dir, self.machine_name, self.name, compose_files
            )
        return project

    def apply_traefik_rule(self, service_name, service_config, rule_name):
        ssl = rule_name == "https"
        if service_config[rule_name]:
            extra_labels = get_traefik_rules(
                service_name, service_config[rule_name], ssl=ssl
            )
            service = self.project.get_service(service_config[rule_name]["container"])
            if "labels" in service.options:
                service.options["labels"].update(extra_labels)
            else:
                service.options["labels"] = extra_labels

    def apply_traefik_rules(self):
        for service_name, service_config in self.config["services"].items():
            self.apply_traefik_rule(service_name, service_config, "http")
            self.apply_traefik_rule(service_name, service_config, "https")

    def ps(self, services):
        self.cmd.ps(
            {"--quiet": False, "--services": False, "--all": False, "SERVICE": services}
        )

    def env(self):
        check_call(["docker-machine", "env", "--", self.machine_name])

    def get_exec(self, service_name, command):
        service = self.project.get_service(service_name)
        container_name = service.get_container(1).name

        r = self.client.containers.get(container_name).exec_run(command, demux=True)
        stdout, _ = r.output
        return stdout

    def exec(self, service_name, command, privileged=False):
        options = {
            "--index": "1",
            "SERVICE": service_name,
            "COMMAND": command[0],
            "ARGS": list(command[1:]),
            "-T": False,
            "--detach": False,
            "--privileged": privileged,
            "--user": None,
            "--env": {},
            "--workdir": None,
        }
        # will call exit()
        self.cmd.exec_command(options)

    def ssh(self, args, get_output=False):
        cmd = ["docker-machine", "ssh", self.machine_name, *args]
        if get_output:
            return check_output(cmd)
        else:
            return check_call(cmd)

    def start(self, service_names):
        try:
            self.project.up(service_names=service_names, renew_anonymous_volumes=True)
        except BuildError as e:
            exit(f"Build failed for {e.service.name}")

    def stop(self, service_names, timeout=10):
        self.project.stop(service_names=service_names, timeout=timeout)

    def restart(self, service_names, timeout=10):
        self.stop(service_names, timeout)
        self.start(service_names)

    def build(self, service_names):
        try:
            self.project.build(service_names=service_names)
        except BuildError as e:
            print(e)
            exit(f"Build failed for {e.service.name}")

    def backup(self, volume_name):
        backup_path = "~/PM_Backup"
        volume_path = self.client.volumes.get(volume_name).attrs["Mountpoint"]

        backup_name = datetime.now().strftime(f"{volume_name}_%s.tgz")
        backup_fullpath = os.path.join(backup_path, backup_name)
        print(f"Backuping {volume_name}")
        self.ssh(["mkdir", "-p", backup_path])
        cmd = [
            "tar",
            "czf",
            backup_fullpath,
            volume_path,
        ]
        self.ssh(cmd, get_output=True)
        print(f"Backup available here: {backup_fullpath}")

    def logs(self, service_names, follow, tail):
        containers = self.project.containers(service_names=service_names, stopped=True)

        nocolor = False

        tail = tail if tail == "all" else int(tail)
        log_args = {"follow": follow, "tail": tail, "timestamps": False}
        log_printer_from_project(
            self.project,
            containers,
            nocolor,
            log_args,
            event_stream=self.project.events(service_names=service_names),
        ).run()

    def mount(self, volume_name, mountpoint):
        def do_mount(remote_path, local_path):
            success = check_call(
                [
                    "docker-machine",
                    "mount",
                    f"{self.machine_name}:{remote_path}",
                    local_path,
                ]
            )
            if not success:
                exit(1)
            print(
                f"Volume '{volume_name}' mounted on '{local_path}'.\n"
                "Exit this shell (ctrl+d) to unmount.\nStarting ...\r",
                end="",
            )
            check_call([os.environ["SHELL"]], cwd=local_path)
            check_call(["umount", local_path])

        volume = self.volumes[volume_name]
        remote_path = volume.inspect()["Mountpoint"]

        if mountpoint is not None:
            return do_mount(remote_path, mountpoint)

        prefix = f"{self.machine_name}-{volume_name}-"
        with tempfile.TemporaryDirectory(prefix=prefix) as mountpoint:
            return do_mount(remote_path, mountpoint)

    def get_container_names_for_services(self, service_names):
        container_names = []
        for service_name in service_names:
            container_names.extend(
                self.config["services"][service_name].get("containers", [])
            )
        return container_names
