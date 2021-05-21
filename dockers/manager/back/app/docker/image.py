from app.utils import registerQuery, registerMutation, createType
from . import docker_client, KeyValue, formatTime
from docker.errors import APIError, ImageNotFound
from dataclasses import dataclass
import aiohttp
import re

DockerImage = createType("DockerImage")

# A tag name must be valid ASCII and may contain lowercase and uppercase letters, digits, underscores, periods and dashes.
# A tag name may not start with a period or a dash and may contain a maximum of 128 characters.
TAG_REG = re.compile(r"^[a-z0-9_][a-z0-9_\.\-]{0,127}$", re.IGNORECASE)


@registerQuery("dockerImages")
async def resolve_images(*_, onlyFinal=True):
    return docker_client.images.list(all=not onlyFinal)


@dataclass
class RepoTag:
    repository: str
    tag: str = "latest"


@DockerImage.field("tags")
async def resolve_image_tags(image, _):
    return [RepoTag(*ref.partition(":")[::2]) for ref in image.tags]


@DockerImage.field("name")
async def resolve_image_name(image, *_):
    if image.attrs["RepoTags"]:
        return image.attrs["RepoTags"][0]
    if image.attrs["RepoDigests"]:
        return image.attrs["RepoDigests"][0].rpartition("@")[0]
    _, _, id = image.attrs["Id"].partition(":")
    return id[:12]


@DockerImage.field("labels")
async def resolve_image_labels(image, _):
    return [KeyValue(*label) for label in image.labels.items()]


@DockerImage.field("parent")
async def resolve_image_parent(image, _):
    return image.attrs["Config"]["Image"]


@DockerImage.field("created")
async def resolve_image_created(image, _):
    return formatTime(image.attrs["Created"])


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
    return [KeyValue(*var.partition("=")[::2]) for var in image.attrs["Config"]["Env"]]


@DockerImage.field("usingContainers")
async def resolve_image_using_containers(image, _, onlyRunning=True):
    return docker_client.containers.list(
        all=not onlyRunning, filters={"ancestor": image.id}
    )


@registerQuery("dockerSearchImage")
async def resolve_search_image(*_, search):
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


@registerMutation("dockerPullImage")
async def resolve_pull_image(*_, repository, tag):
    try:
        return docker_client.images.pull(repository, tag)
    except APIError:
        return None


@registerMutation("dockerTagImage")
async def resolve_tag_image(*_, id, repository, tag, force=False):
    try:
        docker_client.api.tag(id, repository, tag, force)
        return docker_client.images.get(id)
    except (APIError, ImageNotFound):
        return None


@registerMutation("dockerRemoveImage")
async def resolve_remove_image(*_, id, force=False, pruneParents=True):
    try:
        docker_client.api.remove_image(id, force, noprune=not pruneParents)
    except APIError:
        return False
    return True


@registerMutation("dockerPruneImages")
async def resolve_prune_images(*_, onlyDangling=False):
    try:
        filters = {"dangling": onlyDangling}
        return docker_client.api.prune_images(filters)["SpaceReclaimed"]
    except APIError:
        return None
