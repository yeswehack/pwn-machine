from . import auth_query, auth_mutation, auth_operations
from .database import Database

import os
import time
from warnings import warn
from inspect import isawaitable

import argon2
import pyotp
import jwt


ISSUER = "PwnMachine"

AUTH_DISABLED_ENVVAR = "PM_DISABLE_AUTH"
if AUTH_DISABLED := bool(os.environ.get(AUTH_DISABLED_ENVVAR)):
    warn(f"Never set {AUTH_DISABLED_ENVVAR} in production")

hasher = argon2.PasswordHasher()
db = Database()


@auth_query("authNeedsSetup")
async def resolve_needs_setup(*_):
    if await db.password_hash is None:
        return "PASSWORD"
    if await db.totp_client is None:
        return "TOTP"


@auth_query("authTotpUri")
async def resolve_totp_uri(*_):
    secret = pyotp.random_base32()
    return pyotp.totp.utils.build_uri(secret, ISSUER)


async def make_jwt_auth(expire=None):
    now = int(time.time())
    payload = {"iss": ISSUER, "iat": now}
    if expire is not None:
        payload["exp"] = now + expire

    token = jwt.encode(payload, await db.jwt_secret)
    return {"token": token, "expire": payload.get("exp")}


@auth_mutation("createAuthToken")
async def resolve_create_token(*_, password, totp, expire=None):
    if AUTH_DISABLED is False:
        try:
            hasher.verify(await db.password_hash, password)
        except argon2.exceptions.VerificationError:
            return False
        if not (await db.totp_client).verify(totp):
            return False

    return make_jwt_auth(expire)


@auth_mutation("refreshAuthToken")
async def resolve_resfresh_token(*_, token, expire=None):
    if AUTH_DISABLED is False:
        try:
            jwt.decode(token, await db.jwt_secret, ["HS256"], issuer=ISSUER)
        except jwt.exceptions.InvalidTokenError:
            return None

    return make_jwt_auth(expire)


@auth_mutation("updateAuthPassword")
async def resolve_set_password(*_, password):
    await db.save_password_hash(hasher.hash(password))
    return True


@auth_mutation("updateAuthTotp")
async def resolve_set_totp(*_, uri, totp):
    totp_client = pyotp.parse_uri(uri)
    if not totp_client.verify(totp):
        return False

    await db.save_totp_client(totp_client, uri)
    return True


async def auth_middleware(resolver, obj, info, **args):
    if (
        AUTH_DISABLED is False
        # Check auth only for root fields
        and info.path.prev is None
        # except for introspection queries
        and not info.field_name.startswith("__")
        # except for auth operations
        and info.field_name not in auth_operations
    ):
        try:
            headers = info.context["request"].headers
            token = headers["Authorization"].split()[-1]
            jwt.decode(token, await db.jwt_secret, ["HS256"], issuer=ISSUER)
        except jwt.exceptions.InvalidTokenError:
            raise Exception("Unauthorized")

    res = resolver(obj, info, **args)
    return await res if isawaitable(res) else res
