import asyncio
import socket
import sys
from struct import unpack

import dns.rcode
import dns.rdatatype
from google.protobuf.message import DecodeError

from elasticsearch import AsyncElasticsearch

import dnsmessage_pb2
import time

GRABBER_HOST = "127.0.0.1"
GRABBER_PORT = 4000
ES_HOSTS = ["elasticsearch"]
ES_INDEX = "powerdns-logs"

es = AsyncElasticsearch(ES_HOSTS)


async def wait_for_es(es):
    # wait for es for ~30s
    for i in range(30):
        try:
            await es.wait_for_status("yellow")
            return
        except:
            await asyncio.sleep(1)
            continue
    print("Unable to connect to elasticsearch, stopping process")
    exit(1)


async def init_mappings():
    body = {
        "mappings": {
            "properties": {
                "type": {"type": "wildcard"},
                "query": {"type": "wildcard"},
            }
        }
    }
    return await es.indices.create(ES_INDEX, body=body)


async def save_to_es(log):
    await es.index(index=ES_INDEX, body=log)


def rrs_to_response(rrs):
    decode = lambda x: x.decode()
    mapping = {
        "A": lambda x: socket.inet_ntop(socket.AF_INET, x),
        "AAAA": lambda x: socket.inet_ntop(socket.AF_INET6, x),
        "CNAME": decode,
        "MX": decode,
        "PTR": decode,
        "NS": decode,
        "SPF": decode,
        "SRV": decode,
        "TXT": decode,
    }
    data_type = dns.rdatatype.to_text(rrs.type)
    rdata = mapping[data_type](rrs.rdata)
    return {
        "name": rrs.name,
        "type": data_type,
        "rdata": rdata,
    }


def msg_to_log(msg):
    log = {}
    if 0 < msg.response.rcode > 4095:
        log["return_code"] = "UNKNOW_ERROR"
    else:
        log["return_code"] = dns.rcode.to_text(msg.response.rcode)

    log["responses"] = [rrs_to_response(rrs) for rrs in msg.response.rrs]
    log["origin"] = socket.inet_ntoa(getattr(msg, "from"))
    log["date"] = msg.timeSec
    log["query"] = msg.question.qName
    log["type"] = dns.rdatatype.to_text(msg.question.qType)
    return log


async def log_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    while True:
        (size,) = unpack("!H", await reader.readexactly(2))
        data = await reader.readexactly(size)
        msg = dnsmessage_pb2.PBDNSMessage()
        try:
            msg.ParseFromString(data)
            if msg.type == dnsmessage_pb2.PBDNSMessage.DNSResponseType:
                log = msg_to_log(msg)
                asyncio.ensure_future(save_to_es(log))
        except DecodeError as e:
            print(f"Error parsing message, {e}")


async def main():
    await wait_for_es(es)
    if not await es.indices.exists(ES_INDEX):
        await init_mappings()
    server = await asyncio.start_server(log_handler, GRABBER_HOST, GRABBER_PORT)
    print(f"Log grabber server started on {GRABBER_HOST}:{GRABBER_PORT}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
