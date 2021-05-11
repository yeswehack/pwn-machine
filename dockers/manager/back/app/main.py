import ariadne
from .utils.registration import (
    registered_mutations,
    registered_queries,
    registered_types,
    registered_subscriptions,
)
from starlette.applications import Starlette
from starlette.websockets import WebSocket
from starlette.requests import HTTPConnection
from starlette.routing import Router, Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from ariadne.asgi import GraphQL

from .redis import client as redis_client
from . import docker
from . import traefik
from . import dns
from .auth import auth_middleware
from .api.traefik import new_traefik_http_client, TraefikRedisApi
from .api.powerdns import new_powerdns_http_client, PowerdnsRedisApi


class TraefikApiMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        async with new_traefik_http_client("http://127.0.0.1:8080/api") as client:
            request.state.traefik_http = client
            request.state.traefik_redis = TraefikRedisApi(
                redis_client, "traefik", client
            )
            response = await call_next(request)
        return response


class PowerDNSApiMiddleware(BaseHTTPMiddleware):
    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            ws = WebSocket(scope=scope, receive=receive, send=send)
            ws.state.dns_redis = PowerdnsRedisApi(redis_client, "dns")
        return await super().__call__(scope, receive, send)

    async def dispatch(self, request, call_next):
        async with new_powerdns_http_client("http://127.0.0.1:8081", "test") as client:
            request.state.dns_http = client
            request.state.dns_redis = PowerdnsRedisApi(redis_client, "dns")
            response = await call_next(request)
        return response


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


app = Starlette(
    routes=[
        Route("/api", GraphQL(schema, middleware=[auth_middleware])),
        WebSocketRoute("/api", GraphQL(schema=schema)),
        # Mount("/", StaticFilesFallback(directory="static", html=True)),
    ],
    middleware=[Middleware(TraefikApiMiddleware), Middleware(PowerDNSApiMiddleware)],
)
