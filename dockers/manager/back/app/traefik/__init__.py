from ..redis import client as redis_client

TRAEFIK_REDIS_ROOK_KEY = "traefik"


class TraefikRedisClient:
    root = TRAEFIK_REDIS_ROOK_KEY

    def __init__(self, client):
        self.client = client

    def _with_root_key(self, key):
        return f"{self.root}/{key.lstrip('/')}"

    def set(self, key, value):
        return self.client.set(self._with_root_key(key), value)

    def delete_pattern(self, pattern):
        print(self._with_root_key(pattern))
        for key in self.client.keys(self._with_root_key(pattern)):
            print("DELET KEY", key)
            self.client.delete(key)


client = TraefikRedisClient(redis_client)


from . import router
from . import entrypoint
from . import service
from . import middlewares