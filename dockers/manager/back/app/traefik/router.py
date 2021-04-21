
from ..utils.registration import registerQuery, registerMutation, createType
from . import with_traefik_http, with_traefik_redis

TraefikRouter = createType("TraefikRouter")

async def get_routers(client, *protocols):
    all_routers = []
    for proto in protocols:
        routers = await client.get(f"/{proto}/routers")
        for router in routers:
            router["protocol"] = proto
        all_routers += routers

    return all_routers


@registerQuery("traefikRouters")
@with_traefik_http
async def resolve_TraefikRouters(*_, traefik_http):
    return await get_routers(traefik_http, "http", "tcp", "udp")


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
@with_traefik_http
async def resolve_traefikrouter_name(router, *_, traefik_http):
    return await traefik_http.get(f"/{router['protocol']}/services/{router['service']}")


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
            traefik_redis.set(f"{protocol}/routers/{name}/middlewares/{idx}", entrypoint)

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