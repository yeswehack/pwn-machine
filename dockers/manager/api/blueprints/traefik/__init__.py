#!/usr/bin/env python
from flask import Blueprint, jsonify, request
from app import redis_client, docker_client, traefik_client
from collections import defaultdict
from flask import current_app

bp = Blueprint("traefik", __name__)


def ok(**kwargs):
    return {"msg": "ok", **kwargs}


def do_set(key, value):
    root = current_app.config["TRAEFIK_REDIS_ROOK_KEY"]
    key = key.lstrip("/")
    print("SET", f"{root}/{key}", value)
    redis_client.set(f"{root}/{key}", value)


def delete_pattern(pattern):
    root = current_app.config["TRAEFIK_REDIS_ROOK_KEY"]
    pattern = pattern.lstrip("/")
    search = f"{root}/{pattern}"
    print("DELETE", search)
    for key in redis_client.keys(search):
        print("DELETE", key)
        redis_client.delete(key)


def settings_to_kv(settings, prefix=""):
    for k, v in settings.items():
        if v == None:
            continue

        if isinstance(v, dict):
            yield from settings_to_kv(v, f"{prefix}/{k}")
        elif isPair(v):
            for name, value in v:
                if name is None:
                    continue
                yield f"{prefix}/{k}/{name}", value
        elif isinstance(v, list):
            for idx, value in enumerate(v):
                yield f"{prefix}/{k}/{idx}", value
        elif isinstance(v, bool):
            yield f"{prefix}/{k}", str(v).lower()
        else:
            yield f"{prefix}/{k}", v


# ENTRYPOINTS ROUTES


@bp.route("/entrypoints")
def list_entrypoints():
    entries = traefik_client.entrypoints()
    for entry in entries:
        if entry["address"].endswith("/udp"):
            entry["address"] = entry["address"][:-4]
            entry["type"] = "udp"
        else:
            entry["type"] = "tcp"
    return jsonify(entries)


# SERVICES UTILS


def do_add_service(name, type, servers):
    for idx, server in enumerate(servers):
        key = "url" if type == "http" else "address"
        do_set(f"/{type}/services/{name}/loadbalancer/servers/{idx}/{key}", server)


def do_delete_service(name):
    return delete_pattern(f"/*/services/{name}/*")


# SERVICE ROUTES
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


# ROUTERS UTILS
def do_delete_router(name):
    return delete_pattern(f"/*/routers/{name}/*")


def do_delete_router_middlewares(name):
    return delete_pattern(f"/http/routers/{name}/middlewares/*")


def do_add_router(name, rule, type, service, entrypoints):
    if rule and rule.strip():
        do_set(f"/{type}/routers/{name}/rule", rule)
    do_set(f"/{type}/routers/{name}/service", service)
    for idx, entrypoint in enumerate(entrypoints):
        do_set(f"/{type}/routers/{name}/entrypoints/{idx}", entrypoint)


# ROUTERS ROUTES


@bp.route("/routers")
def list_routers():
    entries = traefik_client.routers()
    return jsonify(entries)


@bp.route("/routers", methods=["POST"])
def add_router():
    form = request.get_json()
    name = form.get("name")
    rule = form.get("rule")
    type = form.get("type")
    service = form.get("service")
    entrypoints = form.get("entrypoints")

    do_add_router(name, rule, type, service, entrypoints)
    return jsonify(ok(name=f"{name}@redis"))


@bp.route("/routers/<old_name>", methods=["POST"])
def update_router(old_name):
    form = request.get_json()
    name = form.get("name")
    rule = form.get("rule")
    type = form.get("type")
    service = form.get("service")
    entrypoints = form.get("entrypoints")
    do_delete_router(old_name)
    do_add_router(name, rule, type, service, entrypoints)
    return jsonify(ok(name=f"{name}@redis"))


@bp.route("/routers/<name>/middlewares", methods=["POST"])
def update_router_middlewares(name):
    middlewares = request.get_json()
    do_delete_router_middlewares(name)
    for idx, middleware in enumerate(middlewares):
        do_set(f"/http/routers/{name}/middlewares/{idx}", middleware)
    return jsonify(ok(name=f"{name}@redis"))


@bp.route("/routers/<name>", methods=["DELETE"])
def delete_router(name):
    do_delete_router(name)
    return jsonify(ok(name=f"{name}@redis"))


# MIDDLEWARES UTILS
def isPair(item):
    if not isinstance(item, list):
        return False

    # all items are a list of len 2
    return all((isinstance(i, list) and len(i) == 2) for i in item)


def do_delete_middleware(name):
    return delete_pattern(f"/http/middlewares/{name}/*")


def do_add_middleware(name, type, settings):
    for k, v in settings_to_kv(settings, f"{name}/{type}"):
        do_set(f"/http/middlewares/{k}", v)


# MIDDLEWARES ROUTES


@bp.route("/middlewares")
def list_middlewares():
    entries = traefik_client.middlewares()
    return jsonify(entries)


@bp.route("/middlewares", methods=["POST"])
def add_middleware():
    form = request.get_json()
    name = form.get("name")
    type = form.get("type")
    settings = form.get("settings")
    do_add_middleware(name, type, settings)
    return jsonify(ok(name=f"{name}@redis"))


@bp.route("/middlewares/<old_name>", methods=["POST"])
def update_middleware(old_name):
    form = request.get_json()
    name = form.get("name")
    type = form.get("type")
    settings = form.get("settings")
    do_delete_middleware(old_name)
    do_add_middleware(name, type, settings)
    return jsonify(ok(name=f"{name}@redis"))


@bp.route("/middlewares/<name>", methods=["DELETE"])
def delete_middleware(name):
    do_delete_middleware(name)
    return jsonify(ok(name=f"{name}@redis"))