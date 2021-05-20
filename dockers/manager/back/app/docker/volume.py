from app.utils import registerQuery, registerMutation, createType
from . import docker_client, KeyValue, formatTime
from docker.errors import APIError, NotFound

DockerVolume = createType("DockerVolume")


@registerQuery("dockerVolumes")
async def resolve_volumes(*_):
    return docker_client.volumes.list()


@DockerVolume.field("labels")
async def resolve_volume_labels(volume, _):
    return [KeyValue(*label) for label in (volume.attrs["Labels"] or {}).items()]


@DockerVolume.field("created")
async def resolve_volume_created(volume, _):
    return formatTime(volume.attrs["CreatedAt"])


@DockerVolume.field("mountpoint")
async def resolve_volume_mountpoint(volume, _):
    return volume.attrs["Mountpoint"]


@DockerVolume.field("usingContainers")
async def resolve_volume_using_containers(volume, _, onlyRunning=True):
    return docker_client.containers.list(
        all=not onlyRunning, filters={"volume": volume.attrs["Name"]}
    )


@registerMutation("dockerCreateVolume")
async def resolve_create_volume(*_, name=None, labels: list[KeyValue]):
    try:
        return docker_client.volumes.create(name, labels=dict(labels))
    except APIError:
        return None


@registerMutation("dockerRemoveVolume")
async def resolve_remove_volume(*_, name, force=False):
    try:
        docker_client.volumes.get(name).remove(force)
    except (NotFound, APIError):
        return False
    return True


@registerMutation("dockerPruneVolumes")
async def resolve_prune_volumes(*_):
    try:
        return docker_client.volumes.prune()["SpaceReclaimed"]
    except APIError:
        return None
