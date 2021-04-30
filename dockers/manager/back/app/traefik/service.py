from ..utils import (
    registerQuery,
    registerMutation,
    create_kv_resolver,
    createType,
    base64_encode,
    createInterface,
)
from . import with_traefik_http, with_traefik_redis


TraefikService = createInterface("TraefikService")


@TraefikService.type_resolver
def resolve_service_type(service, *_):
    mapping = {
        "http": {
            "loadbalancer": "TraefikHTTPServiceLoadBalancer",
            "mirroring": "TraefikHTTPServiceMirroring",
            "weighted": "TraefikHTTPServiceWeighted",
        },
        "tcp": {
            "loadbalancer": "TraefikTCPServiceLoadBalancer",
            "weighted": "TraefikTCPServiceWeighted",
        },
        "udp": {
            "loadbalancer": "TraefikUDPServiceLoadBalancer",
            "weighted": "TraefikUDPServiceWeighted",
        },
    }
    try:
        return mapping[service["protocol"]][service["type"]]
    except:
        return "TraefikHTTPServiceInternal"


@registerQuery("traefikServices")
@with_traefik_http
async def resolve_TraefikServices(*_, traefik_http, protocols=None):
    print(protocols)
    if (protocols):
        return await traefik_http.get_services(protocols)
    return await traefik_http.get_services()


@TraefikService.field("enabled")
def resolve_traefik_enabled(service, *_):
    return service["status"] == "enabled"


@TraefikService.field("nodeId")
async def resolve_nodeid(service, *_):
    return base64_encode(["service", service["protocol"], service["name"]], json=True)


@TraefikService.field("usedBy")
@with_traefik_http
async def resolve_usedBy(service, *_, traefik_http):
    if "usedBy" not in service:
        return []
    return await traefik_http.get_routers_used_by(service["usedBy"])


@TraefikService.field("type")
async def resolve_type(service, *_):
    type = service.get("type", "internal")
    if type == "loadbalancer":
        return "loadBalancer"
    return type


TraefikServiceLoadBalancerHealthCheck = createType(
    "TraefikServiceLoadBalancerHealthCheck"
)


TraefikServiceLoadBalancerHealthCheck.field("headers")(create_kv_resolver("headers"))


TraefikUDPWeighted = createType("TraefikUDPWeighted")
TraefikWeighted = createType("TraefikWeighted")


@TraefikWeighted.field("services")
@TraefikUDPWeighted.field("services")
def resolve_weighted_services(weighted, *_):
    services = weighted.get("services", [])
    return services


TraefikHTTPLoadBalancer = createType("TraefikHTTPLoadBalancer")


@TraefikHTTPLoadBalancer.field("servers")
def resolve_loadbalancer_servers(loadbalancer, *_):
    servers = loadbalancer.get("servers", [])
    return servers

@registerMutation("createTraefikHTTPServiceLoadBalancer")
@with_traefik_redis
async def create_http_loadbalancer(*_, traefik_redis, input):
    name = input["name"]
    return await traefik_redis.create_service(name, "http", "loadBalancer", input["loadBalancer"])


@registerMutation("deleteTraefikService")
@with_traefik_redis
async def delete_service(*_, traefik_redis, nodeId):
    return await traefik_redis.delete_service(nodeId)