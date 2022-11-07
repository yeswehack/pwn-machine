import os
import asyncio

import jwt
import pyotp
from app.utils import registerMutation
from app.exception import PMException

from . import AUTH_DISABLED, auth_mutation, auth_operations, auth_query, db

USERNAME = "admin"
AUTHENTICATED = "authenticated"


@auth_query("otpSecret")
async def resolve_otp_secret(_, info):
    if not db.is_first_run:
        raise PMException("PwnMachine is already setup.")
    return db.totp_secret


@auth_mutation("login")
def resolve_create_token(*_, input):
    # always do both operation to avoid timming attack
    password_ok = db.verify_password(input["password"])
    otp_ok = db.verify_otp(input["otp"])
    if password_ok and otp_ok:
        return db.make_jwt_token(input.get("durationDays", 1))

    raise PMException("Invalid credentials.")


@auth_mutation("refreshToken")
def resolve_refresh_token(*_, token):
    response = {"isFirstRun": db.is_first_run}
    if token := db.verify_token(token):
        response["token"] = db.refresh_token(token)
    if AUTH_DISABLED:
        response["token"] = db.make_jwt_token()

    return response


@registerMutation("updatePassword")
async def resolve_update_password(*_, old, new):
    if not db.verify_password(old):
        raise PMException("Invalid password.")

    await db.save_password(new)

@registerMutation("resetJWTSecret")
async def resolve_reset_jwt_secret(*_):
    await db.reset_jwt_secret()
    return True

@auth_mutation("initializeAuth")
async def resolve_initialize_auth(*_, password, otp):
    if not db.is_first_run:
        raise PMException("PwnMachine is already setup.")

    if not db.verify_otp(otp):
        raise PMException("Invalid OTP.")

    return await db.register(password)


def verify_jwt(request):
    try:
        token = request.headers["Authorization"].split()[-1]
        claim = jwt.decode(token, db.jwt_secret, ["HS256"])
        return claim
    except Exception:
        return False


def verify_auth(info):
    # Only check for root field
    if info.path.prev is not None:
        return True

    # Skip auth for some queries like login and setup
    if auth_operations.get(info.field_name):
        return True

    # Skip introspection queries
    if info.field_name.startswith("__"):
        return True

    if claim := verify_jwt(info.context["request"]):
        info.context[AUTHENTICATED] = claim
        return True
    return False


async def auth_middleware(resolver, obj, info, **args):
    if not AUTH_DISABLED and not verify_auth(info):
        raise Exception("Unauthorized")

    if asyncio.iscoroutinefunction(resolver):
        return await resolver(obj, info, **args)
    return resolver(obj, info, **args)
