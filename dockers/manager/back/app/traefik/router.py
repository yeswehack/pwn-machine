from .api import get_from_api, wait_from_api, wait_delete_from_api
from ..utils.registration import registerQuery, registerMutation, createType
from . import client as redis_client

TraefikRouter = createType("TraefikRouter")


@registerQuery("traefikRouters")
async def resolve_TraefikRouters(*_):
    all_routers = []
    for proto in ["http", "tcp", "udp"]:
        routers = await get_from_api(f"/{proto}/routers")
        for router in routers:
            router["protocol"] = proto
        all_routers += routers

    return all_routers


@TraefikRouter.field("enabled")
def resolve_traefik_enabled(obj, *_):
    return obj["status"] == "enabled"


@TraefikRouter.field("entryPoints")
def resolve_traefik_enabled(obj, *_):
    if "entryPoints" in obj:
        return obj["entryPoints"]
    return []


@TraefikRouter.field("priority")
def resolve_traefikrouter_name(router, *_):
    if "priority" in router:
        return router["priority"]
    if "rule" in router:
        return len(router["rule"])
    return 0


@TraefikRouter.field("service")
async def resolve_traefikrouter_name(router, *_):
    return await get_from_api(f"/{router['protocol']}/services/{router['service']}")


@registerMutation("traefikCreateRouter")
async def mutation_create_router(*_, input):
    protocol = input["protocol"]
    name = input["name"]
    print(input)
    if "rule" in input:
        redis_client.set(f"{protocol}/routers/{name}/rule", input["rule"])
    redis_client.set(f"{protocol}/routers/{name}/service", input["service"])


    for idx, entrypoint in enumerate(input["entryPoints"]):
        redis_client.set(f"{protocol}/routers/{name}/entrypoints/{idx}", entrypoint)

    if "middlewares" in input:
        for idx, entrypoint in enumerate(input["middlewares"]):
            redis_client.set(f"{protocol}/routers/{name}/middlewares/{idx}", entrypoint)

    router = await wait_from_api(f"/{protocol}/routers/{name}@redis")
    router["protocol"] = protocol
    return router


@registerMutation("traefikDeleteRouter")
async def mutation_delete_router(*_, input):
    protocol = input["protocol"]
    name = input["name"]
    redis_name = name.split("@")[0] if "@" in name else name
    redis_client.delete_pattern(f"/{protocol}/routers/{redis_name}/*")
    ok = await wait_delete_from_api(f"/{protocol}/routers/{name}")
    return {"ok": ok}