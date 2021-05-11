import docker
from dataclasses import dataclass

docker_client = docker.from_env()


@dataclass
class KeyValue:
    key: str
    value: str = ""


@dataclass
class RepoTag:
    repository: str
    tag: str = "latest"


from . import image
from . import container
from . import network
from . import volume
