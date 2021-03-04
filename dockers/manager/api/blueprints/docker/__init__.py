#!/usr/bin/env python
from flask import Blueprint, jsonify, request
import copy
from functools import wraps
from app import docker_client

bp = Blueprint("docker", __name__)

from . import volume
from . import network
from . import container


@bp.route("/images")
def list_images():
    seen = set()
    images = docker_client.images.list()
    images_attrs = []
    for image in images:
        for rtag in image.attrs["RepoTags"]:
            attrs = copy.deepcopy(image.attrs)
            if rtag not in seen:
                seen.add(rtag)
                repo, _, tag = rtag.partition(":")
                attrs["Repository"] = repo
                attrs["Tag"] = tag
                images_attrs.append(attrs)

    return jsonify(images_attrs)
