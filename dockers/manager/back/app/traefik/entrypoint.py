import re
from ..utils.registration import createType, registerQuery
from .router import get_routers
from . import with_traefik_http


TraefikEntrypoint = createType("TraefikEntrypoint")

entrypoint_re = re.compile(
    r"(?P<ip>\d+\.\d+\.\d+\.\d+)?:(?P<port>\d+)(?:/(?P<protocol>[a-z]+))?"
)


@registerQuery("traefikEntrypoints")
@with_traefik_http
async def resolve_TraefikEntrypoints(*_, traefik_http):
    entrypoints = []
    for entrypoint in await traefik_http.get(f"/entrypoints"):
        groups = entrypoint_re.match(entrypoint["address"]).groupdict()
        ip = groups["ip"] or "0.0.0.0"
        port = groups["port"] or 0
        protocol = groups["protocol"] or "tcp"
        address = f"{ip}:{port}/{protocol}"
        entrypoints.append(
            {
                "ip": ip,
                "port": port,
                "protocol": protocol,
                "address": address,
                "name": entrypoint["name"],
            }
        )

    return entrypoints


@TraefikEntrypoint.field("usedBy")
@with_traefik_http
async def resolved_usedby(entrypoint, *_, traefik_http):
    if entrypoint["protocol"] == "udp":
        routers = await get_routers(traefik_http, "udp")
    else:
        routers = await get_routers(traefik_http, "http", "tcp")
    return [router for router in routers if entrypoint["name"] in router["entryPoints"]]
