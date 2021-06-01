
from .traefik import TraefikHTTPApi , TraefikRedisApi
from .powerdns import PowerdnsHTTPApi
from .elasticsearch import es
from .shell import create_shell
from .docker import docker_client 

def get_traefik_http_api():
    return TraefikHTTPApi.get_instance()

def get_traefik_redis_api():
    return TraefikRedisApi.get_instance()

def get_powerdns_http_api():
    return PowerdnsHTTPApi.get_instance()


