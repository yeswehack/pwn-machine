# pylint: disable=all
import graphene
from .client import docker


class RootFS(graphene.ObjectType):
    type = graphene.String(resolver=lambda x, y: x["Type"])
    layer = graphene.List(graphene.String, resolver=lambda x, y: x["Layers"])


class Image(graphene.ObjectType):
    id = graphene.ID()
    shortId = graphene.String()
    repo_tags = graphene.List(graphene.String)
    container = graphene.String()
    rootfs = graphene.Field(RootFS, name="rootFS")
    repository = graphene.String()
    created = graphene.String()
    size = graphene.Float()
    tag = graphene.String()
    used_by = graphene.List("schemas.docker.container.Container")

    def resolve_id(image, info):
        return image.attrs["Id"]

    def resolve_shortId(image, info):
        return image.attrs["Id"].split(":")[1][:12]

    def resolve_repository(image, info):
        repoTags = image.attrs["RepoTags"]
        if not repoTags:
            return "<none>"
        return repoTags[0].split(":")[0]

    def resolve_tag(image, info):
        repoTags = image.attrs["RepoTags"]
        if not repoTags:
            return "<none>"
        return repoTags[0].split(":")[1]

    def resolve_created(image, info):
        return image.attrs["Created"]

    def resolve_size(image, info):
        return image.attrs["Size"]

    def resolve_used_by(image, info):
        return docker.containers.list(filters={"ancestor": image.attrs["Id"]})
