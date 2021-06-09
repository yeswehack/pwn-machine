#!/usr/bin/env python3

import asyncio
from app.redis import client as redis_client
from app.auth.database import PASSWORD_KEY, TOTP_URI_KEY, JWT_SECRET_KEY

asyncio.run(redis_client.delete(PASSWORD_KEY, TOTP_URI_KEY, JWT_SECRET_KEY))
