import docker

docker_client = docker.from_env()


def KeyValue(it, *keys):
    return dict(zip(keys or ["key", "value"], it))


from . import image
from . import container
