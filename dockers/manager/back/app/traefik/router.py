from app.utils import (
    registerQuery,
    registerMutation,
    createType,
    createInterface,
    create_node_id,
)
from app.api import (
    get_traefik_http_api as traefik_http,
    get_traefik_redis_api as traefik_redis,
)

TraefikRouter = createInterface("TraefikRouter")


@TraefikRouter.type_resolver
def resolve_router_type(router, *_):
    mapping = {
        "http": "TraefikHTTPRouter",
        "tcp": "TraefikTCPRouter",
        "udp": "TraefikUDPRouter",
    }
    return mapping[router["protocol"]]


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
    entrypoints = {e['name']: e for e in await traefik_http().get_entrypoints()}
    results = []
    for name in router["entryPoints"]:
        results.append(entrypoints[name])
    return results

TraefikHTTPRouter = createType("TraefikHTTPRouter")


@TraefikHTTPRouter.field("priority")
def resolve_traefikrouter_name(router, *_):
    if "priority" in router:
        return router["priority"]
    if "rule" in router:
        return len(router["rule"])
    return 0


@TraefikHTTPRouter.field("middlewares")
async def middlewares(router, *_):
    if "middlewares" not in router:
        return []
    middlewares = {m["name"]: m for m in await traefik_http().get_middlewares()}
    results = []
    for name in router["middlewares"]:
        if name in middlewares:
            results.append(middlewares[name])
        else:
            results.append({"name":name, "type": "invalid"})
    return results


@TraefikRouter.field("nodeId")
async def resolve_nodeid(router, *_):
    return create_node_id("TRAEFIK_ROUTER", router["protocol"], router["name"])


@TraefikRouter.field("service")
async def resolve_traefikrouter_name(router, *_):
    if "service" in router:
        return await traefik_http().get_service(router["protocol"], router["service"])
    return None


@registerMutation("updateTraefikHTTPRouter")
@registerMutation("updateTraefikTCPRouter")
@registerMutation("updateTraefikUDPRouter")
async def mutation_update_http_router(*_, id, patch):
    return await traefik_redis().update_router(id, patch)


@registerMutation("createTraefikHTTPRouter")
async def mutation_create_router(*_, input):
    return await traefik_redis().create_router("http", input)


@registerMutation("createTraefikTCPRouter")
async def mutation_create_router(*_, input):
    return await traefik_redis().create_router("tcp", input)


@registerMutation("createTraefikUDPRouter")
async def mutation_create_router(*_, input):
    return await traefik_redis().create_router("udp", input)


@registerMutation("deleteTraefikRouter")
async def mutation_delete_router(*_, id):
    return await traefik_redis().delete_router(id)
