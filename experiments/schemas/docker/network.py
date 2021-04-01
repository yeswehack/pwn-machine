# pylint: disable=all
import graphene
from .client import docker
from schemas.utils import register_mutation
from docker.types import IPAMPool, IPAMConfig
from docker.errors import APIError
from graphql import GraphQLError
from contextlib import contextmanager


@contextmanager
def catch_api_exception():
    try:
        yield
    except APIError as e:
            raise GraphQLError(e.explanation)


class ConnectedContainer(graphene.ObjectType):
    name = graphene.String()
    mac = graphene.String()
    ipv4 = graphene.String()
    ipv6 = graphene.String()

    def resolve_name(connection, info):
        return connection["Name"]

    def resolve_mac(connection, info):
        return connection["MacAddress"]

    def resolve_ipv4(connection, info):
        return connection["IPv4Address"].split("/")[0]

    def resolve_ipv6(connection, info):
        return connection["IPv6Address"]


class Network(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    driver = graphene.String()
    gateway = graphene.String()
    subnet = graphene.String()
    internal = graphene.Boolean()
    labels = graphene.List("schemas.docker.keyValue.KeyValue")
    used_by = graphene.List("schemas.docker.container.Container")
    connected_containers = graphene.List(ConnectedContainer)

    def resolve_driver(network, info):
        return network.attrs["Driver"]

    def resolve_internal(network, info):
        return network.attrs["Internal"]

    def resolve_name(network, info):
        return network.attrs["Name"]

    def resolve_id(network, info):
        return network.attrs["Name"]

    def resolve_labels(network, info):
        return network.attrs["Labels"].items()

    def resolve_connected_containers(network, info):
        return network.attrs["Containers"].values()

    def resolve_gateway(network, info):
        config = network.attrs["IPAM"]["Config"]
        return None if len(config) == 0 else config[0]["Gateway"]

    def resolve_subnet(network, info):
        config = network.attrs["IPAM"]["Config"]
        return None if len(config) == 0 else config[0]["Subnet"]

    def resolve_used_by(network, info):
        return docker.containers.list(filters={"network": network.attrs["Name"]})


class LabelInput(graphene.InputObjectType):
    key = graphene.String(required=True)
    value = graphene.String(required=True)


def labels_as_object(labels):
    return {label["key"]: label["value"] for label in labels}


@register_mutation()
class deleteDockerNetwork(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    ok = graphene.Boolean()

    def mutate(root, info, name):
        with catch_api_exception():
            network = docker.networks.get(name)
            network.remove()
        return deleteDockerNetwork(ok=True)


@register_mutation()
class detachContainerFromDockerNetwork(graphene.Mutation):
    class Arguments:
        network = graphene.String(required=True)
        container = graphene.String(required=True)

    network = graphene.Field(Network)

    def mutate(root, info, network, container):
        with catch_api_exception():
            network = docker.networks.get(network)
            network.disconnect(container)
            return detachContainerFromDockerNetwork(network=network)



@register_mutation()
class attachContainerToDockerNetwork(graphene.Mutation):
    class Arguments:
        network = graphene.String(required=True)
        container = graphene.String(required=True)

    network = graphene.Field(Network)

    def mutate(root, info, network, container):
        with catch_api_exception():
            network = docker.networks.get(network)
            network.connect(container)
            return attachContainerToDockerNetwork(network=network)

@register_mutation()
class createDockerNetwork(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        internal = graphene.Boolean()
        labels = graphene.List(LabelInput)
        gateway = graphene.String()
        subnet = graphene.String()

    network = graphene.Field(Network)

    def mutate(
        root, info, name, internal=False, gateway=None, subnet=None, labels=None
    ):
        if (gateway or subnet):
            pool_config = IPAMPool(subnet=subnet, gateway=gateway)
            ipam = IPAMConfig(pool_configs=[pool_config])
        else:
            ipam = None
        labels = None if labels is None else labels_as_object(labels)


        with catch_api_exception():
            network = docker.networks.create(
                name, internal=internal, ipam=ipam, check_duplicate=True, labels=labels
            )   
            return createDockerNetwork(network=network)
