import redis
import ariadne
from .utils.registration import (
    registered_mutations,
    registered_queries,
    registered_types,
)
from starlette.routing import Router, Mount
from starlette.staticfiles import StaticFiles
from ariadne.asgi import GraphQL

from . import traefik
# from . import auth


type_defs = ariadne.load_schema_from_path("./schema")

query = ariadne.QueryType()
mutation = ariadne.MutationType()


for name, resolver in registered_queries.items():
    query.field(name)(resolver)

for name, resolver in registered_mutations.items():
    query.field(name)(resolver)

schema = ariadne.make_executable_schema(
    type_defs,
    query,
    mutation,
    *registered_types,
    ariadne.snake_case_fallback_resolvers,
)


app = Router(
    routes=[Mount("/api", GraphQL(schema))],
    default=StaticFiles(directory="static", html=True),
)
