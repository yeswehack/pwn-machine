#!/usr/bin/env python
import re
import signal
import redis
import time
import os
import asyncio
import sys
from uuid import uuid4

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
EXPIRE_DURATION = int(os.getenv("EXPIRE_DURATION", 60 * 60 * 24))
MAX_LOG_ENTRY = 10000
query_reg = re.compile(
    r"^\w+ \d{2} \d{2}:\d{2}:\d{2} Remote (\d+\.\d+.\d+.\d+) wants ([^ ]+) .*"
)


def escape_decode(s):
    def replace(m):
        return chr(int(m.group(1)))

    return re.sub(r"\\(\d{3})", replace, s)


def log_query(redis_client, query):
    log_key = f"dns/logs"
    data_key = f"dns/data/{uuid4()}"
    r = (
        redis_client.pipeline()
        .lpush(log_key, data_key)
        .ltrim(log_key, 0, MAX_LOG_ENTRY)
        .hset(data_key, mapping=query)
        .expire(data_key, EXPIRE_DURATION)
        .execute()
    )


def parse_query(l):
    if match := query_reg.match(l):
        origin = match.group(1)
        query = match.group(2)[1:-2]
        domain, _, type = query.rpartition("|")
        domain = escape_decode(domain)

        return {"origin": origin, "domain": domain, "type": type, "time": time.time()}
    return None


def main():
    redis_client = redis.from_url(REDIS_URL)
    with open("/dev/stdin") as f:
        while l := f.readline():
            line = l[:-1]
            print(line)
            query = parse_query(line)
            if query:
                log_query(redis_client, query)


if __name__ == "__main__":
    main()
