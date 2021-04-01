import graphene
from .client import docker


class Volume(graphene.ObjectType):
    name = graphene.ID()
    created_at = graphene.String()
    driver = graphene.String()
    mountpoint = graphene.String()
    used_by = graphene.List("schemas.docker.container.Container")
    labels = graphene.List("schemas.docker.keyValue.KeyValue")

    def resolve_created_at(volume, info):
        return volume.attrs["CreatedAt"]

    def resolve_labels(volume, info):
        return volume.attrs["Labels"].items()

    def resolve_driver(volume, info):
        return volume.attrs["Driver"]

    def resolve_mountpoint(volume, info):
        return volume.attrs["Mountpoint"]

    def resolve_used_by(volume, info):
        return docker.containers.list(filters={"volume": volume.attrs["Name"]})

    