import os
import argon2
from datetime import datetime, timedelta
import jwt
from dataclasses import dataclass
from functools import wraps

import pyotp

PASSWORD_KEY = "pm/auth/password"
JWT_SECRET_KEY = "pm/auth/jwtSecret"
TOTP_SECRET_KEY = "pm/auth/totp"

TOKEN_ISSUER = "PwnMachine"

hasher = argon2.PasswordHasher()


class Database:
    _instance = None
    password_hash: bytes = None
    totp_secret: str = None
    jwt_secret: bytes = None
    totp_client: pyotp.TOTP = None
    redis = None

    async def init(self, redis_client):
        from . import AUTH_DISABLED

        self.redis = redis_client
        if AUTH_DISABLED:
            self.password_hash = "nope"
            self.totp_secret = pyotp.random_base32()
            self.jwt_secret = os.urandom(32).hex()
            return self

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
    def is_first_run(self):
        if self.password_hash is None:
            return True
        if self.jwt_secret is None:
            return True
        if self.totp_secret is None:
            return True
        return False

    async def save_password(self, password):
        self.password_hash = hasher.hash(password)
        await self.redis.set(PASSWORD_KEY, self.password_hash)

    async def register(self, password):
        await self.save_password(password)
        return self.make_jwt_token()

    def verify_password(self, password):
        try:
            return hasher.verify(self.password_hash, password)
        except Exception as e:
            return False

    def verify_token(self, token):
        try:
            return jwt.decode(token, self.jwt_secret, ["HS256"], issuer=TOKEN_ISSUER)
        except jwt.exceptions.InvalidTokenError:
            return False

    def verify_otp(self, otp):
        return pyotp.TOTP(self.totp_secret).verify(otp)

    def make_jwt_token(self, duration_days=1):
        now = datetime.now()
        payload = {"iss": TOKEN_ISSUER, "iat": now, "duration_days": duration_days}

        if duration_days:
            payload["exp"] = now + timedelta(days=duration_days)

        return jwt.encode(payload, self.jwt_secret)

    def refresh_token(self, token):
        return self.make_jwt_token(token.get("duration_days", 1))
