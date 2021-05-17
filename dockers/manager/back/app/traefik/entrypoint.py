from ..utils import createType, registerQuery, create_node_id
from ..api import get_traefik_http_api as traefik_http


TraefikEntrypoint = createType("TraefikEntrypoint")


@registerQuery("traefikEntrypoints")
async def resolve_TraefikEntrypoints(*_):
    return await traefik_http().get_entrypoints()


@TraefikEntrypoint.field("nodeId")
async def resolve_nodeid(entrypoint, *_):
    return create_node_id("TRAEFIK_EP", entrypoint["name"])


@TraefikEntrypoint.field("usedBy")
async def resolved_usedby(entrypoint, *_):
    if entrypoint["protocol"] == "udp":
        protocols = ["udp"]
    else:
        protocols = ["http", "tcp"]

    routers = await traefik_http().get_routers(protocols)
    return [router for router in routers if entrypoint["name"] in router["entryPoints"]]
