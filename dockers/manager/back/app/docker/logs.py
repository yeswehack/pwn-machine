from dataclasses import dataclass
from datetime import datetime

from app.api import logdb
from app.utils import createType, registerQuery

DockerLog = createType("DockerLog")


@dataclass
class DockerLogEntry:
    rowid: int
    date: str
    image: str
    container: str
    stream: str
    log: str

    @classmethod
    def from_row(cls, row):
        rowid = row[0]
        date = str(datetime.fromtimestamp(row[1]))
        return cls(rowid, date, *row[2:])


def query_from(image_filter, container_filter, offset, size):
    cur = logdb.cursor()
    total = next(cur.execute("SELECT count(rowid) FROM docker_logs"))[0]

    filters = ["TRUE"]
    args = []
    if image_filter:
        filters.append(f"image IN ({', '.join('?' * len(image_filter))})")
        args += image_filter
    if container_filter:
        filters.append(f"container IN ({', '.join('?' * len(container_filter))})")
        args += container_filter

    query = f"""
    SELECT 
        rowid, date, image, container, stream, log
    FROM 
        docker_logs
    WHERE 
        {' AND '.join(filters)}
    ORDER BY date DESC, rowid DESC
    LIMIT ?, ?
    ;"""

    rows = cur.execute(query, [*args, offset, size])
    result = [DockerLogEntry.from_row(row) for row in rows]

    return {"result": result, "total": total}


@registerQuery("dockerLogs")
def query_docker_logs(*_, filter={}, cursor={}):
    offset = cursor.get("from", 0)
    size = max(min(cursor.get("size", 20), 100), 1)

    images = filter.get("images") or []
    containers = filter.get("containers") or []

    return query_from(images, containers, offset, size)


@DockerLog.field("nodeId")
def resolve_nodeid(log, *_):
    return log.rowid


@DockerLog.field("container")
def resolve_container(log, *_):
    return log.container[1:]
