from ..utils import registerQuery, createType
from . import docker_client, KeyValue, RepoTag
from datetime import datetime

DockerImage = createType("DockerImage")


@registerQuery("dockerImages")
async def resolve_images(*_, onlyFinal=True, filters=None):
    return docker_client.images.list(all=not onlyFinal, filters=filters)


@DockerImage.field("tags")
async def resolve_image_tags(image, _):
    return [RepoTag(*ref.split(":", 1)) for ref in image.tags]


@DockerImage.field("labels")
async def resolve_image_labels(image, _):
    return [KeyValue(k, v) for k, v in image.labels.items()]


@DockerImage.field("parent")
async def resolve_image_parent(image, _):
    return image.attrs["Config"]["Image"]


@DockerImage.field("created")
async def resolve_image_created(image, _):
    return str(datetime.fromisoformat(image.attrs["Created"].partition(".")[0]))


@DockerImage.field("size")
async def resolve_image_size(image, _):
    return image.attrs["Size"]


@DockerImage.field("entrypoint")
async def resolve_image_entrypoint(image, _):
    return image.attrs["Config"].get("Entrypoint")


@DockerImage.field("command")
async def resolve_image_command(image, _):
    return image.attrs["Config"].get("Cmd")


@DockerImage.field("environment")
async def resolve_image_environment(image, _):
    return [KeyValue(*var.split("=", 1)) for var in image.attrs["Config"]["Env"]]
