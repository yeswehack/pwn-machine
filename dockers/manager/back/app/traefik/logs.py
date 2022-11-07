from dataclasses import dataclass
from datetime import datetime

from app.api import logdb
from app.utils import createType, registerQuery

TraefikLog = createType("TraefikLog")


@dataclass
class TraefikLogEntry:
    rowid: int
    date: int
    origin: str
    status: int
    host: str
    method: str
    path: str
    port: int
    protocol: str
    scheme: str
    routerName: str
    entrypointName: str
    serviceName: str

    @classmethod
    def from_row(cls, row):
        rowid = row[0]
        date = str(datetime.fromtimestamp(row[1]))
        return cls(rowid, date, *row[2:])


def query_from(entrypoint_filter, router_filter, service_filter, offset, size):
    cur = logdb.cursor()
    total = next(cur.execute("SELECT count(rowid) FROM traefik_logs"))[0]

    filters = ["TRUE"]
    args = []
    if entrypoint_filter:
        filters.append(
            f"entrypoint_name IN ({', '.join('?' * len(entrypoint_filter))})"
        )
        args += entrypoint_filter
    if router_filter:
        filters.append(f"router_name IN ({', '.join('?' * len(router_filter))})")
        args += router_filter
    if service_filter:
        filters.append(f"service_name IN ({', '.join('?' * len(service_filter))})")
        args += service_filter

    query = f"""
    SELECT 
        rowid, date, origin, status, host, method, path, port, protocol, scheme, router_name, entrypoint_name, service_name
    FROM 
        traefik_logs
    WHERE 
        {' AND '.join(filters)}
    ORDER BY date DESC, rowid DESC
    LIMIT ?, ?
    ;"""

    rows = cur.execute(query, [*args, offset, size])
    result = [TraefikLogEntry.from_row(row) for row in rows]

    return {"result": result, "total": total}


@registerQuery("traefikLogs")
def query_traefik_logs(*_, filter={}, cursor={}):
    offset = cursor.get("from", 0)
    size = max(min(cursor.get("size", 20), 100), 1)

    entrypoints = filter.get("entrypoints") or []
    routers = filter.get("routers") or []
    services = filter.get("services") or []

    return query_from(entrypoints, routers, services, offset, size)


@TraefikLog.field("nodeId")
def resolve_nodeid(log, *_):
    return log.rowid


@TraefikLog.field("port")
def resolve_port(log, *_):
    if not isinstance(log.port, int):
        if log.scheme == "https":
            return 443
        else:
            return 80
    return log.port
