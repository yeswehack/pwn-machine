from ..utils import registerQuery, createType
from . import docker_client, KeyValue
from datetime import datetime

DockerContainer = createType("DockerContainer")
DockerContainerMount = createType("DockerContainerMount")


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


@DockerContainer.field("mounts")
async def resolve_container_mounts(container, _):
    return container.attrs["Mounts"]


@DockerContainer.field("status")
async def resolve_container_status(container, _):
    return container.status.upper()


@DockerContainerMount.field("type")
async def resolve_container_mount_type(mount, _):
    return mount["Type"].upper()


@DockerContainerMount.field("volume")
async def resolve_container_mount_volume(mount, _):
    return docker_client.volumes.get(name) if (name := mount.get("Name")) else None


@DockerContainerMount.field("source")
async def resolve_container_mount_source(mount, _):
    return mount.get("Source")


@DockerContainerMount.field("target")
async def resolve_container_mount_target(mount, _):
    return mount["Destination"]


@DockerContainerMount.field("readonly")
async def resolve_container_mount_readonly(mount, _):
    return not mount["RW"]
