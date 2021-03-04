from flask import jsonify, request
from docker.types import IPAMConfig, IPAMPool
from . import bp, docker_client


def json_container(container):
    attrs = container.attrs
    attrs["Name"] = attrs["Name"].lstrip("/")
    return attrs


@bp.route("/containers")
def list_containers():
    containers = docker_client.containers.list(all=True)
    return jsonify([json_container(c) for c in containers])


@bp.route("/container/<name>/pause", methods=["PUT"])
def pause_container(name):
    container = docker_client.containers.get(name)
    container.pause()
    return ""


@bp.route("/container/<name>/unpause", methods=["PUT"])
def unpause_container(name):
    container = docker_client.containers.get(name)
    container.unpause()
    return ""


@bp.route("/container/<name>/start", methods=["PUT"])
def start_container(name):
    container = docker_client.containers.get(name)
    container.start()
    return ""


@bp.route("/container/<name>/stop", methods=["PUT"])
def stop_container(name):
    container = docker_client.containers.get(name)
    container.stop()
    return ""


@bp.route("/container/<name>/restart", methods=["PUT"])
def restart_container(name):
    container = docker_client.containers.get(name)
    container.restart()
    return ""