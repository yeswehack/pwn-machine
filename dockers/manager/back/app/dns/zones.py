from functools import wraps
from ..utils import registerQuery, createType


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
    return zone["id"]


@DnsZone.field("soa")
@with_dns_http
def resolve_soa(zone, *_, dns_http):
    return dns_http.get_soa(zone["id"])


@DnsZone.field("rules")
@with_dns_http
def resolve_rules(zone, *_, dns_http):
    return dns_http.get_rules_for_zone(zone["id"])


DnsRecord = createType("DnsRecord")


@DnsRecord.field("enabled")
def resolve_enabled(record, *_):
    return not record["disabled"]


@registerQuery("dnsRules")
@with_dns_http
async def get_dns_rules(*_, dns_http):
    return await dns_http.get_rules()