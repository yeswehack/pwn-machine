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
from .auth import login, register, auth_middleware
from .api.traefik import new_traefik_http_client, TraefikRedisApi


class TraefikAPIMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        async with new_traefik_http_client("http://127.0.0.1:8080/api") as client:
            request.state.traefik_http = client
            request.state.traefik_redis = TraefikRedisApi(redis_client, "traefik")
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
    ariadne.snake_case_fallback_resolvers,
)


api_routes = [
    Route("/login", login, methods=["POST"]),
    Route("/register", register, methods=["POST"]),
    Mount("/", GraphQL(schema, middleware=[auth_middleware])),
]

app = Starlette(
    routes=[
        Mount("/api", routes=api_routes),
        Mount("/", StaticFiles(directory="static", html=True)),
    ],
    middleware=[Middleware(TraefikAPIMiddleware)],
)
