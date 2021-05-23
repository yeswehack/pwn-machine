from app.utils import registerQuery, registerMutation, createType
from . import docker_client, KeyValue, formatTime, kv_to_dict
from docker.errors import APIError, NotFound
from docker.types import IPAMConfig, IPAMPool

DockerNetwork = createType("DockerNetwork")
DockerNetworkConnection = createType("DockerNetworkConnection")


@registerQuery("dockerNetworks")
def resolve_networks(*_):
    return docker_client.networks.list(greedy=True)


@DockerNetwork.field("labels")
def resolve_network_labels(network, _):
    for label in network.attrs["Labels"].items():
        yield KeyValue(*label)


@DockerNetwork.field("created")
def resolve_network_created(network, _):
    return formatTime(network.attrs["Created"])


@DockerNetwork.field("ipv6")
def resolve_network_ipv6(network, _):
    return network.attrs["EnableIPv6"]


@DockerNetwork.field("driver")
def resolve_network_driver(network, _):
    return network.attrs["Driver"]


@DockerNetwork.field("builtin")
def resolve_network_builtin(network, _):
    return network.name in ["bridge", "host", "none"]


@DockerNetwork.field("internal")
def resolve_network_internal(network, _):
    return network.attrs["Internal"]


@DockerNetwork.field("ipams")
def resolve_network_ipams(network, _):
    for ipam in network.attrs["IPAM"]["Config"]:
        yield {
            "subnet": ipam.get("Subnet"),
            "ipRange": ipam.get("IPRange"),
            "gateway": ipam.get("Gateway"),
        }


@DockerNetwork.field("usedBy")
def resolve_network_connections(network, _):
    for id, endpoint in network.attrs["Containers"].items():
        yield {
            "ipv4Address": endpoint["IPv4Address"].rpartition("/")[0] or None,
            "ipv6Address": endpoint["IPv6Address"] or None,
            "container": docker_client.containers.get(id),
        }


def resolve_network_using_containers(network, _):
    return network.attrs["Containers"].values()


@registerMutation("createDockerNetwork")
def resolve_create_network(*_, input):
    name = input.get("name")
    labels = kv_to_dict(input.get("labels"))
    enable_ipv6 = input.get("ipv6")
    internal = input.get("internal")
    pool_configs = []
    ipams = input.get("ipams", [])
    ipam = None
    if ipams:
        pool_configs = []
        for entry in ipams:
            pool_configs.append(
                IPAMPool(
                    entry.get("subnet", None),
                    entry.get("ipRange", None),
                    entry.get("gateway", None),
                )
            )
        ipam = IPAMConfig(pool_configs)
    return docker_client.networks.create(
        name,
        check_duplicate=True,
        labels=labels,
        enable_ipv6=enable_ipv6,
        driver="bridge",
        internal=internal,
        ipam=ipam,
    )


@registerMutation("deleteDockerNetwork")
def mutation_delete_network(*_, id):
    try:
        network = docker_client.networks.get(id)
    except APIError:
        raise ValueError("Invalid network ID")
    try:
        network.remove()
    except APIError as e:
        raise ValueError(e.explanation)
    return True


@registerMutation("connectDockerContainer")
def resolve_connect_container(*_, input):
    network = docker_client.networks.get(input["networkId"])
    container = docker_client.containers.get(input["containerId"])
    try:
        network.connect(container)
    except APIError:
        return False
    return True


@registerMutation("disconnectDockerContainer")
def resolve_disconnect_container(*_, input):
    network = docker_client.networks.get(input["networkId"])
    container = docker_client.containers.get(input["containerId"])
    try:
        network.disconnect(container)
    except APIError:
        return False
    return True


@registerMutation("deleteDockerNetwork")
def resolve_remove_network(*_, id):
    try:
        docker_client.api.remove_network(id)
    except (NotFound, APIError):
        return False
    return True


@registerMutation("pruneDockerNetworks")
def resolve_prune_networks(*_):
    pruned = docker_client.networks.prune()
    return {
        "deleted": pruned["NetworksDeleted"] or [],
        "spaceReclaimed": 0,
    }
