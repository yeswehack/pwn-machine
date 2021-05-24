from typing import NamedTuple
from datetime import datetime
from app.api import docker_client


class KeyValue(NamedTuple):
    key: str
    value: str = None


def kv_to_dict(kv):
    return {entry["key"]: entry["value"] for entry in kv}


def formatTime(time):
    return str(datetime.fromisoformat(time[:19]))


from . import image
from . import container
from . import network
from . import volume
from . import shell
from . import logs
