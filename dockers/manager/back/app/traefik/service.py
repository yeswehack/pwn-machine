from app.utils import (
    registerQuery,
    registerMutation,
    create_kv_resolver,
    createType,
    create_node_id,
    createInterface,
)
from . import with_traefik_redis
from app.api import (
    get_traefik_http_api as traefik_http,
    get_traefik_redis_api as traefik_redis,
)


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
        "invalid": {
            "invalid": "TraefikInvalidService"
        }
    }
    try:
        return mapping[service["protocol"]][service["type"]]
    except:
        return "TraefikHTTPServiceInternal"



@registerQuery("traefikServices")
async def resolve_TraefikServices(*_, protocols=None):
    if protocols:
        return await traefik_http().get_services(protocols)
    return await traefik_http().get_services()


@TraefikService.field("enabled")
def resolve_traefik_enabled(service, *_):
    return service["status"] == "enabled"


@TraefikService.field("nodeId")
async def resolve_nodeid(service, *_):
    return create_node_id("TRAEFIK_SERVICE", service["protocol"], service["name"])


@TraefikService.field("usedBy")
async def resolve_usedBy(service, *_):
    if "usedBy" not in service:
        return []
    return await traefik_http().get_routers_used_by(service["usedBy"])


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


TraefikWeighted = createType("TraefikWeighted")


@TraefikWeighted.field("services")
def resolve_weighted_services(weighted, *_):
    services = weighted.get("services", [])
    return services


TraefikHTTPLoadBalancer = createType("TraefikHTTPLoadBalancer")


@TraefikHTTPLoadBalancer.field("servers")
def resolve_loadbalancer_servers(loadbalancer, *_):
    servers = loadbalancer.get("servers", [])
    return servers


@registerMutation("createTraefikHTTPServiceLoadBalancer")
async def create_http_loadbalancer(*_, input):
    return await traefik_redis().create_service(
        input["name"], "http", "loadBalancer", input["loadBalancer"]
    )


@registerMutation("createTraefikHTTPServiceMirroring")
async def create_http_mirroring(*_, input):
    return await traefik_redis().create_service(
        input["name"], "http", "mirroring", input["mirroring"]
    )


@registerMutation("createTraefikHTTPServiceWeighted")
async def create_http_weighted(*_, input):
    return await traefik_redis().create_service(
        input["name"], "http", "weighted", input["weighted"]
    )


@registerMutation("createTraefikTCPServiceLoadBalancer")
async def create_tcp_loadbalancer(*_, input):
    return await traefik_redis().create_service(
        input["name"], "tcp", "loadBalancer", input["loadBalancer"]
    )


@registerMutation("createTraefikTCPServiceWeighted")
async def create_tcp_weighted(*_, input):
    return await traefik_redis().create_service(
        input["name"], "tcp", "weighted", input["weighted"]
    )


@registerMutation("createTraefikUDPServiceLoadBalancer")
async def create_udp_loadbalancer(*_, input):
    return await traefik_redis().create_service(
        input["name"], "udp", "loadBalancer", input["loadBalancer"]
    )


@registerMutation("createTraefikUDPServiceWeighted")
async def create_udp_weighted(*_, input):
    return await traefik_redis().create_service(
        input["name"], "udp", "weighted", input["weighted"]
    )


@registerMutation("deleteTraefikService")
async def delete_service(*_, nodeId):
    return await traefik_redis().delete_service(nodeId)
