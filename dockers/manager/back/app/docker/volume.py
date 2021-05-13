from ..utils import registerQuery, createType
from . import docker_client, KeyValue
from datetime import datetime

DockerVolume = createType("DockerVolume")


@registerQuery("dockerVolumes")
async def resolve_volumes(*_):
    return docker_client.volumes.list()


@DockerVolume.field("labels")
async def resolve_volume_labels(volume, _):
    return [KeyValue(label) for label in (volume.attrs["Labels"] or {}).items()]


@DockerVolume.field("created")
async def resolve_volume_created(volume, _):
    return str(datetime.fromisoformat(volume.attrs["CreatedAt"].partition(".")[0]))
