
from ..utils.registration import registerQuery, createType



TraefikService = createType("TraefikService")
TraefikServiceLoadBalancer = createType("TraefikServiceLoadBalancer")

@registerQuery("traefikServices")
def resolve_TraefikServices(*_):
    all_routers = []
    for proto in ["http", "tcp", "udp"]:
        routers = get_from_api(f"/{proto}/services")
        for router in routers:
            router["protocol"] = proto
        all_routers += routers

    return all_routers

@TraefikService.field("enabled")
def resolve_traefik_enabled(obj, *_):
    return obj["status"] == "enabled"



@TraefikService.field("loadBalancer")
def resolve_loadBalancer(service, *_):
    if "loadBalancer" in service:
        return service["loadBalancer"]
    return None


@TraefikServiceLoadBalancer.field("healthCheck")
def healthCheck(loadBalancer, *_):
    if "healthCheck" in loadBalancer:
        return loadBalancer["healthCheck"]
    return None