from app.utils import createType, registerQuery, registerSubscription
from app.api import es

TraefikLog = createType("TraefikLog")


@registerQuery("traefikLogs")
async def resolve_traefik_logs(*_, filter={}, cursor={}):
    from_ = max(cursor["from"], 0)
    size = max(min(cursor["size"], 100), 0)

    skip_internal = filter.get("skipInternal", False)

    must = [{"exists": {"field": "json.StartUTC"}}]
    must_not = []

    if filter.get("skipInternal", False):
        must_not.append({"match": {"json.entryPointName": "traefik"}})
    if entrypointName := filter.get("entrypoint"):
        must.append({"terms": {"json.entryPointName.keyword": entrypointName}})
    if routerName := filter.get("router"):
        must.append({"terms": {"json.RouterName.keyword": routerName}})
    if serviceName := filter.get("service"):
        must.append({"terms": {"json.ServiceName.keyword": serviceName}})

    body = {"query": {"bool": {"must": must, "must_not": must_not}}}

    r = await es.search(
        index="filebeat-traefik-*",
        sort="@timestamp:desc",
        body=body,
        from_=from_,
        size=size,
    )
    hits = r["hits"]
    total = hits["total"]["value"]
    next_from = from_ + len(hits["hits"])
    response = {
        "total": hits["total"]["value"],
        "result": [h["_source"]["json"] for h in hits["hits"]],
        "next": None,
        "prev": None,
    }
    return response


@TraefikLog.field("date")
def resolve_time(log, _):
    return log["StartUTC"]


@TraefikLog.field("host")
def resolve_host(log, _):
    return log["RequestHost"]


@TraefikLog.field("host")
def resolve_host(log, _):
    return log["RequestHost"]


@TraefikLog.field("status")
def resolve_status(log, _):
    return log["DownstreamStatus"]


@TraefikLog.field("method")
def resolve_method(log, _):
    return log["RequestMethod"]


@TraefikLog.field("path")
def resolve_path(log, _):
    return log["RequestPath"]


@TraefikLog.field("port")
def resolve_port(log, _):
    port = log["RequestPort"]
    if port == "-":
        if log["RequestScheme"] == "http":
            return 80
        elif log["RequestScheme"] == "https":
            return 443
        return 0  # error should be unreachable ?
    return port


@TraefikLog.field("protocol")
def resolve_protocol(log, _):
    return log["RequestProtocol"]


@TraefikLog.field("scheme")
def resolve_scheme(log, _):
    return log["RequestScheme"]


@TraefikLog.field("routerName")
def resolve_router(log, _):
    return log.get("RouterName")


@TraefikLog.field("entrypointName")
def resolve_entrypoint(log, _):
    return log.get("entryPointName")


@TraefikLog.field("serviceName")
def resolve_service(log, _):
    return log.get("ServiceName")


@TraefikLog.field("origin")
def resolve_origin(log, _):
    return log.get("ClientHost")

