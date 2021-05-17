from functools import wraps
import time
from ..utils import registerQuery, registerMutation, createType, dnsname, create_node_id, undnsname
from ..api import get_powerdns_http_api as dns_http



@registerQuery("dnsZones")
async def get_dns_zones(*_):
    return await dns_http().get_zones()


DnsZone = createType("DnsZone")


@DnsZone.field("nodeId")
def resolve_nodeid(zone, *_):
    return create_node_id("DNS_ZONE", zone['id'])

@DnsZone.field("name")
def resolve_name(zone, *_):
    return undnsname(zone['name'])

@DnsZone.field("soa")
def resolve_soa(zone, *_):
    return dns_http().get_soa(zone["id"])


@DnsZone.field("rules")
def resolve_rules(zone, *_):
    print("ZONE", zone)
    return dns_http().get_rules_for_zone(zone["id"])




@registerMutation("createDnsZone")
async def create_dns_zone_mutation(*_, input):
    return await dns_http().create_zone(input['name'], input['soa'])
    

@registerMutation("updateDnsZone")
async def update_dns_zone_mutation(*_, nodeId, patch):
    return await dns_http().update_zone(nodeId, patch['soa'])
    

@registerMutation("deleteDnsZone")
async def delete_dns_zone_mutation(*_, nodeId):
    return await dns_http().delete_zone(nodeId)