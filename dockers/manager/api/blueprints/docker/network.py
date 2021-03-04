from flask import jsonify, request
from docker.types import IPAMConfig, IPAMPool
from . import bp, docker_client


@bp.route("/networks")
def list_networks():
    networks = docker_client.networks.list(greedy=True)
    return jsonify([network.attrs for network in networks])


def get_ipam_config(form):
    ipam_config = form.get("IPAM", None)
    if ipam_config is None:
        return None
    pool = IPAMPool(
        subnet=ipam_config.get("Subnet", None),
        iprange=ipam_config.get("IPRange", None),
        gateway=ipam_config.get("Gateway", None),
    )
    return IPAMConfig(driver="default", pool_configs=[pool])


@bp.route("/network", methods=["POST"])
def create_network():
    form = request.get_json()
    name = form.get("Name")
    labels = form.get("Labels")
    internal = form.get("Internal")
    ipam = get_ipam_config(form)

    network = docker_client.networks.create(
        name, driver="bridge", ipam=ipam, labels=labels, internal=internal
    )
    return jsonify(network.attrs)