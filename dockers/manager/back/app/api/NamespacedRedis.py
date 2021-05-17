import aioredis
import asyncio


class NamespacedRedis:
    def __init__(self, root, client):
        self.root = root
        self.client = client

    def _ns(self, s):
        return f"{self.root}/{s.lstrip('/')}"

    def _uns(self, s):
        return s.lstrip(self.root + "/")

    def make_basic(self, name):
        f = getattr(self.client, name)

        def basic(key, *args, **kwargs):
            return f(self._ns(key), *args, **kwargs)

        return basic


    def __getattr__(self, name):
        basics = ["get", "set", "hget", "hgetall", "lrange"]
        if name in basics:
            return self.make_basic(name)

    async def keys(self, key):
        return [self._uns(key) for key in await self.client.keys(self._ns(key))]


async def main():
    c = NamespacedRedis(
        "dns", aioredis.from_url("redis://localhost", decode_responses=True)
    )
    for k in await c.lrange("logs", 0, 100):
        print(k)
        v = await c.hgetall(k)
        print(v)


if __name__ == "__main__":
    asyncio.run(main())
