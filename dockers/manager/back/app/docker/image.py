from app.utils import registerQuery, registerMutation, createType, registerSubscription
from . import docker_client, KeyValue, formatTime
from docker.errors import APIError, ImageNotFound
import docker
from typing import NamedTuple
import aiohttp
from dataclasses import dataclass
from uuid import uuid4
import asyncio
import re
from app.exception import PMException

DockerImage = createType("DockerImage")

# A tag name must be valid ASCII and may contain lowercase and uppercase letters, digits, underscores, periods and dashes.
# A tag name may not start with a period or a dash and may contain a maximum of 128 characters.
TAG_REG = re.compile(r"^[a-z0-9_][a-z0-9_\.\-]{0,127}$", re.IGNORECASE)


@dataclass
class HistoryEntry:
    operation: str
    argument: str
    comment: str
    tags: list[str]
    date: int
    size: int


@registerQuery("dockerImages")
def resolve_images(*_, onlyFinal):
    return docker_client.images.list(all=not onlyFinal)


@DockerImage.field("name")
def resolve_image_name(image, *_):
    if image.tags:
        return image.tags[0]
    if image.attrs["RepoDigests"]:
        return image.attrs["RepoDigests"][0].rpartition("@")[0]
    return image.id.partition(":")[2][:12]


@DockerImage.field("shortId")
def resolve_image_shortId(image, *_):
    return image.id.partition(":")[2][:12]


@DockerImage.field("tags")
def resolve_image_tags(image, _):
    return image.tags


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


OP_RE = re.compile(r"^([A-Z]+)\s+(.*)")


def parse_created_by(s):
    if "#(nop)" in s:
        return parse_created_by(s.split("#(nop)", 1)[1].strip())
    if s.startswith("RUN |") or s.startswith("/bin/sh -c"):
        return parse_created_by(s.split("sh -c", 1)[1].strip())
    if match := OP_RE.match(s):
        return match.group(1), match.group(2)
    return "RUN", s


@DockerImage.field("history")
def resolve_image_history(image, _):
    for entry in image.history()[::-1]:
        operation, argument = parse_created_by(entry["CreatedBy"])
        size = entry["Size"]
        comment = entry["Comment"]
        date = entry["Created"]
        tags = entry["Tags"] or []
        yield HistoryEntry(
            operation=operation,
            argument=argument,
            tags=tags,
            comment=comment,
            date=date,
            size=size,
        )


@registerMutation("dockerTagImage")
def resolve_tag_image(*_, id, tag, force):
    raise NotImplementedError()  # need fix
    try:
        docker_client.api.tag(id, **tag, force=force)
        return docker_client.images.get(id)
    except APIError as e:
        raise PMException(e.explanation)
    except Exception as e:
        raise PMException(str(e))


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
    tags = []
    for tag in await get_tags_for_image(repoName, imageName):
        name = f"{imageName}:{tag['name']}"
        if repoName != "library":
            name = f"{repoName}/{name}"
        tags.append(
            {
                "name": name,
                "size": tag["full_size"],
                "lastUpdated": formatTime(tag["last_updated"]),
            }
        )
    return tags


@registerMutation("dockerRemoveImage")
def resolve_remove_image(*_, id, force, pruneParents):
    try:
        docker_client.api.remove_image(id, force=force, noprune=not pruneParents)
    except APIError as e:
        raise PMException(e.explanation)
    except Exception as e:
        raise PMException(str(e))


@registerMutation("pruneDockerImages")
def resolve_prune_images(*_, onlyDangling):
    pruned = docker_client.images.prune(filters={"dangling": onlyDangling})
    deleted = []
    if deletedImages := pruned.get("ImagesDeleted", None):
        deleted = [next(iter(x.values())) for x in deletedImages]
    return {
        "deleted": deleted,
        "spaceReclaimed": pruned.get("SpaceReclaimed", None),
    }
