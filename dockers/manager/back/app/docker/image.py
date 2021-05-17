from ..utils import registerQuery, createType
from . import docker_client, KeyValue, RepoTag
import aiohttp
import re
from datetime import datetime

DockerImage = createType("DockerImage")

# A tag name must be valid ASCII and may contain lowercase and uppercase letters, digits, underscores, periods and dashes.
# A tag name may not start with a period or a dash and may contain a maximum of 128 characters.
TAG_REG = re.compile(r"^[a-z0-9_][a-z0-9_\.\-]{0,127}$", re.IGNORECASE)


def formatTime(t):
    return datetime.fromisoformat(t.partition(".")[0])


@registerQuery("dockerImages")
async def resolve_images(*_, onlyFinal=True, filters=None):
    return docker_client.images.list(all=not onlyFinal, filters=filters)


@DockerImage.field("tags")
async def resolve_image_tags(image, _):
    return [RepoTag(*ref.split(":", 1)) for ref in image.tags]


@DockerImage.field("name")
def resolve_image_name(image, *_):
    name = "<no name>"
    if len(image.attrs["RepoTags"]):
        name = image.attrs["RepoTags"][0]
    elif len(image.attrs["RepoDigests"]):
        name = image.attrs["RepoDigests"][0].rpartition("@")[0]

    # if name.endswith(":latest"):
    #    return name[:-7]
    return name


@DockerImage.field("labels")
async def resolve_image_labels(image, _):
    return [KeyValue(k, v) for k, v in image.labels.items()]


@DockerImage.field("parent")
async def resolve_image_parent(image, _):
    return image.attrs["Config"]["Image"]


@DockerImage.field("created")
async def resolve_image_created(image, _):
    return str(formatTime(image.attrs["Created"]))


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


@registerQuery("dockerSearchImage")
def resolve_search_image(*_, search):
    result = []
    for image in docker_client.images.search(search):
        entry = {
            "name": image["name"],
            "description": image["description"],
            "isOfficial": image["is_official"],
            "isAutomated": image["is_automated"],
            "starCount": image["star_count"],
        }
        result.append(entry)
    return result


async def get_tags_for_image(repoName, imageName):
    url = f"https://registry.hub.docker.com/v2/repositories/{repoName}/{imageName}/tags"
    params = {"page_size": 50}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            if "results" not in data:
                return []
            return data["results"]


@registerQuery("dockerSearchImageTag")
async def resolve_search_tag(*_, repoName, imageName):
    if not TAG_REG.match(repoName):
        raise ValueError(f"Invalid repoName, must match {TAG_REG.pattern}")
    if not TAG_REG.match(imageName):
        raise ValueError(f"Invalid imageName, must match {TAG_REG.pattern}")

    result = []
    for tag in await get_tags_for_image(repoName, imageName):
        entry = {
            "name": f"{repoName}/{imageName}:{tag['name']}",
            "lastUpdated": str(formatTime(tag["last_updated"])) if tag["last_updated"] else "never",
            "size": tag["full_size"],
        }
        result.append(entry)
    return result
