import os
import time
import argon2
import pyotp
import jwt

from ..utils.registration import registerMutation
from ..redis import client as redis_client

hasher = argon2.PasswordHasher()
ISSUER = "pwnmachine"
SECRET = os.urandom(32)


@registerMutation("login")
def resolve_login(*_, password, otp, expire=None):
    admin_hash = redis_client.get("admin.hash")
    admin_totp = redis_client.get("admin.totp")

    try:
        hasher.verify(admin_hash, password)
    except:
        raise Exception("Invalid password")
    if not pyotp.TOTP(admin_totp).verify(otp):
        raise Exception("Invalid OTP")

    now = int(time.time())
    payload = {"iss": ISSUER, "iat": now}
    if expire is not None:
        payload["exp"] = now + expire

    token = jwt.encode(payload, SECRET)
    redis_client.set(f"admin.tokens.{token}", "*", expire)
    return {"token": token, "expire": payload.get("exp")}


@registerMutation("register")
def resolve_register(*_, password, otp):
    admin_totp = redis_client.get("admin.totp")
    if not pyotp.TOTP(admin_totp).verify(otp):
        raise Exception("Invalid OTP")
    redis_client.set("admin.hash", hasher.hash(password))


def auth_middleware(resolver, obj, info, **args):
    # Skip auth checking for non-root fields
    if info.path.prev is not None:
        return resolver(obj, info, **args)
    # Skip auth checking for introspection queries
    if info.field_name.startswith("__"):
        return resolver(obj, info, **args)
    if info.field_name in ["login", "register"]:
        return resolver(obj, info, **args)

    try:
        headers = info.context["request"].headers
        token = headers["Authorization"].split()[-1]
        jwt.decode(token, SECRET, ["HS256"], issuer=ISSUER)
    except:
        raise Exception("Unauthorized")

    return resolver(obj, info, **args)


# warn('REMOVE DEFAULT PASSWORD AND TOTP')
# redis_client.set('admin.totp', 'W7RPT7JWR6YNSVOB')
# redis_client.set('admin.hash', hasher.hash('admin'))
