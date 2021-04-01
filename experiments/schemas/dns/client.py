import requests
from graphql import GraphQLError
import time
import json

URL = "http://127.0.0.1:8081"

headers = {"X-API-KEY": "test"}


def str_to_soa(zone):
    groups = regex_soa.match(str)
    return {
        "nameserver": groups["nameserver"][:-1],
        "postmaster": groups["postmaster"][:-1].replace(".", "@", 1),
        "expire": int(groups["expire"]),
        "refresh": int(groups["refresh"]),
        "retry": int(groups["retry"]),
        "ttl": int(groups["ttl"]),
        "serial": int(groups["serial"]),
    }


def soa_to_str(soa):
    nameserver = dnsname(soa["nameserver"])
    postmaster = dnsname(soa["postmaster"].replace("@", "."))
    serial = soa["serial"] if "serial" in soa else int(time.time())
    return f'{nameserver} {postmaster} {serial} {soa["refresh"]} {soa["retry"]} {soa["expire"]} {soa["ttl"]}'


def dnsname(s):
    return s if s.endswith(".") else f"{s}."


def undnsname(s):
    return s[:-1] if s.endswith(".") else s


def FETCH(method, path, data=None):
    print(method, path)
    args = {"headers": headers}
    if data is not None:
        args["json"] = data
    r = requests.request(method, f"{URL}{path}", **args)
    if 200 <= r.status_code < 300:
        try:
            return r.json()
        except json.JSONDecodeError:
            return True

    error = r.text if r.text == "Conflict" else "Invalid data"
    try:
        error = r.json()["error"]
    except Exception:
        pass

    raise GraphQLError(error)


def GET(path):
    return FETCH("GET", path)


def DELETE(path):
    return FETCH("DELETE", path)


def PATCH(path, data):
    return FETCH("PATCH", path, data)


def POST(path, data):
    return FETCH("POST", path, data)


def get_zones():
    zones = GET("/api/v1/servers/localhost/zones")
    for zone in zones:
        zone["name"] = undnsname(zone["name"])
    return zones


def rrset_match(name, type):
    name = dnsname(name)

    def do_match(rrset):
        return rrset["name"] == name and rrset["type"] == type

    return do_match


def find_record(rrsets, name, type):
    try:
        return next(
            filter(
                rrset_match(name, type),
                rrsets,
            )
        )
    except StopIteration:
        return None


def create_rule(info):
    zone_name = dnsname(info["zone"])
    zone_info = get_zone_info(zone_name)
    if find_record(zone_info["rrsets"], info["name"], info["type"]):
        raise GraphQLError(
            f"A rule with name={info['name']} and type={info['type']} already exist on {info['zone']}"
        )

    for record in info["records"]:
        record["disabled"] = not record["enabled"]

    rrsets = [
        {
            "name": dnsname(info["name"]),
            "type": info["type"],
            "changetype": "REPLACE",
            "ttl": info["ttl"],
            "records": info["records"],
        }
    ]
    zone_name = info["zone"]
    PATCH(f"/api/v1/servers/localhost/zones/{zone_name}", {"rrsets": rrsets})
    return {**rrsets[0], "zone": zone_name}


def create_zone(name, soa):
    zone_name = dnsname(name)

    data = {
        "name": zone_name,
        "kind": "native",
        "nameservers": [dnsname(soa["nameserver"])],
        "soa_edit": "INCEPTION-EPOCH",
        "soa_edit_api": "INCEPTION-EPOCH",
    }
    POST(f"/api/v1/servers/localhost/zones", data)
    return modify_soa(zone_name, soa)


def get_rules(zone):
    for rrset in zone["rrsets"]:
        name = rrset["name"]
        type = rrset["type"]
        ttl = rrset["ttl"]
        yield {
            "zone": undnsname(zone["id"]),
            "name": undnsname(name),
            "type": type,
            "ttl": ttl,
            "records": rrset["records"],
        }


def get_zone_info(name):
    zone = GET(f"/api/v1/servers/localhost/zones/{name}")
    zone["name"] = undnsname(zone["name"])
    return {**zone, "rules": get_rules(zone)}


def disable_all_record(zone, name, type, disabled):
    zone_info = get_zone_info(zone)
    rule = find_record(zone_info["rrsets"], name, type)
    for record in rule["records"]:
        record["disabled"] = disabled

    rule["zone"] = zone_info["name"]
    rule["changetype"] = "REPLACE"

    rrsets = [rule]
    PATCH(f"/api/v1/servers/localhost/zones/{zone}", {"rrsets": rrsets})
    return rule


def enable_rule(zone, name, type):
    return disable_all_record(zone, name, type, False)


def disable_rule(zone, name, type):
    return disable_all_record(zone, name, type, True)


def update_ttl(zone, name, type, ttl):
    zone_info = get_zone_info(zone)
    rule = find_record(zone_info["rrsets"], name, type)
    if rule is None:
        raise GraphQLError(f"Rule {name} with type {type} is not found on {zone}")
    rule["ttl"] = ttl
    rule["zone"] = zone_info["id"]
    rule["changetype"] = "REPLACE"

    rrsets = [rule]
    PATCH(f"/api/v1/servers/localhost/zones/{zone}", {"rrsets": rrsets})
    return rule


def update_records(zone, name, type, records):
    zone_info = get_zone_info(zone)
    rule = find_record(zone_info["rrsets"], name, type)
    if rule is None:
        raise GraphQLError(f"Rule {name} with type {type} is not found on {zone}")

    rule["zone"] = zone_info["id"]
    rule["changetype"] = "REPLACE"
    rule["records"] = [
        {"content": r["content"], "disabled": not r["enabled"]} for r in records
    ]

    rrsets = [rule]
    PATCH(f"/api/v1/servers/localhost/zones/{zone}", {"rrsets": rrsets})
    return rule


def delete_rule(zone, name, type):
    rrsets = [{"name": dnsname(name), "type": type, "changetype": "DELETE"}]
    PATCH(f"/api/v1/servers/localhost/zones/{zone}", {"rrsets": rrsets})


def delete_zone(zone):
    DELETE(f"/api/v1/servers/localhost/zones/{zone}")


def modify_soa(zone, soa):
    zone_info = get_zone_info(zone)
    rule = find_record(zone_info["rrsets"], dnsname(zone), "SOA")
    if rule is None:
        raise GraphQLError(f"Rule {zone} with type SOA is not found on {zone}.")

    nameserver = dnsname(soa["nameserver"])
    postmaster = dnsname(soa["postmaster"].replace("@", "."))
    serial = int(time.time())
    content = f'{nameserver} {postmaster} {serial} {soa["refresh"]} {soa["retry"]} {soa["expire"]} {soa["ttl"]}'

    rule["records"] = [{"content": content, "disabled": False}]
    rule["changetype"] = "REPLACE"
    rule["ttl"] = soa["ttl"]
    rrsets = [rule]
    print(rrsets)
    PATCH(f"/api/v1/servers/localhost/zones/{zone}", {"rrsets": rrsets})
    return zone_info
