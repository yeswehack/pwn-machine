from ..utils import registerQuery, registerMutation, createType, create_node_id
from . import with_traefik_redis
from ..api import get_traefik_http_api as traefik_http

TraefikRouter = createType("TraefikRouter")


@registerQuery("traefikRouters")
async def resolve_TraefikRouters(*_):
    return await traefik_http().get_routers()


@TraefikRouter.field("enabled")
def resolve_traefik_enabled(obj, *_):
    return obj["status"] == "enabled"


@TraefikRouter.field("entryPoints")
async def resolve_traefik_enabled(router, *_):
    if "entryPoints" not in router:
        return []
    return [
        entrypoint
        for entrypoint in await traefik_http().get_entrypoints()
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
async def middlewares(router, *_):
    if "middlewares" not in router:
        return []
    return [
        middleware
        for middleware in await traefik_http().get_middlewares()
        if middleware["name"] in router["middlewares"]
    ]


@TraefikRouter.field("nodeId")
async def resolve_nodeid(router, *_):
    return create_node_id("TRAEFIK_ROUTER", router["protocol"], router["name"])


@TraefikRouter.field("service")
async def resolve_traefikrouter_name(router, *_):
    return await traefik_http().get_service(router["protocol"], router["service"])


@registerMutation("traefikCreateRouter")
@with_traefik_redis
async def mutation_create_router(*_, traefik_redis, input):
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

    router = await traefik_http().wait(f"/{protocol}/routers/{name}@redis")
    router["protocol"] = protocol
    return router


@registerMutation("traefikDeleteRouter")
@with_traefik_redis
async def mutation_delete_router(*_, traefik_redis, input):
    protocol = input["protocol"]
    name = input["name"]
    redis_name = name.split("@")[0] if "@" in name else name
    traefik_redis.delete_pattern(f"/{protocol}/routers/{redis_name}/*")
    ok = await traefik_http().wait_delete(f"/{protocol}/routers/{name}")
    return {"ok": ok}
