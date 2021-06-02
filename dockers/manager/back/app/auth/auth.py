from . import USERNAME, ISSUER, auth_query, auth_mutation, auth_operations
from .database import Database

import os
import time
from warnings import warn
from inspect import isawaitable

import argon2
import pyotp
import jwt


AUTH_DISABLED_ENVVAR = "PM_DISABLE_AUTH"
if AUTH_DISABLED := bool(os.environ.get(AUTH_DISABLED_ENVVAR)):
    warn(f"Never set {AUTH_DISABLED_ENVVAR} in production")

hasher = argon2.PasswordHasher()
db = Database()


@auth_query("authSetupNeeded")
async def resolve_setup_needed(*_):
    if await db.password_hash is None:
        return "PASSWORD"
    if await db.totp_client is None:
        return "TOTP"


@auth_query("authTotpUri")
async def resolve_totp_uri(*_):
    secret = pyotp.random_base32()
    return pyotp.totp.utils.build_uri(secret, USERNAME, issuer=ISSUER)


async def make_jwt_token(expire=None):
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
            return None
        if not (await db.totp_client).verify(totp):
            return None

    return await make_jwt_token(expire)


@auth_mutation("refreshAuthToken")
async def resolve_resfresh_token(*_, token, expire=None):
    if AUTH_DISABLED is False:
        try:
            jwt.decode(token, await db.jwt_secret, ["HS256"], issuer=ISSUER)
        except jwt.exceptions.InvalidTokenError:
            return None

    return await make_jwt_token(expire)


@auth_mutation("updateAuthPassword", skip_auth=resolve_setup_needed)
async def resolve_update_password(*_, current, new):
    if AUTH_DISABLED is False:
        try:
            hasher.verify(await db.password_hash, current)
        except argon2.exceptions.VerificationError:
            return False

    await db.save_password_hash(hasher.hash(new))
    return True


@auth_mutation("updateAuthTotp", skip_auth=resolve_setup_needed)
async def resolve_update_totp(*_, uri, totp):
    totp_client: pyotp.TOTP = pyotp.parse_uri(uri)
    if not totp_client.verify(f"{totp:0{totp_client.digits}}"):
        return False

    await db.save_totp_client(totp_client, uri)
    return True


async def auth_middleware(resolver, obj, info, **args):
    skip_auth = auth_operations.get(info.field_name)
    if callable(skip_auth):
        skip_auth = skip_auth()
    if isawaitable(skip_auth):
        skip_auth = await skip_auth

    if (
        AUTH_DISABLED is False
        # Check auth only for root fields
        and info.path.prev is None
        # except for introspection queries
        and not info.field_name.startswith("__")
        # except for auth operations
        and not skip_auth
    ):
        try:
            headers = info.context["request"].headers
            token = headers["Authorization"].split()[-1]
            jwt.decode(token, await db.jwt_secret, ["HS256"], issuer=ISSUER)
        except (KeyError, jwt.exceptions.InvalidTokenError):
            raise Exception("Unauthorized")

    res = resolver(obj, info, **args)
    return await res if isawaitable(res) else res
