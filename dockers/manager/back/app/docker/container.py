from app.utils import registerQuery, registerMutation, createType
from . import docker_client, KeyValue, formatTime
from docker.errors import APIError, NotFound
from docker.types import Mount
from typing import NamedTuple

DockerContainer = createType("DockerContainer")
DockerContainerMount = createType("DockerContainerMount")
DockerContainerConnection = createType("DockerContainerConnection")


class ContainerMount(NamedTuple):
    type: str
    source: str = None
    target: str = None
    readonly: bool = False
    volume: str = None
    name: str = None


class ContainerPort(NamedTuple):
    protocol: str
    containerPort: int
    hostBindings: list


@registerQuery("dockerContainers")
def resolve_containers(*_, onlyRunning):
    return docker_client.containers.list(all=not onlyRunning)


def resolve_create_container(
    *,
    name=None,
    labels: list[KeyValue],
    imageId,
    command=None,
    user,
    workdir,
    environment: list[KeyValue],
    privileged,
    readonly,
    mounts: list[ContainerMount],
    ports: list[ContainerPort],
    onExit: str = None,
):
    return docker_client.containers.create(
        imageId,  #
        name=name,  #
        labels=dict(labels),  #
        command=command,  #
        user=user,  #
        working_dir=workdir,
        environment=dict(environment),  #
        privileged=privileged,
        read_only=readonly,
        mounts=[
            Mount(target, source, type.lower(), readonly)
            for type, target, source, _, readonly in (
                ContainerMount(**mount) for mount in mounts
            )
        ],  #
        ports={
            f"{containerPort}/{protocol}": [
                (*binding.values(),) for binding in hostBindings
            ]
            for protocol, containerPort, hostBindings in (
                ContainerPort(**port) for port in ports
            )
        },
        **{}
        if onExit is None
        else {"auto_remove": True}
        if onExit == "REMOVE"
        else {
            "restart_policy": {
                "Name": {
                    "RESTART_ON_FAILURE": "on-failure",
                    "RESTART_UNLESS_STOPPED": "unless-stopped",
                    "RESTART_ALWAYS": "always",
                }[onExit]
            }
        },
    )


@registerMutation("createDockerContainer")
def resolve_form_create_container(*_, input):
    return resolve_create_container(**input)


@registerQuery("dockerContainerByName")
@registerQuery("dockerContainerById")
def resolve_container_by_name(*_, name=None, id=None):
    try:
        return docker_client.containers.get(name or id)
    except:
        return None


@DockerContainer.field("labels")
def resolve_container_labels(container, _):
    return [KeyValue(*label) for label in container.labels.items()]


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


@DockerContainer.field("privileged")
def resolve_container_privileged(container, _):
    return container.attrs["HostConfig"]["Privileged"]


@DockerContainer.field("ps")
def resolve_container_ps(container, _):
    if not container.attrs["State"]["Running"]:
        return None
    titles = [
        "user",
        "pid",
        "cpu",
        "mem",
        "vsz",
        "rss",
        "tty",
        "stat",
        "start",
        "time",
        "command",
    ]
    top = container.top(ps_args="-aux")
    processes = []
    for ps in top["Processes"]:
        process = {}
        for title, value in zip(titles, ps):
            process[title] = value
        processes.append(process)
    return processes


@DockerContainerConnection.field("ipAddress")
def resolve_connection_ip_address(connection, *_):
    return connection.get("IPAddress", None) or None


@DockerContainer.field("mounts")
def resolve_container_mounts(container, _):
    return [
        ContainerMount(
            type=mount["Type"],
            source=mount.get("Source"),
            target=mount.get("Destination"),
            readonly=not mount["RW"],
            volume=mount.get("Name"),
            name=mount.get("Name")
        )
        for mount in container.attrs["Mounts"]
    ]


@DockerContainerMount.field("volume")
def resolve_container_mount_volume(mount: ContainerMount, _):
    if mount.type == "VOLUME":
        return docker_client.volumes.get(mount.volume)
    return None


@DockerContainer.field("connections")
def resolve_container_connections(container, _):
    return [
        {
            "aliases": endpoint["Aliases"] or [],
            "ipAddress": endpoint["IPAddress"] or None,
            "network": docker_client.networks.get(name),
        }
        for name, endpoint in container.attrs["NetworkSettings"]["Networks"].items()
    ]


@DockerContainer.field("ports")
def resolve_container_ports(container, _):
    return [
        ContainerPort(
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


@registerMutation("startDockerContainer")
def resolve_start_container(*_, id):
    try:
        docker_client.api.start(id)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("restartDockerContainer")
def resolve_restart_container(*_, id):
    try:
        docker_client.api.restart(id)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("pauseDockerContainer")
def resolve_pause_container(*_, id):
    try:
        docker_client.api.pause(id)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("unpauseDockerContainer")
def resolve_unpause_container(*_, id):
    try:
        docker_client.api.unpause(id)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("stopDockerContainer")
def resolve_stop_container(*_, id):
    try:
        docker_client.api.stop(id)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("killDockerContainer")
def resolve_kill_container(*_, id):
    try:
        docker_client.api.kill(id)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("renameDockerContainer")
def resolve_rename_container(*_, id, name):
    try:
        docker_client.api.rename(id, name=name)
        return docker_client.containers.get(id)
    except (APIError, NotFound):
        return None


@registerMutation("deleteDockerContainer")
def resolve_remove_container(*_, id, force, pruneVolumes):
    try:
        docker_client.api.remove_container(id, v=pruneVolumes, force=force)
    except APIError:
        return False
    return True


@registerMutation("pruneDockerContainers")
def resolve_prune_containers(*_):
    pruned = docker_client.containers.prune()
    return {
        "deleted": pruned["ContainersDeleted"] or [],
        "spaceReclaimed": 0,
    }
