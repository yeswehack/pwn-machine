#!/usr/bin/env python
import re
import signal
import redis
import time
import os
import asyncio
import sys
from uuid import uuid4

EXPIRE_DURATION = int(os.getenv("EXPIRE_DURATION", 60 * 60 * 244))  # keep log 24h
CLEANUP_INTERVAL = int(os.getenv("CLEANUP_INTERVAL", 60))  # cleanup every 60s

redis_client = redis.Redis()

query_reg = re.compile(
    r"^\w+ \d{2} \d{2}:\d{2}:\d{2} Remote (\d+\.\d+.\d+.\d+) wants ([^ ]+) .*"
)


def escape_decode(s):
    def replace(m):
        return chr(int(m.group(1)))

    return re.sub(r"\\(\d{3})", replace, s)


def log_query(origin, domain, type):
    t = time.time()
    key = f"dns/logs/data/{uuid4()}"
    mapping = {"origin": origin, "domain": domain, "type": type, "time": t}
    pipe = redis_client.pipeline()
    lkey = f"dns/logs/domain/{domain}"
    dkey = f"dns/logs/domains"
    r = (
        pipe.hset(key, mapping=mapping)
        .expire(key, EXPIRE_DURATION)
        .zadd(lkey, {key: t})
        .zadd(dkey, {lkey: t})
        .execute()
    )
    print(lkey, key)


def parse_query(l):
    if match := query_reg.match(l):
        origin = match.group(1)
        query = match.group(2)[1:-2]
        domain, _, type = query.rpartition("|")
        domain = escape_decode(domain)

        log_query(origin, domain, type)


async def read_loop():
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)

    while l := await reader.readline():
        parse_query(l.decode()[:-1])


async def cleanup_loop():
    with open("cleanup.lua") as f:
        cleanup = redis_client.register_script(f.read())

    while True:
        cleanup()
        await asyncio.sleep(CLEANUP_INTERVAL)


async def main():
    read = asyncio.Task(read_loop())
    cleanup = asyncio.Task(cleanup_loop())

    await asyncio.gather(read, cleanup)


if __name__ == "__main__":
    asyncio.run(main())
