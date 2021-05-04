from ..utils import createType, registerQuery, registerSubscription
from functools import wraps
from fnmatch import fnmatch

def with_dns_redis(f):
    @wraps(f)
    def wrapper(obj, info, *args, **kwargs):
        dns_redis = info.context["request"].state.dns_redis
        return f(obj, info, *args, **kwargs, dns_redis=dns_redis)

    return wrapper


DnsLog = createType("DnsLog")

@registerQuery("dnsLogs")
@with_dns_redis
async def query_dns_logs(*_, dns_redis, filter={}, cursor={}):
    return await dns_redis.get_logs(**filter, **cursor)


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
            if fnmatch(log["domain"], domain_filter) and fnmatch(log["type"], type_filter):
                yield log