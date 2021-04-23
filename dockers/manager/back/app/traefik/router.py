from ..utils import (
    registerQuery,
    registerMutation,
    createType,
    base64_encode,
    base64_decode,
)
from . import with_traefik_http, with_traefik_redis

TraefikRouter = createType("TraefikRouter")


@registerQuery("traefikRouters")
@with_traefik_http
async def resolve_TraefikRouters(*_, traefik_http):
    return await traefik_http.get_routers()


@TraefikRouter.field("enabled")
def resolve_traefik_enabled(obj, *_):
    return obj["status"] == "enabled"


@TraefikRouter.field("entryPoints")
@with_traefik_http
async def resolve_traefik_enabled(router, *_, traefik_http):
    if "entryPoints" not in router:
        return []
    return [
        entrypoint
        for entrypoint in await traefik_http.get_entrypoints()
        if entrypoint["name"] in router["entryPoints"]
    ]


@TraefikRouter.field("priority")
def resolve_traefikrouter_name(router, *_):
    if "priority" in router:
        return router["priority"]
    if "rule" in router:
        return len(router["rule"])
    return 0


@TraefikRouter.field("middlewares")
@with_traefik_http
async def middlewares(router, *_, traefik_http):
    if "middlewares" not in router:
        return []
    return [
        middleware
        for middleware in await traefik_http.get_middlewares()
        if middleware["name"] in router["middlewares"]
    ]


@TraefikRouter.field("nodeId")
async def resolve_nodeid(router, *_):
    return base64_encode(["router", router["protocol"], router["name"]], json=True)


@TraefikRouter.field("service")
@with_traefik_http
async def resolve_traefikrouter_name(router, *_, traefik_http):
    return await traefik_http.get_service(router["protocol"], router["service"])


@registerMutation("traefikCreateRouter")
@with_traefik_http
@with_traefik_redis
async def mutation_create_router(*_, traefik_redis, traefik_http, input):
    protocol = input["protocol"]
    name = input["name"]
    print(input)
    if "rule" in input:
        traefik_redis.set(f"{protocol}/routers/{name}/rule", input["rule"])
    traefik_redis.set(f"{protocol}/routers/{name}/service", input["service"])

    for idx, entrypoint in enumerate(input["entryPoints"]):
        traefik_redis.set(f"{protocol}/routers/{name}/entrypoints/{idx}", entrypoint)

    if "middlewares" in input:
        for idx, entrypoint in enumerate(input["middlewares"]):
            traefik_redis.set(
                f"{protocol}/routers/{name}/middlewares/{idx}", entrypoint
            )

    router = await traefik_http.wait(f"/{protocol}/routers/{name}@redis")
    router["protocol"] = protocol
    return router


@registerMutation("traefikDeleteRouter")
@with_traefik_http
@with_traefik_redis
async def mutation_delete_router(*_, traefik_redis, traefik_http, input):
    protocol = input["protocol"]
    name = input["name"]
    redis_name = name.split("@")[0] if "@" in name else name
    traefik_redis.delete_pattern(f"/{protocol}/routers/{redis_name}/*")
    ok = await traefik_http.wait_delete(f"/{protocol}/routers/{name}")
    return {"ok": ok}