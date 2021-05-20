import asyncio
import json
import logging
import re
from contextlib import asynccontextmanager, contextmanager

import aiohttp

from app.utils import base64_decode, validate_node_id
from app.utils.cached import cacheMethodForQuery, no_cache

entrypoint_re = re.compile(
    r"(?P<ip>\d+\.\d+\.\d+\.\d+)?:(?P<port>\d+)(?:/(?P<protocol>[a-z]+))?"
)

logger = logging.getLogger("uvicorn")

ROOT = "http://127.0.0.1:8080/api"


def log(msg):
    logger.info(f"[{__name__}] {msg}")


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


async def delete_pattern(client, pattern):
    for key in await client.keys(pattern):
        log(f"REDIS delete key: {key}")
        await client.delete(key)


class TraefikRedisApi:
    _instance = None

    def __init__(self, client, http_api):
        self.client = client
        self.http_api = http_api

    @classmethod
    def create(cls, client, http_api):
        cls._instance = cls(client, http_api)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    async def delete_pattern(self, pattern):
        return await delete_pattern(self.client, pattern)

    # Service
    async def create_service(self, name, protocol, type, settings):
        redis_name = name.split("@")[0] if "@" in name else name
        prefix = f"/{protocol}/services/{redis_name}/{type}"
        for k, v in settings_to_kv(settings, prefix):
            await self.client.set(k, v)
        service = await self.http_api.wait(f"/{protocol}/services/{redis_name}@redis")
        service["protocol"] = protocol
        return service

    async def delete_service(self, nodeId):
        protocol, name = validate_node_id(nodeId, "TRAEFIK_SERVICE")
        service = await self.http_api.get_service(protocol, name)
        if service["provider"] != "redis":
            raise ValueError("You can't delete this service")
        redis_name = name.split("@")[0] if "@" in name else name
        await self.delete_pattern(f"/{protocol}/services/{redis_name}/*")
        return await self.http_api.wait_delete(f"/{protocol}/services/{name}")

    # Middleware
    async def delete_middleware(self, nodeId):
        name = validate_node_id(nodeId, "TRAEFIK_MW")[0]
        redis_name = name.split("@")[0] if "@" in name else name
        await self.delete_pattern(f"/http/middlewares/{redis_name}/*")
        return await self.http_api.wait_delete(f"/http/middlewares/{name}")

    async def create_middleware(self, name, type, settings):
        redis_name = name.split("@")[0] if "@" in name else name
        prefix = f"/http/middlewares/{redis_name}/{type}"
        for k, v in settings_to_kv(settings, prefix):
            await self.client.set(k, v)
        return await self.http_api.wait(f"/http/middlewares/{redis_name}@redis")

    async def update_middleware(self, nodeId, type_name, patch):
        (name,) = validate_node_id(nodeId, "TRAEFIK_MW")
        middleware = await self.http_api.get_middleware(name)
        if middleware["provider"] != "redis":
            raise ValueError("You can't edit this middleware")

        root = f"/http/middlewares/{middleware['name'].split('@')[0]}/{type_name}"

        for key, option in patch.items():
            await self.delete_pattern(f"{root}/{key}/*")
            for key, value in settings_to_kv({key: option}):
                await self.client.set(root + key, value)
        await asyncio.sleep(1)
        with no_cache():
            return await self.http_api.get_middleware(name)

    # Router
    async def create_router(self, protocol, settings):
        name = settings.pop("name")
        redis_name = name.split("@")[0] if "@" in name else name
        prefix = f"/{protocol}/routers/{redis_name}"
        for k, v in settings_to_kv(settings, prefix):
            await self.client.set(k, v)

        with no_cache():
            router = await self.http_api.wait(f"/{protocol}/routers/{redis_name}@redis")
            router["protocol"] = protocol
            return router

    async def delete_router(self, nodeId):
        protocol, name = validate_node_id(nodeId, "TRAEFIK_ROUTER")
        router = await self.http_api.get_router(protocol, name)
        if router["provider"] != "redis":
            raise ValueError("You can't delete this router")

        redis_name = name.split("@")[0]
        await self.delete_pattern(f"/{protocol}/routers/{redis_name}/*")

        with no_cache():
            return await self.http_api.wait_delete(f"/{protocol}/routers/{name}")

    async def update_router(self, nodeId, patch):
        protocol, name = validate_node_id(nodeId, "TRAEFIK_ROUTER")
        router = await self.http_api.get_router(protocol, name)
        if router["provider"] != "redis":
            raise ValueError("You can't edit this router")

        root = f"/{router['protocol']}/routers/{router['name'].split('@')[0]}"

        for key, option in patch.items():
            await self.delete_pattern(f"{root}/{key}/*")
            for key, value in settings_to_kv({key: option}):
                await self.client.set(root + key, value)
        await asyncio.sleep(1)
        with no_cache():
            return await self.http_api.get_router(protocol, name)


class TraefikHTTPApi:
    def __init__(self, root, session):
        self.root = root
        self.session = session
        return

    @classmethod
    def create(cls, root, session):
        cls._instance = cls(root, session)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    @cacheMethodForQuery
    async def get(self, path):
        log(f"API GET {path}")
        full_path = f"{self.root.rstrip('/')}/{path.lstrip('/')}"
        async with self.session.get(full_path) as response:
            return await response.json()

    # Do request until it succede
    # if it fail wait more and more .1 -> 1
    async def wait(self, path):
        max_try = 10
        while max_try := max_try - 1:
            try:
                with no_cache():
                    return await self.get(path)
            except:
                await asyncio.sleep(0.1 * (10 - max_try))

    # Do request until it fail
    # if it succede wait more and more .1 -> 1
    async def wait_delete(self, path):
        max_try = 10
        try:
            while max_try := max_try - 1:
                with no_cache():
                    await self.get(path)
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
            yield TraefikHTTPApi.create(root, session)
    finally:
        pass
