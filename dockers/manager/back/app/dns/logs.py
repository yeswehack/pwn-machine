from app.utils import createType, registerQuery, registerSubscription
from functools import wraps
from fnmatch import fnmatch
from app.api import es


def with_dns_redis(f):
    @wraps(f)
    def wrapper(obj, info, *args, **kwargs):
        dns_redis = info.context["request"].state.dns_redis
        return f(obj, info, *args, **kwargs, dns_redis=dns_redis)

    return wrapper


DnsLog = createType("DnsLog")


def log_from_es_to_gql(log):
    entry = {**log["_source"]}
    entry["nodeId"] = log["_id"]
    if log["_source"]["return_code"] != "NOERROR":
        entry["error"] = log["_source"]["return_code"]
    return entry


@registerQuery("dnsLogs")
async def query_dns_logs(*_, filter={}, cursor={}):
    from_ = max(cursor["from"], 0)
    size = max(min(cursor["size"], 100), 0)

    query_filter = "*" + filter.get("query", "") + "*"
    type_filter = "*" + filter.get("type", "") + "*"

    body = {
        "query": {
            "bool": {
                "must": [
                    {"wildcard": {"query": query_filter}},
                    {"wildcard": {"type": type_filter}},
                ],
            },
        }
    }

    r = await es.search(
        index="filebeat-pdns-*",
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


@DnsLog.field("date")
def resolve_date(log, _):
    return log["date"]


@DnsLog.field("nodeId")
def resolve_date(log, _):
    print(log)
    return log["nodeId"]


@registerSubscription("dnsLogs")
@with_dns_redis
async def dns_logs_subscription(*_, dns_redis, filter={}):
    domain_filter = filter.get("domain", "*")
    type_filter = filter.get("type", "*")
    async with dns_redis.client.pubsub() as sub:
        await sub.psubscribe(f"__keyspace@0__:dns/data/*")
        async for event in sub.listen():
            if event["data"] != "hset":
                continue
            key = event["channel"][15:]
            log = await dns_redis.client.hgetall(key)
            if fnmatch(log["domain"], domain_filter) and fnmatch(
                log["type"], type_filter
            ):
                yield log
