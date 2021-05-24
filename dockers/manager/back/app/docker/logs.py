from app.utils import createType, registerQuery, registerSubscription
from app.api import es

dockerLog = createType("DockerLog")


@registerQuery("dockerLogs")
async def resolve_docker_logs(*_, filter={}, cursor={}):
    from_ = max(cursor["from"], 0)
    size = max(min(cursor["size"], 100), 0)

    skip_internal = filter.get("skipInternal", False)

    must = []
    must_not = []

    if containerName := filter.get("containerName"):
        must.append({"terms": {"container.name": containerName}})
    if containerId := filter.get("containerId"):
        must.append({"terms": {"container.id": containerId}})


    body = {"query": {"bool": {"must": must, "must_not": must_not}}}

    r = await es.search(
        index="filebeat-docker",
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
        "result": [{**h["_source"], "nodeId": h["_id"]} for h in hits["hits"]],
        "next": None,
        "prev": None,
    }
    return response


@dockerLog.field("containerName")
def resolve_container_name(log, _):
    import json
    print(json.dumps(log, indent=2))
    return log["container"]["name"]


@dockerLog.field("containerId")
def resolve_container_id(log, _):
    return log["container"]["id"]


@dockerLog.field("date")
def resolve_date(log, _):
    return log["@timestamp"]
