from ..utils import registerQuery, createType
from . import docker_client, KeyValue
from datetime import datetime

DockerContainer = createType("DockerContainer")


@registerQuery("dockerContainers")
async def resolve_containers(*_, onlyRunning=True):
    return docker_client.containers.list(all=not onlyRunning)


@DockerContainer.field("labels")
async def resolve_container_labels(container, _):
    return [KeyValue(k, v) for k, v in container.labels.items()]


@DockerContainer.field("created")
async def resolve_container_created(container, _):
    return str(datetime.fromisoformat(container.attrs["Created"].partition(".")[0]))


@DockerContainer.field("command")
async def resolve_container_command(container, _):
    return [container.attrs["Path"]] + container.attrs["Args"]


@DockerContainer.field("environment")
async def resolve_container_environment(container, _):
    return [KeyValue(*var.split("=", 1)) for var in container.attrs["Config"]["Env"]]


@DockerContainer.field("status")
async def resolve_container_status(container, _):
    return container.status.upper()
