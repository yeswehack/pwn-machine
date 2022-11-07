from app.utils import registerQuery, registerMutation, createType
from . import docker_client, KeyValue, formatTime, kv_to_dict
from docker.errors import APIError, NotFound
from docker.types import IPAMConfig, IPAMPool
from app.exception import PMException

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
    network_name = network.name
    containers = docker_client.containers.list(
        all=True, filters={"network": network_name}
    )
    get_not_empty = lambda d, k: d.get(k, None) or None
    for container in containers:
        con = container.attrs["NetworkSettings"]["Networks"][network_name]
        ip_address = con.get("IPAddress") or None
        aliases = con.get("Aliases", [])
        yield {
            "ipAddress": ip_address,
            "aliases": aliases,
            "container": container,
            "containerName": container.name,
        }


def resolve_network_using_containers(network, _):
    return network.attrs["Containers"].values()


@registerMutation("createDockerNetwork")
def resolve_create_network(*_, input):
    name = input.get("name")
    labels = kv_to_dict(input.get("labels"))
    internal = input.get("internal")

    ipam = IPAMConfig(
        pool_configs=[
            IPAMPool(
                entry.get("subnet"),
                entry.get("ipRange"),
                entry.get("gateway"),
            )
            for entry in input.get("ipams") or []
        ]
    )

    try:
        docker_client.networks.create(
            name,
            check_duplicate=True,
            labels=labels,
            driver="bridge",
            internal=internal,
            ipam=ipam,
        )
    except APIError as e:
        raise PMException(e.explanation)
    except Exception as e:
        raise PMException(str(e))


@registerMutation("deleteDockerNetwork")
def mutation_delete_network(*_, id):
    try:
        network = docker_client.networks.get(id)
        network.remove()
    except APIError as e:
        raise PMException(e.explanation)
    except Exception as e:
        raise PMException(str(e))


@registerMutation("connectDockerContainer")
def resolve_connect_container(*_, input):
    network = docker_client.networks.get(input["networkId"])
    container = docker_client.containers.get(input["containerId"])
    aliases = input.get("aliases") or []
    try:
        network.connect(container, aliases=aliases)
    except APIError as e:
        raise PMException(e.explanation)
    except Exception as e:
        raise PMException(str(e))


@registerMutation("disconnectDockerContainer")
def resolve_disconnect_container(*_, input):
    try:
        docker_client.api.disconnect_container_from_network(
            input["containerId"],
            input["networkId"],
        )
    except APIError as e:
        raise PMException(e.explanation)
    except Exception as e:
        raise PMException(str(e))


@registerMutation("deleteDockerNetwork")
def resolve_remove_network(*_, id):
    try:
        docker_client.api.remove_network(id)
    except APIError as e:
        raise PMException(e.explanation)
    except Exception as e:
        raise PMException(str(e))


@registerMutation("pruneDockerNetworks")
def resolve_prune_networks(*_):
    pruned = docker_client.networks.prune()
    return {
        "deleted": pruned["NetworksDeleted"] or [],
        "spaceReclaimed": 0,
    }
