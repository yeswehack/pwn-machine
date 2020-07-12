import os
import textwrap
import docker
import json
from tqdm import tqdm
from .utils import parse_compose_project, get_machine_options, print_stream
from compose.cli.main import BuildAction


def get_services_for_id(client, id):
    filters = {"label": [f"pm.pipeline.id={id}", "pm.pipeline.service.name"]}
    running_services = client.containers.list(filters=filters)
    return {s.labels.get("pm.pipeline.service.name"): s for s in running_services}


class DockerClient(docker.DockerClient):
    def __init__(self, api):
        self.api = api


class Service:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    @classmethod
    def from_config(cls, name, config):
        if config is None:
            config = {}
        arguments = config.get("arguments", [])
        return cls(name, arguments)

    def __repr__(self):
        args = " ".join(f"<{a}>" for a in self.arguments)
        return f"""{self.name} {args}"""


class Pipeline:
    def __init__(self, compose_content, project, name, arguments, services):
        self.name = name
        self.id = os.urandom(4).hex()
        self.project = project
        self.services = services
        self.client = DockerClient(self.project.client)
        self.compose_content = compose_content
        self.arguments = arguments

    @classmethod
    def from_config(cls, compose_content, project, name, config):
        if config is None:
            config = {}

        arguments = config.get("arguments", [])
        services = {
            name: Service.from_config(name, s)
            for name, s in config.get("services", {}).items()
        }
        return cls(compose_content, project, name, arguments, services)

    def start(self, args):
        self.check_required_args(args)
        self.assert_runner()
        self.build_services(do_build=BuildAction.none)

        container_name = f"pm-pipeline-{self.name}-{self.id}"
        env = {
            "compose": self.compose_content,
            "pipeline": json.dumps(self.serialize(args)),
        }
        volumes = {
            "/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"}
        }
        labels = {"pm.pipeline.name": self.name, "pm.pipeline.id": self.id}
        self.client.containers.run(
            "pm-pipeline-runner",
            name=container_name,
            labels=labels,
            auto_remove=True,
            detach=True,
            volumes=volumes,
            environment=env,
        )
        print(f'Pipeline "{self.name}" started in container {container_name}')

    def build_runner(self):
        print("Building pm-pipeline-runner")
        stream = self.project.client.build(
            path="/home/bitk/bi.tk/pipeline",
            tag="pm-pipeline-runner",
            quiet=False,
            rm=True,
        )
        print_stream(stream)

    def assert_runner(self):
        try:
            self.client.images.get("pm-pipeline-runner")
        except docker.errors.ImageNotFound:
            self.build_runner()

    def build(self, do_build=BuildAction.force):
        self.build_runner()
        self.build_services()

    def build_services(self, do_build=BuildAction.force):
        to_build = [s for s in self.project.services if s.name in self.services]
        for service in to_build:
            print(f"Building '{service.name}'")
            service.ensure_image_exists(do_build=do_build)

    def check_required_args(self, supplied_args):
        for service in self.services.values():
            for arg in service.arguments:
                if arg not in supplied_args:
                    exit(f"Argument '{arg}' is required for '{service.name}'")

    def serialize(self, arguments):
        services = list(self.services.keys())
        return {
            "name": self.name,
            "id": self.id,
            "services": services,
            "environ": arguments,
        }

    def __repr__(self):
        services = " | ".join(f"{s}" for s in self.services.values())
        return f"""{self.name}: {services}"""


class Pipelines:
    def __init__(self, compose_content, project, pipelines):
        self.project = project
        self.client = DockerClient(self.project.client)
        self.compose_content = compose_content
        self.pipelines = pipelines

    @classmethod
    def from_config(cls, machine_name, config):
        if config is None:
            config = {}

        compose_file = config.get("compose")
        try:
            compose_content = open(compose_file, "r", encoding="utf8").read()
        except:
            exit("compose file in pipeline need to be readable")

        project = parse_compose_project(machine_name, "pm_pipeline", [compose_file])
        pipelines = {
            name: Pipeline.from_config(compose_content, project, name, p)
            for name, p in config.get("pipelines", {}).items()
        }
        return Pipelines(compose_content, project, pipelines)

    def ps(self):
        filters = {"label": "pm.pipeline.name"}
        containers = self.client.containers.list(filters=filters)
        for container in containers:
            name = container.labels["pm.pipeline.name"]
            id = container.labels["pm.pipeline.id"]
            print(f"{name} [{id}]:")
            services = get_services_for_id(self.client, id)
            for service in self.pipelines[name].services:
                running = "" if service not in services else " [Running]"
                print(f"  - {service}{running}")

    def ls(self):
        for pipeline in self.pipelines.values():
            print(pipeline)

    def build(self, pipeline_names):
        for name, pipeline in self.pipelines.items():
            if pipeline_names and name not in pipeline_names:
                continue
            pipeline.build()

    def start(self, pipeline_name, args):
        self.pipelines[pipeline_name].start(args)
