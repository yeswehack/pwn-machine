from dataclasses import dataclass
from datetime import datetime

from app.api import logdb
from app.utils import createType, registerQuery

DnsLog = createType("DnsLog")


@dataclass
class DnsLogEntry:
    rowid: int
    date: str
    origin: str
    query: str
    type: str

    @classmethod
    def from_row(cls, row):
        rowid = row[0]
        date = str(datetime.fromtimestamp(row[1]))
        return cls(rowid, date, *row[2:])


def query_from(query_filter, type_filter, offset, size):
    cur = logdb.cursor()
    total = next(cur.execute("SELECT count(rowid) FROM powerdns_logs"))[0]

    query = """
    SELECT 
        rowid, date, origin, query, type
    FROM 
        powerdns_logs
    WHERE 
        query GLOB ? AND
        type GLOB ?
    ORDER BY date DESC, rowid DESC
    LIMIT ?, ?
    ;"""

    rows = cur.execute(query, [query_filter, type_filter, offset, size])
    result = [DnsLogEntry.from_row(row) for row in rows]

    return {"result": result, "total": total}


@registerQuery("dnsLogs")
def query_dns_logs(*_, filter={}, cursor={}):
    offset = cursor.get("from", 0)
    size = max(min(cursor.get("size", 20), 100), 1)

    query = filter.get("query") or "*"
    type = filter.get("type") or "*"

    return query_from(query, type, offset, size)


@DnsLog.field("nodeId")
def resolve_nodeid(log, *_):
    return log.rowid
