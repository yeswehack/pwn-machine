from app.utils import registerQuery, registerMutation, createType
from . import docker_client, KeyValue, formatTime
from docker.errors import APIError, NotFound
from dataclasses import dataclass

DockerContainer = createType("DockerContainer")
DockerContainerMount = createType("DockerContainerMount")


@registerQuery("dockerContainers")
def resolve_containers(*_, onlyRunning=True):
    return docker_client.containers.list(all=not onlyRunning)


@DockerContainer.field("labels")
def resolve_container_labels(container, _):
    return [KeyValue(*label) for label in container.labels.items()]


@DockerContainer.field("created")
def resolve_container_created(container, _):
    return formatTime(container.attrs["Created"])


@DockerContainer.field("command")
def resolve_container_command(container, _):
    return [container.attrs["Path"]] + container.attrs["Args"]


@DockerContainer.field("privileged")
def resolve_container_privileged(container, _):
    return container.attrs["HostConfig"]["Privileged"]


@DockerContainer.field("environment")
def resolve_container_environment(container, _):
    return [
        KeyValue(*var.partition("=")[::2]) for var in container.attrs["Config"]["Env"]
    ]


@DockerContainer.field("mounts")
def resolve_container_mounts(container, _):
    return [
        {
            "type": mount["Type"].upper(),
            "volume": mount.get("Name"),
            "source": mount.get("Source"),
            "target": mount["Destination"],
            "readonly": not mount["RW"],
        }
        for mount in container.attrs["Mounts"]
    ]


@DockerContainerMount.field("volume")
def resolve_container_mount_volume(mount, _):
    return docker_client.volumes.get(name) if (name := mount["volume"]) else None


@DockerContainer.field("connections")
def resolve_container_connections(container, _):
    return [
        {
            "aliases": endpoint["Aliases"] or [],
            "ipAddress": endpoint["IPAddress"] or None,
            "network": docker_client.networks.get(name),
        }
        for name, endpoint in container.attrs["NetworkSettings"]["Networks"]
    ]


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


@registerMutation("dockerStartContainer")
def resolve_start_container(*_, id):
    try:
        docker_client.api.start(id)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("dockerRestartContainer")
def resolve_restart_container(*_, id):
    try:
        docker_client.api.restart(id)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("dockerPauseContainer")
def resolve_pause_container(*_, id):
    try:
        docker_client.api.pause(id)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("dockerUnpauseContainer")
def resolve_unpause_container(*_, id):
    try:
        docker_client.api.unpause(id)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("dockerStopContainer")
def resolve_stop_container(*_, id, timeout):
    try:
        docker_client.api.stop(id, timeout)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("dockerKillContainer")
def resolve_kill_container(*_, id, signal):
    try:
        docker_client.api.kill(id, signal)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("dockerRenameContainer")
def resolve_rename_container(*_, id, name):
    try:
        docker_client.api.rename(id, name)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("dockerRemoveContainer")
def resolve_remove_container(*_, id, force=False, pruneVolumes=False):
    try:
        docker_client.api.remove_container(id, pruneVolumes, force=force)
    except APIError:
        return False
    return True


@registerMutation("dockerPruneContainers")
def resolve_prune_containers(*_):
    try:
        return docker_client.api.prune_containers()["SpaceReclaimed"]
    except APIError:
        return None
