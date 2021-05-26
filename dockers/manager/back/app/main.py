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

from app.api import NamespacedRedis, PowerdnsHTTPApi, TraefikHTTPApi, TraefikRedisApi
from app import config
from . import dns, docker, traefik
from .api.shell import handle_shell
from app.api import es
from .auth import auth_middleware
from .redis import client as redis_client
from .utils.registration import (
    registered_mutations,
    registered_queries,
    registered_subscriptions,
    registered_types,
)


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
    redis_client = aioredis.from_url(config.PM_REDIS_HOST, decode_responses=True)

    ## Traefik
    sessions["traefik"] = aiohttp.ClientSession()
    traefik_http = TraefikHTTPApi.create(
        config.PM_TRAEFIK_HTTP_API, sessions["traefik"]
    )
    ns_traefik_redis = NamespacedRedis(config.PM_TRAEFIK_REDIS_ROOT, redis_client)
    TraefikRedisApi.create(ns_traefik_redis, traefik_http)

    ## PowerDNS
    sessions["powerdns"] = aiohttp.ClientSession(
        headers={"X-Api-Key": config.PM_POWERDNS_HTTP_API_KEY}
    )
    PowerdnsHTTPApi.create(config.PM_POWERDNS_HTTP_API, sessions["powerdns"])




async def on_shutdown():
    await sessions["traefik"].close()
    await sessions["powerdns"].close()


app = Starlette(
    routes=[
        WebSocketRoute("/ws/shell/{uuid:str}", handle_shell),
        Route("/api", GraphQL(schema, middleware=[auth_middleware])),
        WebSocketRoute("/api", GraphQL(schema=schema)),
        Mount("/", StaticFilesFallback(directory="static", html=True)),
    ],
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    middleware=[Middleware(RawContextMiddleware), Middleware(RequestCacheMiddleware)],
)
