import click
import json
from io import StringIO
from contextlib import redirect_stdout
from tabulate import tabulate


def send_request(method, path, data=None):
    out = StringIO()
    args = [
        "-X",
        method,
        f"http://127.0.0.1:8081/{path.lstrip('/')}",
        "-H",
        f"X-API-Key: {pm.config['environment']['PDNS_API_KEY']}",
    ]
    if data:
        args += ["-d", json.dumps(data)]

    out = pm.get_exec("powerdns", ["curl", *args])
    try:
        return json.loads(out or '"success!"')
    except Exception as e:
        exit(out.decode())


def get(path):
    return send_request("GET", path)


def patch(path, data):
    return send_request("PATCH", path, data)


@click.group(name="dns")
def cli():
    """Manage DNS"""


@cli.command()
@click.argument("zone")
@click.argument("name")
@click.argument("type")
@click.argument("record")
@click.option("--ttl", help="DNS entry ttl", default=60, type=int)
def add(
    zone, name, record, type, ttl,
):
    """add a DNS entry"""
    zone_path = f"/api/v1/servers/localhost/zones/{zone}"
    new_record = {
        "rrsets": [
            {
                "name": name,
                "type": type,
                "ttl": ttl,
                "changetype": "REPLACE",
                "records": [{"content": record, "disabled": False},],
            }
        ]
    }
    print(patch(zone_path, new_record))


@cli.command()
@click.argument("zone")
@click.argument("name")
@click.argument("ips", nargs=-1)
def rebind(zone, name, ips):
    """
    Add a domain that reply a random ip from a list
    """
    if len(ips) < 2:
        exit("You need at least 2 ips")
    zone_path = f"/api/v1/servers/localhost/zones/{zone}"
    lua_ip_array = ",".join(f"'{ip}'" for ip in ips)
    lua_code = f'({{{lua_ip_array}}})[math.random({len(ips)})]'
    new_record = {
        "rrsets": [
            {
                "name": name,
                "type": "LUA",
                "ttl": "0",
                "changetype": "REPLACE",
                "records": [{"content": f'A "{lua_code}"', "disabled": False},],
            }
        ]
    }
    print(patch(zone_path, new_record))


@cli.command()
@click.argument("zone")
@click.argument("name")
@click.argument("type")
def rm(zone, name, type):
    """remove a DNS entry"""
    zone_path = f"/api/v1/servers/localhost/zones/{zone}"
    new_record = {
        "rrsets": [{"name": name, "type": type, "changetype": "DELETE", "records": []}]
    }
    print(patch(zone_path, new_record))


@cli.command()
def ls():
    """list all dns entries"""
    zones = get("/api/v1/servers/localhost/zones")
    to_print = []
    for zone in zones:
        entries = get(f"/api/v1/servers/localhost/zones/{zone['id']}")
        records = []
        for entry in entries["rrsets"]:

            for record in entry["records"]:
                records.append(
                    [zone["id"], entry["name"], entry["type"], record["content"]]
                )

        # sort records by type then by name
        to_print.extend(sorted(records, key=lambda i: (i[2], i[1])))
        # Spacing
        to_print.append([])

    print(tabulate(to_print, headers=["Zone", "Name", "Type", "Record"]))
