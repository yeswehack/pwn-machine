#!/usr/bin/env python
from flask import Blueprint, jsonify, request
from app import dns_client
from collections import defaultdict
from flask import current_app

bp = Blueprint("dns", __name__)


def ok(**kwargs):
    return {"msg": "ok", **kwargs}



@bp.route("/zones")
def list_zones():
    entries = dns_client.zones()
    return jsonify(entries)




@bp.route("/zones", methods=["post"])
def create_zone():
    form = request.get_json()
    zone = dns_client.createZone(form)
    return jsonify(zone)