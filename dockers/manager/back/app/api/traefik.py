import asyncio
import json
import logging
import re
from contextlib import asynccontextmanager, contextmanager

import aiohttp

from app.utils import base64_decode, validate_node_id
from app.utils.cached import cacheMethodForQuery, no_cache
from app.exception import PMException

entrypoint_re = re.compile(
    r"(?P<ip>\d+\.\d+\.\d+\.\d+)?:(?P<port>\d+)(?:/(?P<protocol>[a-z]+))?"
)

ROOT = "http://127.0.0.1:8080/api"


def settings_to_kv(settings, prefix=""):
    for k, v in settings.items():
        if v == None:
            continue
        if isinstance(v, dict):
            yield from settings_to_kv(v, f"{prefix}/{k}")
        elif isinstance(v, list):
            yield from settings_to_kv(dict(enumerate(v)), f"{prefix}/{k}")
        elif isinstance(v, bool):
            yield f"{prefix}/{k.lower()}", str(v).lower()
        else:
            yield f"{prefix}/{k.lower()}", v


async def create_from_object(client, obj, prefix=""):
    async with client.pipeline(transaction=True) as pipe:
        for k, v in settings_to_kv(obj, prefix):
            pipe = pipe.set(k, v)
        await pipe.execute()


async def delete_pattern(client, pattern):
    async with client.pipeline(transaction=True) as pipe:
        for key in await client.keys(pattern):
            pipe = pipe.delete(key)
        await pipe.execute()


class TraefikRedisApi:
    _instance = None

    def __init__(self, root, client, http_api):
        self.root = root
        self.client = client
        self.http_api = http_api

    @classmethod
    def create(cls, root, client, http_api):
        cls._instance = cls(root, client, http_api)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    async def delete_pattern(self, pattern):
        return await delete_pattern(self.client, pattern)

    async def create_from_object(self, settings, prefix=""):
        return await create_from_object(self.client, settings, prefix)

    # Service
    async def create_service(self, name, protocol, type, settings):
        redis_name = name.split("@")[0] if "@" in name else name
        prefix = f"{self.root}/{protocol}/services/{redis_name}/{type}"
        await self.create_from_object(settings, prefix)
        await asyncio.sleep(1)

    async def delete_service(self, nodeId):
        protocol, name = validate_node_id(nodeId, "TRAEFIK_SERVICE")
        service = await self.http_api.get_service(protocol, name)
        if service["provider"] != "redis":
            raise PMException("You can't delete this service")
        redis_name = name.split("@")[0] if "@" in name else name
        await self.delete_pattern(f"{self.root}/{protocol}/services/{redis_name}/*")
        await asyncio.sleep(1)

    # Middleware
    async def delete_middleware(self, nodeId):
        (name,) = validate_node_id(nodeId, "TRAEFIK_MW")
        middleware = await self.http_api.get_middleware(name)
        if middleware["provider"] != "redis":
            raise PMException("You can't delete this middleware")
        redis_name = name.split("@")[0] if "@" in name else name
        await self.delete_pattern(f"{self.root}/http/middlewares/{redis_name}/*")
        await asyncio.sleep(1)

    async def create_middleware(self, name, type, settings):
        redis_name = name.split("@")[0] if "@" in name else name
        prefix = f"{self.root}/http/middlewares/{redis_name}/{type}"
        await self.create_from_object(settings, prefix)
        await asyncio.sleep(1)

    async def update_middleware(self, nodeId, type_name, patch):
        (name,) = validate_node_id(nodeId, "TRAEFIK_MW")
        middleware = await self.http_api.get_middleware(name)
        if middleware["provider"] != "redis":
            raise PMException("You can't edit this middleware")

        prefix = f"{self.root}/http/middlewares/{middleware['name'].split('@')[0]}/{type_name}"

        for key, option in patch.items():
            await self.delete_pattern(f"{prefix}/{key}/*")
            await self.create_from_object({key: option}, prefix)
        await asyncio.sleep(1)

    # Router
    async def create_router(self, protocol, settings):
        name = settings.pop("name")
        redis_name = name.split("@")[0] if "@" in name else name
        prefix = f"{self.root}/{protocol}/routers/{redis_name}"

        await self.create_from_object(settings, prefix)

        await asyncio.sleep(1)

    async def delete_router(self, nodeId):
        protocol, name = validate_node_id(nodeId, "TRAEFIK_ROUTER")
        router = await self.http_api.get_router(protocol, name)
        if router["provider"] != "redis":
            raise PMException("You can't delete this router")

        redis_name = name.split("@")[0]
        await self.delete_pattern(f"{self.root}/{protocol}/routers/{redis_name}/*")

        await asyncio.sleep(1)

    async def update_router(self, nodeId, patch):
        protocol, name = validate_node_id(nodeId, "TRAEFIK_ROUTER")
        router = await self.http_api.get_router(protocol, name)
        if router["provider"] != "redis":
            raise PMException("You can't edit this router")

        prefix = (
            f"{self.root}/{router['protocol']}/routers/{router['name'].split('@')[0]}"
        )

        for key, option in patch.items():
            await self.delete_pattern(f"{prefix}/{key}/*")
            await self.create_from_object({key: option}, prefix)
        await asyncio.sleep(1)


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
        full_path = f"{self.root.rstrip('/')}/{path.lstrip('/')}"
        async with self.session.get(full_path) as response:
            return await response.json()

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
        try:
            service = await self.get(f"/{protocol}/services/{name}")
            service["protocol"] = protocol
            return service
        except:
            return {
                "protocol": "invalid",
                "type": "invalid",
                "enabled": False,
                "usedBy": [],
                "name": name,
            }

    async def get_services(self, protocols=("http", "tcp", "udp")):
        all_services = []
        for proto in protocols:
            services = await self.get(f"/{proto}/services")
            for service in services:
                service["protocol"] = proto
            all_services += services

        return all_services
