from functools import wraps
import time
from ..utils import registerQuery, registerMutation, createType, dnsname, create_node_id, undnsname


def with_dns_http(f):
    @wraps(f)
    def wrapper(obj, info, *args, **kwargs):
        dns_http = info.context["request"].state.dns_http
        return f(obj, info, *args, **kwargs, dns_http=dns_http)

    return wrapper


@registerQuery("dnsZones")
@with_dns_http
async def get_dns_zones(*_, dns_http):
    return await dns_http.get_zones()


DnsZone = createType("DnsZone")


@DnsZone.field("nodeId")
def resolve_nodeid(zone, *_):
    return create_node_id("DNS_ZONE", zone['id'])

@DnsZone.field("name")
def resolve_name(zone, *_):
    return undnsname(zone['name'])

@DnsZone.field("soa")
@with_dns_http
def resolve_soa(zone, *_, dns_http):
    return dns_http.get_soa(zone["id"])


@DnsZone.field("rules")
@with_dns_http
def resolve_rules(zone, *_, dns_http):
    return dns_http.get_rules_for_zone(zone["id"])




@registerMutation("createDnsZone")
@with_dns_http
async def create_dns_zone_mutation(*_, dns_http, input):
    return await dns_http.create_zone(input['name'], input['soa'])
    

@registerMutation("updateDnsZone")
@with_dns_http
async def update_dns_zone_mutation(*_, dns_http, nodeId, patch):
    return await dns_http.update_zone(nodeId, patch['soa'])
    

@registerMutation("deleteDnsZone")
@with_dns_http
async def delete_dns_zone_mutation(*_, dns_http, nodeId):
    return await dns_http.delete_zone(nodeId)