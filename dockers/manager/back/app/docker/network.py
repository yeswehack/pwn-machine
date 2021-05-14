from ..utils import registerQuery, registerMutation, createType
from . import docker_client, KeyValue, formatTime
from docker.errors import APIError

DockerNetwork = createType("DockerNetwork")


@registerQuery("dockerNetworks")
async def resolve_networks(*_):
    return docker_client.networks.list(greedy=True)


@DockerNetwork.field("labels")
async def resolve_network_labels(network, _):
    return [KeyValue(*label) for label in network.attrs["Labels"].items()]


@DockerNetwork.field("created")
async def resolve_network_created(network, _):
    return formatTime(network.attrs["Created"])


@DockerNetwork.field("ipv6")
async def resolve_network_ipv6(network, _):
    return network.attrs["EnableIPv6"]


@DockerNetwork.field("driver")
async def resolve_network_driver(network, _):
    return network.attrs["Driver"]


@DockerNetwork.field("internal")
async def resolve_network_internal(network, _):
    return network.attrs["Internal"]


@DockerNetwork.field("subnet")
async def resolve_network_subnet(network, _):
    return (network.attrs["IPAM"]["Config"] or [{}])[0].get("Subnet")


@DockerNetwork.field("gateway")
async def resolve_network_gateway(network, _):
    return (network.attrs["IPAM"]["Config"] or [{}])[0].get("Gateway")


@DockerNetwork.field("usingContainers")
async def resolve_network_using_containers(network, _):
    return network.containers


@registerMutation("dockerConnectContainerToRouter")
async def connect_container(*_, input):
    network = docker_client.networks.get(input["networkId"])
    container = docker_client.containers.get(input["containerId"])
    try:
        network.connect(container)
    except APIError:
        return False
    return True


@registerMutation("dockerDisconnectContainerFromRouter")
async def connect_container(*_, input):
    network = docker_client.networks.get(input["networkId"])
    container = docker_client.containers.get(input["containerId"])
    try:
        network.disconnect(container)
    except APIError:
        return False
    return True
