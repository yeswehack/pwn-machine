
from .traefik import TraefikHTTPApi 
from .powerdns import PowerdnsHTTPApi
from .elasticsearch import es
from .shell import ShellManager
from .docker import docker_client 

def get_traefik_http_api():
    return TraefikHTTPApi._instance

def get_powerdns_http_api():
    return PowerdnsHTTPApi._instance