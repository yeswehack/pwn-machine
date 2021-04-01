# pylint: disable=no-self-argument
import graphene
from . import network
from .client import docker
from schemas.utils import register_query


@register_query("docker")
class Docker(graphene.ObjectType):
    id = graphene.ID(default_value="DOCKER")
    image = graphene.Field("schemas.docker.image.Image", name=graphene.String())
    images = graphene.List("schemas.docker.image.Image")
    container = graphene.Field("schemas.docker.container.Container", name=graphene.String())
    containers = graphene.List("schemas.docker.container.Container")
    volume = graphene.Field("schemas.docker.volume.Volume", name=graphene.String())
    volumes = graphene.List("schemas.docker.volume.Volume")
    network = graphene.Field("schemas.docker.network.Network", name=graphene.String())
    networks = graphene.List("schemas.docker.network.Network")

    def resolve_image(root, info, name):
        return docker.images.get(name)

    def resolve_images(root, info):
        return docker.images.list()

    def resolve_container(root, info, name):
        return docker.containers.get(name)

    def resolve_containers(root, info):
        return docker.containers.list()

    def resolve_volume(root, info, name):
        return docker.volumes.get(name)

    def resolve_volumes(root, info):
        return docker.volumes.list()

    def resolve_network(root, info, name):
        return docker.networks.get(name)

    def resolve_networks(root, info):
        return docker.networks.list(greedy=True)
