import aiohttp
import asyncio
import logging
import json
import re
from contextlib import asynccontextmanager, contextmanager
from ..utils import base64_decode

entrypoint_re = re.compile(
    r"(?P<ip>\d+\.\d+\.\d+\.\d+)?:(?P<port>\d+)(?:/(?P<protocol>[a-z]+))?"
)

logger = logging.getLogger("uvicorn")

ROOT = "http://127.0.0.1:8080/api"


def log(msg):
    logger.info(f"[{__name__}] {msg}")


def validate_node_id(nodeId, target_type):
    try:
        type, *args = base64_decode(nodeId, json=True)
        if type != target_type:
            raise ValueError()
        return args
    except Exception as e:
        raise ValueError(f"Invalid nodeId.")


def settings_to_kv(settings, prefix=""):
    for k, v in settings.items():
        if v == None:
            continue
        if isinstance(v, dict):
            yield from settings_to_kv(v, f"{prefix}/{k}")
        elif isinstance(v, list):
            yield from settings_to_kv(dict(enumerate(v)), f"{prefix}/{k}")
        elif isinstance(v, bool):
            yield f"{prefix}/{k}", str(v).lower()
        else:
            yield f"{prefix}/{k}", v


class TraefikRedisApi:
    def __init__(self, client, root, http_api):
        self.client = client
        self.root = root
        self.http_api = http_api

    def _with_root_key(self, key):
        return f"{self.root}/{key.lstrip('/')}"

    def set(self, key, value):
        print("SET", key, value)
        return self.client.set(self._with_root_key(key), value)

    def delete_pattern(self, pattern):
        full_pattern = self._with_root_key(pattern)
        log(f"REDIS delete pattern: {full_pattern}")
        for key in self.client.keys(full_pattern):
            log(f"REDIS delete key: {key.decode()}")
            self.client.delete(key)

    # Service
    async def create_service(self, name, protocol, type, settings):
        redis_name = name.split("@")[0] if "@" in name else name
        prefix = f"/{protocol}/services/{redis_name}/{type}"
        for k, v in settings_to_kv(settings, prefix):
            self.set(k, v)
        service = await self.http_api.wait(f"/{protocol}/services/{redis_name}@redis")
        service["protocol"] = protocol
        return service

    async def delete_service(self, nodeId):
        protocol, name = validate_node_id(nodeId, "service")
        redis_name = name.split("@")[0] if "@" in name else name
        self.delete_pattern(f"/{protocol}/services/{redis_name}/*")
        return await self.http_api.wait_delete(f"/{protocol}/services/{name}")

    # Middleware
    async def delete_middleware(self, nodeId):
        name = validate_node_id(nodeId, "middleware")[0]
        redis_name = name.split("@")[0] if "@" in name else name
        self.delete_pattern(f"/http/middlewares/{redis_name}/*")
        return await self.http_api.wait_delete(f"/http/middlewares/{name}")

    async def create_middleware(self, name, type, settings):
        redis_name = name.split("@")[0] if "@" in name else name
        prefix = f"/http/middlewares/{redis_name}/{type}"
        for k, v in settings_to_kv(settings, prefix):
            self.set(k, v)
        return await self.http_api.wait(f"/http/middlewares/{redis_name}@redis")

    async def update_middleware(self, nodeId, type, settings):
        name = validate_node_id(nodeId, "middleware")[0]
        if not await self.delete_middleware(name):
            raise RuntimeError(f"Unable to update {name}")
        return await self.create_middleware(name, type, settings)

    #


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

    # Entrypoints
    def parse_entrypoint(self, entrypoint):
        groups = entrypoint_re.match(entrypoint["address"]).groupdict()
        ip = groups["ip"] or "0.0.0.0"
        port = groups["port"] or 0
        protocol = groups["protocol"] or "tcp"
        address = f"{ip}:{port}/{protocol}"
        return {
            "ip": ip,
            "port": port,
            "protocol": protocol,
            "address": address,
            "name": entrypoint["name"],
        }

    async def get_entrypoint(self, name):
        entrypoint = await self.get(f"/entrypoints/{name}")
        return self.parse_entrypoint(entrypoint)

    async def get_entrypoints(self):
        entrypoints = []
        for entrypoint in await self.get(f"/entrypoints"):
            entrypoints.append(self.parse_entrypoint(entrypoint))
        return entrypoints

    # Routers

    async def get_router(self, protocol, name):
        router = await self.get(f"/{protocol}/routers/{name}")
        router["protocol"] = protocol
        return router

    async def get_routers(self, protocols=("http", "tcp", "udp")):
        all_routers = []
        for proto in protocols:
            routers = await self.get(f"/{proto}/routers")
            for router in routers:
                router["protocol"] = proto

            all_routers += routers

        return all_routers

    async def get_routers_used_by(self, usedBy, protocols=("http", "tcp", "udp")):
        routers = await self.get_routers(protocols)
        return [router for router in routers if router["name"] in usedBy]

    # Middlewares
    async def get_middleware(self, name):
        return await self.get(f"/http/middlewares/{name}")

    async def get_middlewares(self):
        return await self.get(f"/http/middlewares")

    # Services
    async def get_service(self, protocol, name):
        service = await self.get(f"/{protocol}/services/{name}")
        service["protocol"] = protocol
        return service

    async def get_services(self, protocols=("http", "tcp", "udp")):
        all_services = []
        for proto in protocols:
            services = await self.get(f"/{proto}/services")
            for service in services:
                service["protocol"] = proto
            all_services += services

        return all_services


@asynccontextmanager
async def new_traefik_http_client(root):
    try:
        async with aiohttp.ClientSession() as session:
            yield TraefikHTTPApi(root, session)
    finally:
        pass