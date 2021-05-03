from contextlib import asynccontextmanager, contextmanager
import aiohttp
import re
import asyncio
import logging
import time
from ..utils import dnsname, undnsname, validate_node_id

ZONE_MARKER = "DNS_ZONE"

logger = logging.getLogger("uvicorn")


def log(msg):
    logger.info(f"[{__name__}] {msg}")


regex_soa = re.compile(
    r"^\s*(?P<nameserver>\S+)\s+(?P<postmaster>\S+)\s+(?P<serial>\d+)\s+(?P<refresh>\S+)\s+(?P<retry>\S+)\s+(?P<expire>\S+)\s+(?P<ttl>\S+)\s*$"
)


def soa_to_string(soa):
    nameserver = dnsname(soa["nameserver"])
    postmaster = dnsname(soa["postmaster"].replace("@", "."))
    refresh = soa["refresh"]
    retry = soa["retry"]
    expire = soa["expire"]
    ttl = soa["ttl"]
    serial = int(time.time())
    return f"{nameserver} {postmaster} {serial} {refresh} {retry} {expire} {ttl}"


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


def string_to_soa(str):
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


def get_soa(zone):
    for rule in zone["rrsets"]:
        if rule["type"] == "SOA":
            return string_to_soa(rule["records"][0]["content"])
    return None


class PowerDNSApi:
    def __init__(self, root, session):
        self.root = root
        self.session = session
        self.cache = {}
        self.runnings = set()

    @contextmanager
    def running(self, name):
        try:
            self.runnings.add(name)
            yield
        finally:
            self.runnings.remove(name)

    async def post(self, path, data):
        log(f"API POST {path}")
        full_path = f"{self.root.rstrip('/')}/{path.lstrip('/')}"
        await self.session.post(full_path, json=data)

    async def patch(self, path, data):
        log(f"API PATCH {path}")
        full_path = f"{self.root.rstrip('/')}/{path.lstrip('/')}"
        r = await self.session.patch(full_path, json=data)
        if r.status != 204:
            error = await r.json()
            raise Exception(error["error"])
        return r

    async def delete(self, path):
        log(f"API DELETE {path}")
        full_path = f"{self.root.rstrip('/')}/{path.lstrip('/')}"
        return await self.session.delete(full_path)

    async def _get(self, path):
        log(f"API GET {path}")

        full_path = f"{self.root.rstrip('/')}/{path.lstrip('/')}"

        async with self.session.get(full_path) as response:
            return await response.json()

    # All responses are cached for the duration of the HTTP request
    async def get(self, path, allow_cache=True):
        if allow_cache:
            while path in self.runnings:
                await asyncio.sleep(0.1)
            if path in self.cache:
                return self.cache[path]

            with self.running(path):
                response = await self._get(path)
        else:
            response = await self._get(path)

        self.cache[path] = response
        return response

    async def get_zone(self, zone_id, allow_cache=True):
        try:
            return await self.get(
                f"/api/v1/servers/localhost/zones/{dnsname(zone_id)}", allow_cache
            )
        except:
            return None

    async def get_zones(self, allow_cache=True):
        zones = await self.get("/api/v1/servers/localhost/zones")
        return zones

    async def get_soa(self, zone_id, allow_cache=True):
        info = await self.get_zone(zone_id, allow_cache)
        soa = get_soa(info)
        return soa

    async def get_rules_for_zone(self, zone_id, allow_cache=True):
        info = await self.get_zone(zone_id, allow_cache)
        return [{**z, "zone": info["name"]} for z in info["rrsets"]]

    async def get_rules(self, allow_cache=True):
        rules = []
        for zone in await self.get_zones(allow_cache):
            rules += await self.get_rules_for_zone(zone["id"], allow_cache)

        return rules

    async def update_soa(self, zone_name, soa):
        zone_info = await self.get_zone(zone_name)
        rule = find_record(zone_info["rrsets"], dnsname(zone_name), "SOA")
        if rule is None:
            raise Exception(f"Rule {zone} with type SOA is not found on {zone}.")

        content = soa_to_string(soa)
        rule["records"] = [{"content": content, "disabled": False}]
        rule["changetype"] = "REPLACE"
        rule["ttl"] = soa["ttl"]
        url = f"/api/v1/servers/localhost/zones/{zone_info['name']}"
        return await self.patch(url, {"rrsets": [rule]})

    # ZONES

    async def create_zone(self, name, soa):
        zone_info = await self.get_zone(name)
        if zone_info is not None:
            raise Exception("A zone with this name already exists.")
        data = {
            "name": dnsname(name),
            "kind": "native",
            "nameservers": [dnsname(soa["nameserver"])],
            "soa_edit": "INCEPTION-EPOCH",
            "soa_edit_api": "INCEPTION-EPOCH",
        }
        await self.post("/api/v1/servers/localhost/zones", data)
        await self.update_soa(name, soa)
        return await self.get_zone(name)

    async def update_zone(self, nodeId, soa):
        zone_name = validate_node_id(nodeId, "DNS_ZONE")[0]
        zone_info = await self.get_zone(zone_name)
        if zone_info is None:
            raise Exception("This zone doesn't exists.")
        await self.update_soa(zone_name, soa)
        return await self.get_zone(zone_name, allow_cache=False)

    async def delete_zone(self, nodeId):
        zone_name = validate_node_id(nodeId, "DNS_ZONE")[0]
        r = await self.delete(f"/api/v1/servers/localhost/zones/{zone_name}")
        return 200 <= r.status < 300

    # Rules

    async def create_rule(self, zone_name, name, type, ttl, records):
        zone = await self.get_zone(zone_name)
        name = dnsname(name)
        if zone is None:
            raise Exception("Invalid zone")
        if find_record(zone["rrsets"], name, type):
            raise Exception(
                f"A rule with name={name} and type={type} already exist on {zone_name}"
            )
        rrset = {
            "name": name,
            "type": type,
            "changetype": "REPLACE",
            "ttl": ttl,
            "records": records,
        }

        r = await self.patch(
            f"/api/v1/servers/localhost/zones/{zone['id']}", {"rrsets": [rrset]}
        )
        rules = await self.get_rules_for_zone(zone["id"], allow_cache=False)
        return find_record(rules, name, type)

    async def delete_rule(self, nodeId):
        zone, name, type = validate_node_id(nodeId, "DNS_RULE")
        rrset = {"name": name, "type": type, "changetype": "DELETE"}
        r = await self.patch(
            f"/api/v1/servers/localhost/zones/{zone}", {"rrsets": [rrset]}
        )
        return 200 <= r.status < 300


@asynccontextmanager
async def new_powerdns_http_client(root, key):
    headers = {"X-Api-Key": key}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            yield PowerDNSApi(root, session)
    finally:
        pass
