import aiohttp
import asyncio
import logging
from contextlib import asynccontextmanager, contextmanager

logger = logging.getLogger("uvicorn")

ROOT = "http://127.0.0.1:8080/api"


def log(msg):
    logger.info(f"[{__name__}] {msg}")


class TraefikRedisApi:
    def __init__(self, client, root):
        self.client = client
        self.root = root

    def _with_root_key(self, key):
        return f"{self.root}/{key.lstrip('/')}"

    def set(self, key, value):
        return self.client.set(self._with_root_key(key), value)

    def delete_pattern(self, pattern):
        full_pattern = self._with_root_key(pattern)
        log(f"REDIS delete pattern: {full_pattern}")
        for key in self.client.keys(full_pattern):
            log(f"REDIS delete key: {key}")
            self.client.delete(key)


class TraefikHTTPApi:
    def __init__(self, root, session):
        self.root = root
        self.session = session
        self.cache = {}
        self.runnings = set()
        return

    async def _get(self, path):
        log(f"API GET {path}")

        full_path = f"{self.root.rstrip('/')}/{path.lstrip('/')}"

        async with self.session.get(full_path) as response:
            return await response.json()

    @contextmanager
    def running(self, name):
        try:
            self.runnings.add(name)
            yield
        finally:
            self.runnings.remove(name)

    # All responses are cached for the duration of the HTTP request
    async def get(self, path, allow_cache=True):
        if allow_cache:
            while path in self.runnings:
                await asyncio.sleep(0.1)
            if path in self.cache:
                return self.cache[path]

            with self.running(path):
                response = await self._get(path)
        else:
            response = await self._get(path)

        self.cache[path] = response
        return response

    # Do request until it succede
    # if it fail wait more and more .1 -> 1
    async def wait(self, path):
        max_try = 10
        while max_try := max_try - 1:
            try:
                return await self.get(path, allow_cache=False)
            except:
                await asyncio.sleep(0.1 * (10 - max_try))

    # Do request until it fail
    # if it succede wait more and more .1 -> 1
    async def wait_delete(self, path):
        max_try = 10
        try:
            while max_try := max_try - 1:
                await self.get(path, allow_cache=False)
                await asyncio.sleep(0.1 * (10 - max_try))
            return False
        except Exception as e:
            return True


@asynccontextmanager
async def new_traefik_http_client(root):
    try:
        async with aiohttp.ClientSession() as session:
            yield TraefikHTTPApi(root, session)
    finally:
        pass