import os


def from_env(name, default):
    # Handle unset and empty variable
    return os.getenv(name) or default


PM_REDIS_HOST = from_env("PM_REDIS_HOST", "redis://localhost")
PM_TRAEFIK_HTTP_API = from_env("PM_TRAEFIK_HTTP_API", "http://127.0.0.1:8080")  # /api
PM_TRAEFIK_REDIS_ROOT = from_env("PM_TRAEFIK_REDIS_ROOT", "traefik")
PM_POWERDNS_HTTP_API = from_env("PM_POWERDNS_HTTP_API", "http://127.0.0.1:8081")
PM_POWERDNS_HTTP_API_KEY = from_env("PM_POWERDNS_HTTP_API_KEY", "test")
PM_ELASTIC_SEARCH_HTTP_API = from_env("PM_ELASTIC_SEARCH_HTTP_API", "127.0.0.1:9200")
