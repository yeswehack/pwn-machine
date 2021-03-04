import requests
import re


regex_soa = re.compile(
    r"^\s*(?P<nameserver>\S+)\s+(?P<postmaster>\S+)\s+(?P<serial>\d+)\s+(?P<refresh>\S+)\s+(?P<retry>\S+)\s+(?P<expire>\S+)\s+(?P<ttl>\S+)\s*$"
)


def parse_soa(soa):
    groups = regex_soa.match(soa)
    return {
        "nameserver": groups["nameserver"][:-1],
        "postmaster": groups["postmaster"][:-1].replace(".", "@", 1),
        "expire": int(groups["expire"]),
        "refresh": int(groups["refresh"]),
        "retry": int(groups["retry"]),
        "ttl": int(groups["ttl"]),
        "serial": int(groups["serial"]),
    }


def with_dot(s):
    if s.endswith("."):
        return s
    return s + "."

class DNS:
    def __init__(self):
        pass

    def get(self, path):
        path = path.lstrip("/")
        headers = {"X-API-Key": self.token}
        return requests.get(
            f"{self.root}/api/v1/servers/localhost/{path}", headers=headers
        ).json()

    def post(self, path, data):
        path = path.lstrip("/")
        headers = {"X-API-Key": self.token}
        return requests.post(
            f"{self.root}/api/v1/servers/localhost/{path}", json=data, headers=headers
        ).json()

    def patch(self, path, data):
        path = path.lstrip("/")
        headers = {"X-API-Key": self.token}
        return requests.patch(
            f"{self.root}/api/v1/servers/localhost/{path}", json=data, headers=headers
        )

    def init_app(self, app):
        self.root = app.config["DNS_API_URL"].rstrip("/")
        self.token = app.config["DNS_API_TOKEN"]

    def iter_records(self, zone_id):
        api_record = self.get(f"/zones/{zone_id}")
        for rrset in api_record["rrsets"]:
            for record in rrset["records"]:
                yield {
                    "zone": zone_id,
                    "name": rrset["name"],
                    "type": rrset["type"],
                    "ttl": rrset["ttl"],
                    "content": record["content"],
                    "enabled": not record["disabled"],
                }

    def getSOA(self, records):
        for record in records:
            if record["type"] == "SOA":
                return parse_soa(record["content"])
        return {}

    def zones(self):
        zones = []
        for zone in self.get("/zones"):
            records = list(self.iter_records(zone["id"]))
            zones.append(
                {
                    "id": zone["id"],
                    "name": zone["name"],
                    "records": records,
                    **self.getSOA(records),
                }
            )
        return zones

    def createZone(self, info):
        name = with_dot(info["name"])
        zoneData = {
            "id": name,
            "name": name,
            "kind": "Native",
            "nameservers": [with_dot(info["nameserver"])],
            "soa-edit": "INCEPTION-INCREMENT",
        }
        z = self.post("/zones", zoneData)
        print(z)

        soa_content = f"{with_dot(info['nameserver'])} {with_dot(info['postmaster'].replace('@', '.'))} {info['serial']} {info['refresh']} {info['retry']} {info['expire']} {info['ttl']}"
        soaData = {
            "rrsets": [
                {
                    "name": name,
                    "type": "SOA",
                    "changetype": "REPLACE",
                    "ttl": info["ttl"],
                    "records": [
                        {
                            "content": soa_content,
                            "disabled": False,
                        }
                    ],
                }
            ]
        }
        self.patch(f"/zones/{name}", soaData)
        records = [
            {
                "zone": name,
                "name": name,
                "type": "SOA",
                "ttl": info["ttl"],
                "content": soa_content,
                "enabled": True,
            }
        ]
        return {
            "id": name,
            "name": name,
            "records": records,
            **parse_soa(soa_content),
        }