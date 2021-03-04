from flask import Blueprint, jsonify, request, send_from_directory
import shlex
from werkzeug.utils import secure_filename
import copy
import stat
import os
import shutil
import mimetypes
from functools import wraps
from app import docker_client

from . import bp


@bp.route("/volumes")
def list_volumes():
    volumes = docker_client.volumes.list()
    return jsonify([c.attrs for c in volumes])


def get_file_type(st_mode):
    types = ["DIR", "CHR", "BLK", "REG", "FIFO", "LNK", "SOCK", "DOOR", "PORT", "WHT"]

    for name in types:
        method = getattr(stat, f"S_IS{name}")
        if method and method(st_mode):
            return name
    return "UNK"


@bp.route("/volume/<volume_name>/<path:path>")
@bp.route("/volume/<volume_name>")
def ls_volume(volume_name, path=""):
    volume = docker_client.volumes.get(volume_name)
    volume_root = volume.attrs["Mountpoint"]
    path = f"{volume_root}/{os.path.normpath(path)}"
    files = {}
    for file in os.listdir(path):
        fullpath = os.path.join(path, file)
        file_stat = os.stat(fullpath)
        info = {}
        info["size"] = file_stat.st_size
        info["mime"] = mimetypes.guess_type(fullpath)
        info["mode"] = stat.filemode(file_stat.st_mode)
        info["type"] = get_file_type(file_stat.st_mode)

        files[file] = info
    return jsonify(files)


@bp.route("/volume", methods=["POST"])
def create_volume():
    form = request.get_json()
    name = form.get("Name")
    labels = form.get("Labels")
    volume = docker_client.volumes.create(name, labels=labels)
    return jsonify(volume.attrs)


@bp.route("/download/<volume_name>/<path:path>")
def download_file(volume_name, path):
    volume = docker_client.volumes.get(volume_name)
    volume_root = volume.attrs["Mountpoint"]
    return send_from_directory(volume_root, path, as_attachment=True, conditional=True)


@bp.route("/upload/<volume_name>/<path:path>", methods=["POST"], strict_slashes=False)
@bp.route("/upload/<volume_name>", methods=["POST"], strict_slashes=False)
def upload_file(volume_name, path=""):
    volume = docker_client.volumes.get(volume_name)
    volume_root = volume.attrs["Mountpoint"]
    for fname in request.files:
        f = request.files.get(fname)
        full_path = os.path.join(volume_root, path, secure_filename(fname))
        f.save(full_path)

    return jsonify({})


@bp.route("/delete/<volume_name>/<path:path>", methods=["DELETE"], strict_slashes=False)
def delete_file(volume_name, path=""):
    volume = docker_client.volumes.get(volume_name)
    volume_root = volume.attrs["Mountpoint"]
    full_path = os.path.join(volume_root, path)
    if os.path.isfile(full_path):
        os.remove(full_path)
    else:
        shutil.rmtree(full_path)
    return jsonify({})