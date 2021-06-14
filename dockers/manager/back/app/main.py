from collections import defaultdict
from functools import lru_cache

import aiohttp
import aioredis
import ariadne
import graphql
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.routing import Mount, Route, Router, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette_context import context
from starlette_context.middleware import RawContextMiddleware

from app import config

from app.api import PowerdnsHTTPApi, TraefikHTTPApi, TraefikRedisApi
from app.docker.files import download_file, upload_file
from app.auth import auth_middleware, db
from app.docker.shell import handle_shell
from app.utils.registration import (
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


MANAGER_ROUTER_INSTALLED_KEY = "pm/manager/installed"

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


async def init_traefik(redis_client):

    sessions["traefik"] = aiohttp.ClientSession()
    traefik_http = TraefikHTTPApi.create(
        config.PM_TRAEFIK_HTTP_API, sessions["traefik"]
    )
    traefik_redis = TraefikRedisApi.create(
        config.PM_TRAEFIK_REDIS_ROOT, redis_client, traefik_http
    )
    is_installed = await redis_client.get(MANAGER_ROUTER_INSTALLED_KEY)
    if not is_installed:
        await traefik_redis.create_service(
            "pm-manager-service",
            "http",
            "loadBalancer",
            {
                "servers": [{"url": "http://manager:5000/"}],
            },
        )
        await traefik_redis.create_router(
            "http",
            {
                "entrypoints": ["http"],
                "name": "pm-manager-router",
                "service": "pm-manager-service@redis",
                "rule": "PathPrefix(`/`)",
            },
        )
        await redis_client.set(MANAGER_ROUTER_INSTALLED_KEY, "True")


async def init_powerdns():
    sessions["powerdns"] = aiohttp.ClientSession(
        headers={"X-Api-Key": config.PM_POWERDNS_HTTP_API_KEY}
    )
    PowerdnsHTTPApi.create(config.PM_POWERDNS_HTTP_API, sessions["powerdns"])


async def on_startup():
    redis_client = aioredis.from_url(config.PM_REDIS_HOST, decode_responses=True)
    ## Auth
    await db.init(redis_client)

    ## Traefik
    await init_traefik(redis_client)
    ## PowerDNS
    await init_powerdns()


async def on_shutdown():
    await sessions["traefik"].close()
    await sessions["powerdns"].close()


def is_basic_mutation(type):
    for interface in getattr(type, "interfaces", []):
        if is_basic_mutation(interface):
            return True
    return type.name == "IMutationResponse"


def is_non_null_basic_mutation(type):
    if isinstance(type, graphql.type.definition.GraphQLNonNull):
        return is_basic_mutation(type.of_type)
    return False


def validate_schema(schema):

    for name, mutation in schema.mutation_type.fields.items():
        if name == "_unused":
            continue
        if not is_non_null_basic_mutation(mutation.type):
            raise ValueError(f"{name} Must implement IMutationResponse!")


validate_schema(schema)
graphql_route = GraphQL(schema, middleware=[auth_middleware])
app = Starlette(
    routes=[
        WebSocketRoute("/ws/shell/{uuid:str}", handle_shell),
        Route("/file/download", download_file),
        Route("/file/upload", upload_file, methods=["POST"]),
        Route("/api", graphql_route),
        Route("/api/", graphql_route),
        WebSocketRoute("/api", GraphQL(schema=schema)),
        Mount("/", StaticFilesFallback(directory="static", html=True)),
    ],
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    middleware=[
        Middleware(RawContextMiddleware),
        Middleware(RequestCacheMiddleware),
        Middleware(GZipMiddleware, minimum_size=1000),
    ],
)
