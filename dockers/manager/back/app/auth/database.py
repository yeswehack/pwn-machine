import os
import pyotp

from app.redis import client as redis_client


PASSWORD_KEY = "admin.password"
TOTP_URI_KEY = "admin.totp"
JWT_SECRET_KEY = "secret"


class Database:
    _password_hash: bytes = None
    _totp_client: pyotp.TOTP = None
    _jwt_secret: bytes = None

    @property
    async def password_hash(self):
        if self._password_hash is None:
            self._password_hash = await redis_client.get(PASSWORD_KEY)
        return self._password_hash

    async def save_password_hash(self, hash):
        self._password_hash = hash
        await redis_client.set(PASSWORD_KEY, hash)

    @property
    async def totp_client(self) -> pyotp.TOTP:
        if self._totp_client:
            return self._totp_client
        if totp_uri := await redis_client.get(TOTP_URI_KEY):
            self._totp_client = pyotp.parse_uri(totp_uri)
        return self._totp_client

    async def save_totp_client(self, client: pyotp.TOTP, uri: str = None):
        self._totp_client = client
        await redis_client.set(TOTP_URI_KEY, uri or client.provisioning_uri())

    @property
    async def jwt_secret(self):
        if self._jwt_secret:
            return self._jwt_secret
        self._jwt_secret = await redis_client.get(JWT_SECRET_KEY)
        if not self._jwt_secret:
            self._jwt_secret = os.urandom(32)
            await redis_client.set(JWT_SECRET_KEY, self._jwt_secret)
        return self._jwt_secret
