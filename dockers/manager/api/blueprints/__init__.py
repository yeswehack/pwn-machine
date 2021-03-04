#!/usr/bin/env python
from .docker import bp as docker_bp
from .traefik import bp as traefik_bp
from .dns import bp as dns_bp
from .ssh import bp as ssh_bp

blueprints = {
    "/docker": docker_bp,
    "/traefik": traefik_bp,
    "/dns": dns_bp,
    "/shell": ssh_bp,
}

__all__ = ["blueprints"]
