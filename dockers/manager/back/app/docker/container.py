from ..utils import registerQuery, createType
from . import docker_client, KeyValue, formatTime
from dataclasses import dataclass

DockerContainer = createType("DockerContainer")
DockerContainerMount = createType("DockerContainerMount")


@registerQuery("dockerContainers")
async def resolve_containers(*_, onlyRunning=True):
    return docker_client.containers.list(all=not onlyRunning)


@DockerContainer.field("labels")
async def resolve_container_labels(container, _):
    return [KeyValue(*label) for label in container.labels.items()]


@DockerContainer.field("created")
async def resolve_container_created(container, _):
    return formatTime(container.attrs["Created"])


@DockerContainer.field("command")
async def resolve_container_command(container, _):
    return [container.attrs["Path"]] + container.attrs["Args"]


@DockerContainer.field("environment")
async def resolve_container_environment(container, _):
    return [
        KeyValue(*var.partition("=")[::2]) for var in container.attrs["Config"]["Env"]
    ]


@DockerContainer.field("mounts")
async def resolve_container_mounts(container, _):
    return container.attrs["Mounts"]


@DockerContainer.field("networks")
async def resolve_container_networks(container, _):
    return map(
        docker_client.networks.get,
        container.attrs["NetworkSettings"]["Networks"].keys(),
    )


@dataclass
class ExposedPort:
    protocol: str
    containerPort: int
    hostBindings: list


@DockerContainer.field("ports")
async def resolve_container_ports(container, _):
    return [
        ExposedPort(
            *port.upper().rpartition("/")[::-2],
            [
                {
                    "ip": bind["HostIp"],
                    "port": bind["HostPort"],
                }
                for bind in binds or []
            ],
        )
        for port, binds in container.ports.items()
    ]


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
