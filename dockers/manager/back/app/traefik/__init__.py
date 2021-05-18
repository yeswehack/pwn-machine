from ..redis import client as redis_client
from functools import wraps


def with_traefik_redis(f):
    @wraps(f)
    def wrapper(obj, info, *args, **kwargs):
        traefik_redis = info.context["request"].state.traefik_redis
        return f(obj, info, *args, **kwargs, traefik_redis=traefik_redis)

    return wrapper


TRAEFIK_REDIS_ROOK_KEY = "traefik"


from . import router
from . import entrypoint
from . import service
from . import middlewares
