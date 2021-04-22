import os
import time
import argon2
import pyotp
import jwt

from starlette.responses import Response
from ..redis import client as redis_client

hasher = argon2.PasswordHasher()
ISSUER = "pwnmachine"
SECRET = os.urandom(32)
COOKIE = "__Host-token"


async def login(request):
    form = await request.form()

    admin_hash = redis_client.get("admin.hash")
    admin_totp = redis_client.get("admin.totp")

    try:
        hasher.verify(admin_hash, form["password"])
    except:
        return Response("Invalid password", 401)
    if not pyotp.TOTP(admin_totp).verify(form["otp"]):
        return Response("Invalid OTP", 401)

    now = int(time.time())
    exp = int(form["expire"])
    payload = {"iss": ISSUER, "iat": now, "exp": now + exp}
    token = jwt.encode(payload, SECRET)

    response = Response()
    response.set_cookie(
        key=COOKIE,
        value=token,
        max_age=exp,
        secure=True,
        httponly=True,
        samesite="Strict",
    )
    return response


async def register(request):
    pass


def auth_middleware(resolver, obj, info, **args):
    # Skip auth checking for non-root fields
    if info.path.prev is not None:
        return resolver(obj, info, **args)
    # Skip auth checking for introspection queries
    if info.field_name.startswith("__"):
        return resolver(obj, info, **args)

    try:
        token = info.context["request"].cookies[COOKIE]
        jwt.decode(token, SECRET, ["HS256"], issuer=ISSUER)
    except:
        raise Exception("Unauthorized")

    return resolver(obj, info, **args)


# warn('REMOVE DEFAULT PASSWORD AND TOTP')
# redis_client.set('admin.totp', 'W7RPT7JWR6YNSVOB')
# redis_client.set('admin.hash', hasher.hash('admin'))
