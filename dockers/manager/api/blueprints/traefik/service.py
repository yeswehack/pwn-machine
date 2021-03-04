from flask import jsonify, request
from app import traefik_client
from . import bp


def do_add_service(name, type, servers):
    for idx, server in enumerate(servers):
        key = "url" if type == "http" else "address"
        do_set(f"/{type}/services/{name}/loadbalancer/servers/{idx}/{key}", server)


def do_delete_service(name):
    return delete_pattern(f"/*/services/{name}/*")


@bp.route("/services")
def list_services():
    entries = traefik_client.services()
    return jsonify(entries)


@bp.route("/services", methods=["POST"])
def add_service():
    form = request.get_json()
    name = form.get("name")
    type = form.get("type")
    servers = form.get("servers")

    do_add_service(name, type, servers)
    return jsonify(ok(name=f"{name}@redis"))


@bp.route("/services/<old_name>", methods=["POST"])
def update_service(old_name):
    form = request.get_json()
    name = form.get("name")
    type = form.get("type")
    servers = form.get("servers")

    do_delete_service(old_name)
    do_add_service(name, type, servers)
    return jsonify(ok(name=f"{name}@redis"))


@bp.route("/services/<name>", methods=["DELETE"])
def delete_service(name):
    do_delete_service(name)
    return jsonify(ok(name=f"{name}@redis"))