import docker
from typing import NamedTuple
from datetime import datetime

docker_client = docker.from_env()



class KeyValue(NamedTuple):
    key: str
    value: str = None


def formatTime(t):
    return str(datetime.fromisoformat(t.partition(".")[0]))


from . import image
from . import container
from . import network
from . import volume
