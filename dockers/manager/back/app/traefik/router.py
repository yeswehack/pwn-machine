from .api import get_from_api
from ..utils.registration import registerQuery, createType

TraefikRouter = createType("TraefikRouter")


@registerQuery("traefikRouters")
def resolve_TraefikRouters(*_):
    all_routers = []
    for proto in ["http", "tcp", "udp"]:
        routers = get_from_api(f"/{proto}/routers")
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
    return len(router["rule"])


@TraefikRouter.field("service")
def resolve_traefikrouter_name(router, *_):
    return get_from_api(f"/{router['protocol']}/services/{router['service']}")