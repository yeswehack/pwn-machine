# pylint: disable=all
import graphene
from collections import namedtuple
from .client import (
    dnsname,
    get_zones,
    get_zone_info,
    create_rule,
    create_zone,
    enable_rule,
    delete_rule,
    delete_zone,
    disable_rule,
    update_records,
    update_ttl,
    modify_soa,
)
from schemas.utils import register_mutation, register_query, register_subscription
from datetime import datetime
from hashlib import md5
import re
import redis

regex_soa = re.compile(
    r"^\s*(?P<nameserver>\S+)\s+(?P<postmaster>\S+)\s+(?P<serial>\d+)\s+(?P<refresh>\S+)\s+(?P<retry>\S+)\s+(?P<expire>\S+)\s+(?P<ttl>\S+)\s*$"
)

redis_client = redis.from_url("redis://localhost/0", decode_responses=True)


def get_domain_logs(domain, type):
    logs = []
    for key in redis_client.scan_iter(f"dns/logs/{domain}/{type}/*"):
        logs.append(redis_client.hgetall(key))
    return sorted(logs, key=lambda k: k["time"])


def hash(*args):
    return md5(b"".join(a.encode() for a in args)).hexdigest()


def get_soa(zone):
    for rule in zone["rrsets"]:
        if rule["type"] == "SOA":
            groups = regex_soa.match(rule["records"][0]["content"])
            return {
                "nameserver": groups["nameserver"][:-1],
                "postmaster": groups["postmaster"][:-1].replace(".", "@", 1),
                "expire": int(groups["expire"]),
                "refresh": int(groups["refresh"]),
                "retry": int(groups["retry"]),
                "ttl": int(groups["ttl"]),
                "serial": int(groups["serial"]),
            }

    return None


class DnsLog(graphene.ObjectType):
    origin = graphene.String()
    type = graphene.String()
    domain = graphene.String()
    time = graphene.String()

    def resolve_time(log, info):
        date = datetime.fromtimestamp(float(log["time"]))
        return date.isoformat()


class Record(graphene.ObjectType):
    content = graphene.String()
    enabled = graphene.Boolean()

    def resolve_enabled(entry, info):
        return not entry["disabled"]


class Rule(graphene.ObjectType):
    id = graphene.ID()
    zone = graphene.String()
    type = graphene.String()
    name = graphene.String()
    records = graphene.List(Record)
    ttl = graphene.Int()

    def resolve_id(rule, info):
        return hash(dnsname(rule["zone"]), rule["type"], dnsname(rule["name"]))


class Soa(graphene.ObjectType):
    nameserver = graphene.String()
    postmaster = graphene.String()
    expire = graphene.Int()
    refresh = graphene.Int()
    retry = graphene.Int()
    ttl = graphene.Int()
    serial = graphene.Int()


class Zone(graphene.ObjectType):
    id = graphene.ID()
    soa = graphene.Field(Soa)
    serial = graphene.Int()
    name = graphene.String()
    rules = graphene.List(Rule)

    def resolve_rules(zone, info):
        zone = get_zone_info(zone["id"])
        return [{**z, "zone": zone["name"]} for z in zone["rrsets"]]

    def resolve_soa(zone, info):
        zone_info = get_zone_info(zone["id"])
        soa = get_soa(zone_info)
        return soa


class SoaInput(graphene.InputObjectType):
    nameserver = graphene.String(required=True)
    postmaster = graphene.String(required=True)
    expire = graphene.Int(required=True)
    refresh = graphene.Int(required=True)
    retry = graphene.Int(required=True)
    ttl = graphene.Int(required=True)


class RecordInput(graphene.InputObjectType):
    content = graphene.String(required=True)
    enabled = graphene.Boolean(required=True)


class RuleInput(graphene.InputObjectType):
    zone = graphene.String(required=True)
    type = graphene.String(required=True)
    name = graphene.String(required=True)
    records = graphene.List(RecordInput)
    ttl = graphene.Int(required=True)


@register_subscription()
class DnsLogsSubscription(graphene.ObjectType):
    log = graphene.Field(DnsLog, rule_name=graphene.String(), rule_type=graphene.String())

    async def subscribe_log(root, info, rule_name, rule_type):
        redis_client.pubsub()
        p.psubscribe(f"__keyspace@0__:dns/{rule_name}/{rule_type}/*")
        for event in p.listen():
            if event["data"] == "hset":
                key = event["chanel"][15:]
                yield redis_client.hgetall(key)

@register_query("dns")
class Dns(graphene.ObjectType):
    id = graphene.ID(default_value="DNS")
    zones = graphene.List(Zone)
    rules = graphene.List(Rule)

    logs = graphene.List(DnsLog, rule_name=graphene.String(), rule_type=graphene.String())

    def resolve_zones(root, info):
        return get_zones()

    def resolve_rules(root, info):
        rules = []
        for zone in get_zones():
            info = get_zone_info(zone["id"])
            for record in info["rules"]:
                rules.append(record)

        return rules

    def resolve_logs(zone, info, rule_name="*", rule_type="*"):
        return get_domain_logs(rule_name, rule_type)


@register_mutation()
class EnableDnsRule(graphene.Mutation):
    class Arguments:
        zone = graphene.String(required=True)
        name = graphene.String(required=True)
        type = graphene.String(required=True)

    rule = graphene.Field(Rule)

    def mutate(root, info, zone, name, type):
        rule = enable_rule(zone, name, type)
        return EnableDnsRule(rule=rule)


@register_mutation()
class DisableDnsRule(graphene.Mutation):
    class Arguments:
        zone = graphene.String(required=True)
        name = graphene.String(required=True)
        type = graphene.String(required=True)

    rule = graphene.Field(Rule)

    def mutate(root, info, zone, name, type):
        rule = disable_rule(zone, name, type)
        return EnableDnsRule(rule=rule)


@register_mutation()
class DeleteDnsRule(graphene.Mutation):
    class Arguments:
        zone = graphene.String(required=True)
        name = graphene.String(required=True)
        type = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, zone, name, type):
        delete_rule(zone, name, type)
        return DeleteDnsRule(ok=True)


@register_mutation()
class DeleteDnsZone(graphene.Mutation):
    class Arguments:
        zone = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, zone):
        delete_zone(zone)
        return DeleteDnsZone(ok=True)


@register_mutation()
class CreateDnsRule(graphene.Mutation):
    class Arguments:
        rule = RuleInput(required=True)

    rule = graphene.Field(Rule)

    def mutate(root, info, rule):
        rule = create_rule(rule)
        return CreateDnsRule(rule=rule)


@register_mutation()
class UpdateRecordsForDnsRule(graphene.Mutation):
    class Arguments:
        zone = graphene.String(required=True)
        name = graphene.String(required=True)
        type = graphene.String(required=True)
        records = graphene.List(RecordInput)

    rule = graphene.Field(Rule)

    def mutate(root, info, zone, name, type, records):
        rule = update_records(zone, name, type, records)
        return UpdateRecordsForDnsRule(rule=rule)


@register_mutation()
class UpdateTTLForDnsRule(graphene.Mutation):
    class Arguments:
        zone = graphene.String(required=True)
        name = graphene.String(required=True)
        type = graphene.String(required=True)
        ttl = graphene.Int(required=True)

    rule = graphene.Field(Rule)

    def mutate(root, info, zone, name, type, ttl):
        rule = update_ttl(zone, name, type, ttl)
        return UpdateTTLForDnsRule(rule=rule)


@register_mutation()
class CreateDnsZone(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        soa = SoaInput(required=True)

    zone = graphene.Field(Zone)

    def mutate(root, info, name, soa):
        zone = create_zone(name, soa)
        return CreateDnsZone(zone=zone)


@register_mutation()
class ModifySoaForDnsZone(graphene.Mutation):
    class Arguments:
        zone = graphene.String(required=True)
        soa = SoaInput(required=True)

    zone = graphene.Field(Zone)

    def mutate(root, info, zone, soa):
        zone = modify_soa(zone, soa)
        return ModifySoaForDnsZone(zone=zone)