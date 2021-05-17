import docker
from dataclasses import dataclass
from ..api import docker_client
from datetime import datetime

docker_client = docker.from_env()


@dataclass
class KeyValue:
    key: str
    value: str = None


def formatTime(time):
    return str(datetime.fromisoformat(time[:19]))


from . import image
from . import container
from . import network
from . import volume
from . import shell
