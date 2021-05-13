from ..utils import registerQuery, createType
from . import docker_client, KeyValue
from datetime import datetime

DockerNetwork = createType("DockerNetwork")


@registerQuery("dockerNetworks")
async def resolve_networks(*_):
    return docker_client.networks.list(greedy=True)


@DockerNetwork.field("labels")
async def resolve_network_labels(network, _):
    return [KeyValue(label) for label in network.attrs["Labels"].items()]


@DockerNetwork.field("created")
async def resolve_network_created(network, _):
    return str(datetime.fromisoformat(network.attrs["Created"].partition(".")[0]))


@DockerNetwork.field("ipv6")
async def resolve_network_ipv6(network, _):
    return network.attrs["EnableIPv6"]
