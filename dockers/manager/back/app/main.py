import redis
import ariadne
from .utils.registration import (
    registered_mutations,
    registered_queries,
    registered_types,
)
from starlette.applications import Starlette
from starlette.routing import Router, Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from ariadne.asgi import GraphQL

from .redis import client as redis_client
from . import traefik
from .auth import auth_middleware
from .api.traefik import new_traefik_http_client, TraefikRedisApi


class TraefikAPIMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        async with new_traefik_http_client("http://127.0.0.1:8080/api") as client:
            request.state.traefik_http = client
            request.state.traefik_redis = TraefikRedisApi(redis_client, "traefik", client)
            response = await call_next(request)
        return response


type_defs = ariadne.load_schema_from_path("./schema")

query = ariadne.QueryType()
mutation = ariadne.MutationType()


for name, resolver in registered_queries.items():
    query.field(name)(resolver)

for name, resolver in registered_mutations.items():
    mutation.field(name)(resolver)

schema = ariadne.make_executable_schema(
    type_defs,
    query,
    mutation,
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
        Mount("/", StaticFilesFallback(directory="static", html=True)),
    ],
    middleware=[Middleware(TraefikAPIMiddleware)],
)
