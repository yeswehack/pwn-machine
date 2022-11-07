from app.utils import registerQuery, registerMutation, createType
from . import docker_client, KeyValue, formatTime, kv_to_dict
from docker.errors import APIError
from app.exception import PMException

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


@DockerVolume.field("usedBy")
def resolve_volume_used_by(volume, _, onlyRunning):
    return docker_client.containers.list(
        all=not onlyRunning, filters={"volume": volume.attrs["Name"]}
    )


@registerMutation("createDockerVolume")
def resolve_create_volume(*_, input):
    try:
        labels = kv_to_dict(input["labels"])
        docker_client.volumes.create(input.get("name"), labels=labels)
    except APIError as e:
        raise PMException(e.explanation)
    except Exception as e:
        raise PMException(str(e))


@registerMutation("deleteDockerVolume")
def resolve_remove_volume(*_, name, force):
    try:
        docker_client.api.remove_volume(name, force=force)
    except APIError as e:
        raise PMException(e.explanation)
    except Exception as e:
        raise PMException(str(e))


@registerMutation("pruneDockerVolumes")
def resolve_prune_volumes(*_):
    pruned = docker_client.volumes.prune()
    return {
        "deleted": pruned["VolumesDeleted"],
        "spaceReclaimed": pruned["SpaceReclaimed"],
    }
