import os
import time
from inspect import isawaitable

import argon2
import jwt
import pyotp
from app.utils import registerMutation
from app.exception import PMException

from . import AUTH_DISABLED, auth_mutation, auth_operations, auth_query, db

USERNAME = "admin"
ISSUER = "PwnMachine"
TWO_DAYS = 3600 * 24 * 2


hasher = argon2.PasswordHasher()


def check_token(token):
    try:
        jwt.decode(token, db.jwt_secret, ["HS256"], issuer=ISSUER)
    except jwt.exceptions.InvalidTokenError:
        return False
    return True


@auth_query("authSetupNeeded")
async def resolve_setup_needed(*_):
    if db.password_hash is None:
        return "PASSWORD"
    if db.totp_client is None:
        return "TOTP"


@auth_query("authTotpUri")
async def resolve_totp_uri(*_):
    if not db.is_first_run:
        return None
    otp = pyotp.TOTP(db.totp_secret)
    return otp.provisioning_uri(name=USERNAME, issuer_name=ISSUER)


async def make_jwt_token(expire=TWO_DAYS):
    now = int(time.time())
    payload = {"iss": ISSUER, "iat": now}
    if expire is not None:
        payload["exp"] = now + expire

    token = jwt.encode(payload, db.jwt_secret)
    return {"token": token, "expire": expire}


@auth_mutation("login")
async def resolve_create_token(*_, password, otp, expire=None):
    print(dir(argon2.exceptions))
    try:
        hasher.verify(db.password_hash, password)
    except Exception as e:
        raise PMException("Invalid credentials.")
    if not db.totp_client.verify(otp):
        raise PMException("Invalid credentials.")

    token = await make_jwt_token(expire)
    return token


@auth_mutation("validateAuthToken")
async def resolve_validate_token(*_, token, expire=None):
    isFirstRun = db.is_first_run
    if AUTH_DISABLED or check_token(token):
        return {"token": make_jwt_token(expire), "isFirstRun": isFirstRun}
    else:
        return {"isFirstRun": isFirstRun}


@registerMutation("updatePassword")
async def resolve_update_password(*_, old, new):
    try:
        hasher.verify(db.password_hash, old)
    except Exception as e:
        raise PMException("Invalid password.")

    await db.save_password_hash(hasher.hash(new))


@auth_mutation("initializeAuth")
async def resolve_initialize_auth(*_, password, otp):
    if not db.is_first_run:
        raise PMException("PwnMachine is already setup.")
    otp_client = pyotp.TOTP(db.totp_secret)
    if not otp_client.verify(otp):
        raise PMException("Invalid OTP.")

    await db.save_password_hash(hasher.hash(password))
    await db.set_ready(True)
    return make_jwt_token()


async def auth_middleware(resolver, obj, info, **args):
    skip_auth = auth_operations.get(info.field_name)
    if (
        # Check auth only for root fields
        info.path.prev is None
        # except for introspection queries
        and not info.field_name.startswith("__")
        # except for auth operations
        and not skip_auth
    ):
        try:
            headers = info.context["request"].headers
            token = headers["Authorization"].split()[-1]
            jwt.decode(token, db.jwt_secret, ["HS256"], issuer=ISSUER)
        except (KeyError, jwt.exceptions.InvalidTokenError):
            raise Exception("Unauthorized")

    res = resolver(obj, info, **args)
    return await res if isawaitable(res) else res
