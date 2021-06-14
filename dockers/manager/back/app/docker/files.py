import os
import shutil
import stat
from dataclasses import dataclass

import magic
from app.auth.auth import verify_jwt
from app.utils import createInterface, registerQuery, registerMutation
from app.exception import PMException
from starlette.responses import FileResponse, PlainTextResponse

from . import docker_client

DockerVolumeExploreEntry = createInterface("DockerVolumeExploreEntry")


@DockerVolumeExploreEntry.type_resolver
def resolve_entry_type(entry, *_):
    mapping = {
        "REG": "DockerVolumeFile",
        "DIR": "DockerVolumeFolder",
        "LNK": "DockerVolumeLink",
    }
    return mapping.get(entry.type, "DockerVolumeUnkownFile")


class VolumeFile:
    def __init__(self, path, volume_path):
        self.fullpath = volume_path
        self.path = path
        self.stat = os.stat(path, follow_symlinks=False)

    @property
    def name(self):
        return os.path.basename(self.path)

    @property
    def type(self):
        types = [
            "DIR",
            "CHR",
            "BLK",
            "FIFO",
            "LNK",
            "SOCK",
            "DOOR",
            "PORT",
            "WHT",
            "REG",
        ]

        for name in types:
            method = getattr(stat, f"S_IS{name}")
            if method and method(self.stat.st_mode):
                return name
        return "UNK"

    @property
    def size(self):
        return self.stat.st_size

    @property
    def mime(self):
        return magic.from_file(self.path, mime=True)

    @property
    def target(self):
        return os.readlink(self.path)


def safe_path(basedir, path, *, follow_link=True):
    parts = [part for part in path.split("/") if part]
    full_path = os.path.join(basedir, *parts)
    if follow_link:
        real_path = os.path.realpath(full_path)
    else:
        real_path = os.path.normpath(full_path)
    if basedir != os.path.commonpath((basedir, real_path)):
        raise ValueError("Invalid path")
    return full_path


def get_volume_path(volume_name, path):
    volume = docker_client.volumes.get(volume_name)
    root_path = volume.attrs["Mountpoint"]
    return safe_path(root_path, path)


@registerQuery("dockerExploreVolume")
def resolve_explore_volume(*_, input):
    volume = docker_client.volumes.get(input.get("volumeName"))
    asked_path = input.get("path", "/")
    root_path = volume.attrs["Mountpoint"]
    full_path = safe_path(root_path, asked_path)

    files = []
    for file in os.listdir(full_path):
        real_path = os.path.join(full_path, file)
        volume_path = real_path[len(root_path) :]
        yield VolumeFile(real_path, volume_path)


@registerMutation("deleteDockerVolumeFile")
def resolve_delete_file(*_, input):
    volume = docker_client.volumes.get(input.get("volumeName"))
    asked_path = input.get("path", "/")
    root_path = volume.attrs["Mountpoint"]
    full_path = safe_path(root_path, asked_path, follow_link=False)

    try:
        if os.path.islink(full_path):
            os.unlink(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            os.remove(full_path)
    except Exception as e:
        raise PMException(e)


async def download_file(request):
    if not verify_jwt(request):
        return PlainTextResponse("Unauthorized", status_code=403)
    not_found = PlainTextResponse("File not found", status_code=404)
    volume = request.query_params.get("volume")
    path = request.query_params.get("path")
    if volume is None or path is None:
        return not_found
    try:
        real_path = get_volume_path(volume, path)
        size = os.stat(real_path)
        return FileResponse(real_path)
    except:
        return not_found


async def upload_file(request):
    if not verify_jwt(request):
        return PlainTextResponse("Unauthorized", status_code=403)
    not_found = PlainTextResponse("File not found", status_code=404)
    volume = request.query_params.get("volume")
    path = request.query_params.get("path")
    if volume is None or path is None:
        return not_found
    try:
        form = await request.form()
        for name, upload in form.items():
            filename = upload.filename
            dest = get_volume_path(volume, os.path.join(path, filename))
            contents = await upload.read()
            with open(dest, "wb") as f:
                f.write(contents)
    except Exception as e:
        return PlainTextResponse(str(e))
    return PlainTextResponse(dest)
