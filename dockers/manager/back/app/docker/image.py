from app.utils import registerQuery, registerMutation, createType
from . import docker_client, KeyValue, formatTime
from docker.errors import APIError, ImageNotFound
from typing import NamedTuple
import aiohttp
import re

DockerImage = createType("DockerImage")

# A tag name must be valid ASCII and may contain lowercase and uppercase letters, digits, underscores, periods and dashes.
# A tag name may not start with a period or a dash and may contain a maximum of 128 characters.
TAG_REG = re.compile(r"^[a-z0-9_][a-z0-9_\.\-]{0,127}$", re.IGNORECASE)


class RepoTag(NamedTuple):
    repository: str
    tag: str = "latest"


@registerQuery("dockerImages")
def resolve_images(*_, onlyFinal):
    return docker_client.images.list(all=not onlyFinal)


@registerMutation("dockerPullImage")
def resolve_pull_image(*_, tag: RepoTag):
    try:
        return docker_client.images.pull(**tag)
    except APIError:
        return None


@DockerImage.field("name")
def resolve_image_name(image, *_):
    if image.attrs["RepoTags"]:
        return image.attrs["RepoTags"][0]
    if image.attrs["RepoDigests"]:
        return image.attrs["RepoDigests"][0].rpartition("@")[0]
    return image.attrs["Id"].partition(":")[2][:12]


@DockerImage.field("tags")
def resolve_image_tags(image, _):
    return [RepoTag(*ref.partition(":")[::2]) for ref in image.tags]


@DockerImage.field("labels")
def resolve_image_labels(image, _):
    return [KeyValue(*label) for label in image.labels.items()]


@DockerImage.field("parent")
def resolve_image_parent(image, _):
    return image.attrs["Config"]["Image"]


@DockerImage.field("created")
def resolve_image_created(image, _):
    return formatTime(image.attrs["Created"])


@DockerImage.field("size")
def resolve_image_size(image, _):
    return image.attrs["Size"]


@DockerImage.field("entrypoint")
def resolve_image_entrypoint(image, _):
    return image.attrs["Config"].get("Entrypoint")


@DockerImage.field("command")
def resolve_image_command(image, _):
    return image.attrs["Config"].get("Cmd")


@DockerImage.field("environment")
def resolve_image_environment(image, _):
    return [KeyValue(*var.partition("=")[::2]) for var in image.attrs["Config"]["Env"]]


@DockerImage.field("usedBy")
def resolve_image_used_by(image, _, onlyRunning):
    return docker_client.containers.list(
        all=not onlyRunning, filters={"ancestor": image.id}
    )


@registerMutation("dockerTagImage")
def resolve_tag_image(*_, id, tag: RepoTag, force):
    try:
        docker_client.api.tag(id, **tag, force=force)
        return docker_client.images.get(id)
    except (APIError, ImageNotFound):
        return None


@registerQuery("dockerSearchImage")
def resolve_search_image(*_, search):
    return [
        {
            "name": image["name"],
            "description": image["description"],
            "isOfficial": image["is_official"],
            "isAutomated": image["is_automated"],
            "starCount": image["star_count"],
        }
        for image in docker_client.images.search(search)
    ]


async def get_tags_for_image(repoName, imageName):
    url = f"https://registry.hub.docker.com/v2/repositories/{repoName}/{imageName}/tags"
    params = {"page_size": 50}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return (await response.json()).get("results", [])


@registerQuery("dockerSearchImageTag")
async def resolve_search_tag(*_, repoName, imageName):
    if not TAG_REG.match(repoName):
        raise ValueError(f"Invalid repoName, must match {TAG_REG.pattern}")
    if not TAG_REG.match(imageName):
        raise ValueError(f"Invalid imageName, must match {TAG_REG.pattern}")

    return [
        {
            "name": f"{repoName}/{imageName}:{tag['name']}",
            "size": tag["full_size"],
            "lastUpdated": formatTime(tag["last_updated"]),
        }
        for tag in await get_tags_for_image(repoName, imageName)
    ]


@registerMutation("dockerRemoveImage")
def resolve_remove_image(*_, id, force, pruneParents):
    try:
        docker_client.api.remove_image(id, force=force, noprune=not pruneParents)
    except APIError:
        return False
    return True


@registerMutation("dockerPruneImages")
def resolve_prune_images(*_, onlyDangling):
    try:
        filters = {"dangling": onlyDangling}
        return docker_client.api.prune_images(filters)["SpaceReclaimed"]
    except APIError:
        return None
