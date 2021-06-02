import os
import pyotp
from functools import wraps
from dataclasses import dataclass


from app.redis import client as redis_client

IS_FIRST_RUN_KEY = "pm/ready"
PASSWORD_KEY = "pm/auth/password"
JWT_SECRET_KEY = "pm/auth/jwtSecret"
TOTP_SECRET_KEY = "pm/auth/totp"


class Database:
    _instance = None
    is_first_run: bool = True
    password_hash: bytes = None
    totp_secret: str = None
    jwt_secret: bytes = None

    async def init(self):
        self.is_first_run = not await redis_client.get(IS_FIRST_RUN_KEY)
        self.password_hash = await redis_client.get(PASSWORD_KEY)
        self.totp_secret = await redis_client.get(TOTP_SECRET_KEY)
        if self.totp_secret is None:
            self.totp_secret = pyotp.random_base32()
            await redis_client.set(TOTP_SECRET_KEY, self.totp_secret)

        self.jwt_secret = await redis_client.get(JWT_SECRET_KEY)
        if self.jwt_secret is None:
            self.jwt_secret = os.urandom(32).hex()
            await redis_client.set(JWT_SECRET_KEY, self.jwt_secret)

        return self

    @property
    def totp_client(self):
        return pyotp.TOTP(self.totp_secret)

    async def set_ready(self, v):
        self.is_first_run = not v
        await redis_client.set(IS_FIRST_RUN_KEY, str(v))

    async def save_password_hash(self, hash):
        self.password_hash = hash
        await redis_client.set(PASSWORD_KEY, hash)

    async def save_totp_client(self, client: pyotp.TOTP, uri: str = None):
        self.totp_client = client
        await redis_client.set(TOTP_URI_KEY, uri or client.provisioning_uri())
