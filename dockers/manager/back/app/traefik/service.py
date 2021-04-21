from ..utils.registration import registerQuery, createType
from .api import get_from_api

TraefikService = createType("TraefikService")
TraefikServiceLoadBalancer = createType("TraefikServiceLoadBalancer")
TraefikServiceLoadBalancerServer = createType("TraefikServiceLoadBalancerServer")


@registerQuery("traefikServices")
async def resolve_TraefikServices(*_):
    all_routers = []
    for proto in ["http", "tcp", "udp"]:
        routers = await get_from_api(f"/{proto}/services")
        for router in routers:
            router["protocol"] = proto
        all_routers += routers

    return all_routers


@TraefikService.field("enabled")
def resolve_traefik_enabled(service, *_):
    return service["status"] == "enabled"


@TraefikService.field("loadBalancer")
def resolve_loadBalancer(service, *_):
    if "loadBalancer" in service:
        return service["loadBalancer"]
    return None


@TraefikService.field("usedBy")
async def resolve_usedBy(service, *_):
    if "usedBy" not in service:
        return []
    routers = []
    for router_name in service["usedBy"]:
        router = await get_from_api(f"/{service['protocol']}/routers/{router_name}")
        routers.append(router)
    return routers


@TraefikService.field("serverStatus")
def resolve_server_status(service, *_):
    if "serverStatus" not in service:
        return []
    status = []
    for name, value in service["serverStatus"].items():
        status.append({"url": name, "status": value})
    return status


@TraefikServiceLoadBalancer.field("healthCheck")
def healthCheck(loadBalancer, *_):
    if "healthCheck" in loadBalancer:
        return loadBalancer["healthCheck"]
    return None


@TraefikServiceLoadBalancer.field("servers")
def healthCheck(loadBalancer, *_):
    if "servers" in loadBalancer:
        return loadBalancer["servers"]
    return []


@TraefikServiceLoadBalancerServer.field("url")
def resolve_server_url(server, *_):
    if "url" in server:
        return server["url"]
    if "address" in server:
        return server["address"]