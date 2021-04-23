from ..utils import registerQuery, createType, base64_encode
from . import with_traefik_http
TraefikService = createType("TraefikService")
TraefikServiceLoadBalancer = createType("TraefikServiceLoadBalancer")
TraefikServiceLoadBalancerServer = createType("TraefikServiceLoadBalancerServer")



@registerQuery("traefikServices")
@with_traefik_http
async def resolve_TraefikServices(*_, traefik_http):
    return await traefik_http.get_services()


@TraefikService.field("enabled")
def resolve_traefik_enabled(service, *_):
    return service["status"] == "enabled"


@TraefikService.field("nodeId")
async def resolve_nodeid(service, *_):
    return base64_encode(["service", service["protocol"], service["name"]], json=True)


@TraefikService.field("loadBalancer")
def resolve_loadBalancer(service, *_):
    if "loadBalancer" in service:
        return service["loadBalancer"]
    return None


@TraefikService.field("usedBy")
@with_traefik_http
async def resolve_usedBy(service, *_, traefik_http):
    if "usedBy" not in service:
        return []
    routers = []
    for router_name in service["usedBy"]:
        routers.append(await traefik_http.get_router(service['protocol'], router_name))
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