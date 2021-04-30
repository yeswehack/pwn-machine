from contextlib import asynccontextmanager, contextmanager
import aiohttp
import re
import asyncio
import logging


logger = logging.getLogger("uvicorn")


def log(msg):
    logger.info(f"[{__name__}] {msg}")


regex_soa = re.compile(
    r"^\s*(?P<nameserver>\S+)\s+(?P<postmaster>\S+)\s+(?P<serial>\d+)\s+(?P<refresh>\S+)\s+(?P<retry>\S+)\s+(?P<expire>\S+)\s+(?P<ttl>\S+)\s*$"
)


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

    async def get_zone_info(self, zone_id):
        return await self.get(f"/api/v1/servers/localhost/zones/{zone_id}")

    async def get_zones(self):
        zones = await self.get("/api/v1/servers/localhost/zones")
        return zones

    async def get_soa(self, zone_id):
        info = await self.get_zone_info(zone_id)
        soa = get_soa(info)
        return soa

    async def get_rules_for_zone(self, zone_id):
        info = await self.get_zone_info(zone_id)
        return [{**z, "zone": info["name"]} for z in info["rrsets"]]

    async def get_rules(self):
        rules = []
        for zone in await self.get_zones():
            rules += await self.get_rules_for_zone(zone["id"])

        return rules


@asynccontextmanager
async def new_powerdns_http_client(root, key):
    headers = {"X-Api-Key": key}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            yield PowerDNSApi(root, session)
    finally:
        pass