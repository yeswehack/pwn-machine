from app.utils import registerQuery, createType
from . import docker_client, KeyValue, formatTime
from dataclasses import dataclass

DockerContainer = createType("DockerContainer")
DockerContainerMount = createType("DockerContainerMount")
DockerContainerConnection = createType("DockerContainerConnection")


@registerQuery("dockerContainers")
def resolve_containers(*_, onlyRunning=True):
    return docker_client.containers.list(all=not onlyRunning)


@DockerContainer.field("labels")
def resolve_container_labels(container, _):
    return [KeyValue(*label) for label in container.labels.items()]

@DockerContainer.field("privileged")
def resolve_container_privileged(container, _):
    return container.attrs["HostConfig"]["Privileged"]



@DockerContainer.field("created")
def resolve_container_created(container, _):
    return formatTime(container.attrs["Created"])


@DockerContainer.field("command")
def resolve_container_command(container, _):
    return [container.attrs["Path"]] + container.attrs["Args"]


@DockerContainer.field("environment")
def resolve_container_environment(container, _):
    return [
        KeyValue(*var.partition("=")[::2]) for var in container.attrs["Config"]["Env"]
    ]


@DockerContainer.field("mounts")
def resolve_container_mounts(container, _):
    return container.attrs["Mounts"]


@DockerContainer.field("connections")
def resolve_container_connections(container, _):
    return container.attrs["NetworkSettings"]["Networks"].values()


@DockerContainerConnection.field("ipAddress")
def resolve_connection_ip_address(connection, *_):
    print(connection)
    return connection["IPAddress"] or None


@DockerContainerConnection.field("aliases")
def resolve_connection_ip_aliases(connection, *_):
    return connection["Aliases"] or []


@DockerContainerConnection.field("network")
def resolve_connection_ip_network(connection, *_):
    return docker_client.networks.get(connection["NetworkID"])


@dataclass
class ExposedPort:
    protocol: str
    containerPort: int
    hostBindings: list


@DockerContainer.field("ports")
def resolve_container_ports(container, _):
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
def resolve_container_status(container, _):
    return container.status.upper()


@DockerContainerMount.field("type")
def resolve_container_mount_type(mount, _):
    return mount["Type"].upper()


@DockerContainerMount.field("volume")
def resolve_container_mount_volume(mount, _):
    return docker_client.volumes.get(name) if (name := mount.get("Name")) else None


@DockerContainerMount.field("source")
def resolve_container_mount_source(mount, _):
    return mount.get("Source")


@DockerContainerMount.field("target")
def resolve_container_mount_target(mount, _):
    return mount["Destination"]


@DockerContainerMount.field("readonly")
def resolve_container_mount_readonly(mount, _):
    return not mount["RW"]
