from app.utils import registerQuery, registerMutation, createType
from . import docker_client, KeyValue, formatTime
from docker.errors import APIError

DockerVolume = createType("DockerVolume")


@registerQuery("dockerVolumes")
def resolve_volumes(*_):
    return docker_client.volumes.list()


@DockerVolume.field("labels")
def resolve_volume_labels(volume, _):
    return [KeyValue(*label) for label in (volume.attrs["Labels"] or {}).items()]


@DockerVolume.field("created")
def resolve_volume_created(volume, _):
    return formatTime(volume.attrs["CreatedAt"])


@DockerVolume.field("mountpoint")
def resolve_volume_mountpoint(volume, _):
    return volume.attrs["Mountpoint"]


@DockerVolume.field("usingContainers")
def resolve_volume_using_containers(volume, _, onlyRunning=True):
    return docker_client.containers.list(
        all=not onlyRunning, filters={"volume": volume.attrs["Name"]}
    )


@registerMutation("dockerCreateVolume")
def resolve_create_volume(*_, input):
    try:
        return docker_client.volumes.create(
            input.get("name"), labels=dict(input["labels"])
        )
    except APIError:
        return None


@registerMutation("dockerRemoveVolume")
def resolve_remove_volume(*_, name, force=False):
    try:
        docker_client.api.remove_volume(name, force)
    except APIError:
        return False
    return True


@registerMutation("dockerPruneVolumes")
def resolve_prune_volumes(*_):
    try:
        return docker_client.api.prune_volumes()["SpaceReclaimed"]
    except APIError:
        return None
