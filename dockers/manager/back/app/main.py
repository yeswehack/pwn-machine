from collections import defaultdict
from functools import lru_cache

import aiohttp
import aioredis
import ariadne
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import HTTPConnection
from starlette.routing import Mount, Route, Router, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from starlette_context import context
from starlette_context.middleware import RawContextMiddleware

from . import dns, docker, traefik
from .api.NamespacedRedis import NamespacedRedis
from .api.powerdns import PowerdnsHTTPApi, PowerdnsRedisApi
from .api.shell import handle_shell
from .api.traefik import TraefikHTTPApi, TraefikRedisApi
from .auth import auth_middleware
from .redis import client as redis_client
from .utils.registration import (registered_mutations, registered_queries,
                                 registered_subscriptions, registered_types)


class PowerDNSApiMiddleware(BaseHTTPMiddleware):
    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            ws = WebSocket(scope=scope, receive=receive, send=send)
            ws.state.dns_redis = PowerdnsRedisApi(redis_client, "dns")
        return await super().__call__(scope, receive, send)

    async def dispatch(self, request, call_next):
        get_request()
        async with new_powerdns_http_client("http://127.0.0.1:8081", "test") as client:
            request.state.dns_http = client
            request.state.dns_redis = PowerdnsRedisApi(redis_client, "dns")
            response = await call_next(request)
        return response


class RequestCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        context["cache"] = dict()
        context["cache_disabled"] = False
        return await call_next(request)


type_defs = ariadne.load_schema_from_path("./schema")

query = ariadne.QueryType()
mutation = ariadne.MutationType()
subscription = ariadne.SubscriptionType()


for name, resolver in registered_queries.items():
    query.set_field(name, resolver)

for name, resolver in registered_mutations.items():
    mutation.set_field(name, resolver)

for name, resolver in registered_subscriptions.items():
    subscription.set_source(name, resolver)
    subscription.set_field(name, lambda f, *_, **__: f if f else None)

schema = ariadne.make_executable_schema(
    type_defs,
    query,
    mutation,
    subscription,
    *registered_types,
    ariadne.fallback_resolvers,
)


class StaticFilesFallback(StaticFiles):
    async def __call__(self, scope, receive, send):
        response = await self.get_response(self.get_path(scope), scope)
        if response.status_code == 404:
            response = await self.get_response("index.html", scope)
        await response(scope, receive, send)


sessions = {}


async def on_startup():
    redis_client = aioredis.from_url("redis://localhost", decode_responses=True)

    ## Traefik
    sessions["traefik"] = aiohttp.ClientSession()
    traefik_http = TraefikHTTPApi.create("http://127.0.0.1:8080/api", sessions["traefik"])
    ns_traefik_redis = NamespacedRedis("traefik", redis_client)
    TraefikRedisApi.create(ns_traefik_redis, traefik_http)

    ## PowerDNS
    sessions["powerdns"] = aiohttp.ClientSession(headers={"X-Api-Key": "test"})
    PowerdnsHTTPApi.create("http://127.0.0.1:8081", sessions["powerdns"])


async def on_shutdown():
    await sessions["traefik"].close()
    await sessions["powerdns"].close()


app = Starlette(
    routes=[
        Route("/api", GraphQL(schema, middleware=[auth_middleware])),
        WebSocketRoute("/api", GraphQL(schema=schema)),
        WebSocketRoute("/shell/{uuid:str}", handle_shell),
        # Mount("/", StaticFilesFallback(directory="static", html=True)),
    ],
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    middleware=[Middleware(RawContextMiddleware), Middleware(RequestCacheMiddleware)],
)
