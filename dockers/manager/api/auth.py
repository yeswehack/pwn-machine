import os
import pyotp
import json
import fnmatch
import shelve
import warnings
import time
import re
from collections import namedtuple
from flask import redirect, url_for, session, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash


Token = namedtuple("Token", ["grant", "expire"])



def create_token(grant, duration):
    from app import redis_client

    key = os.urandom(32).hex()
    redis_key = f"admin.tokens.{key}"

    redis_client.set(redis_key, grant)
    expire = 0
    if duration:
        expire = int(time.time() + duration)
        redis_client.expire(redis_key, duration)

    token = {
        "token": key,
        "expire": expire,
        "grant": grant
    }
    return token


def verify_token(key, path):
    from app import redis_client

    grant = redis_client.get(f"admin.tokens.{key}")
    if grant is None:
        raise AuthenticationException("Invalid token")

    if not fnmatch.fnmatch(path, grant.decode()):
        raise AuthenticationException("Unauthorized")
    return True


def auth(password, otp, grant, duration):
    from app import redis_client

    warnings.warn("REMOVE DEFAULT PASSWORD")
    redis_client.set("admin.hash", generate_password_hash("test"))
    redis_client.set("admin.totp", "W7RPT7JWR6YNSVOB")

    admin_hash = redis_client.get("admin.hash").decode()
    admin_totp = redis_client.get("admin.totp").decode()

    is_password_valid = check_password_hash(admin_hash, password)

    warnings.warn("REMOVE DEFAULT TOTP")
    is_otp_valid = otp == "000000" or pyotp.TOTP(admin_totp).verify(otp)

    if is_password_valid and is_otp_valid:
        return create_token(grant, duration)
    return {"err": "Invalid password or OTP."}


class AuthenticationException(Exception):
    pass


def init_app(app):
    BEARER_REGEX = re.compile(r"^Bearer (?P<token>.*)$", re.IGNORECASE)

    @app.route("/api/authenticate", methods=["GET", "POST"])
    def authenticate():
        if request.method == "POST":
            form = request.get_json()
            password = form.get("password", "")
            otp = form.get("otp", "")
            duration = int(form.get("duration", 60 * 60 * 24))
            grant = form.get("grant", "*")
            return jsonify(auth(password, otp, grant, duration))

    @app.before_request
    def before_request():
        if request.method == "OPTIONS":
            return
        if request.endpoint == "authenticate":
            return
        if request.endpoint == "static_front":
            return
        authorization = request.headers.get("Authorization", "")
        match = BEARER_REGEX.match(authorization)
        if match is None:
            return jsonify({"err": "Missing authorization token"}), 401
        token = match.group("token")
        try:
            verify_token(token, request.path)
        except AuthenticationException as e:
            return jsonify({"err": str(e)}), 401

        return