from functools import wraps
import asyncio
from starlette_context import context
from contextlib import contextmanager


@contextmanager
def no_cache():
    try:
        context["cache_disabled"] = True
        yield
    finally:
        context["cache_disabled"] = False


def cacheMethodForQuery(func):
    runnings = set()
    running_marker = object()

    @contextmanager
    def running(name):
        try:
            runnings.add(name)
            yield
        finally:
            runnings.remove(name)

    @wraps(func)
    async def wrapper(self, *args, **kwargs):

        cache = context["cache"]
        key = (func.__qualname__, args, frozenset(kwargs.items()))
        if key not in cache or context["cache_disabled"]:
            cache[key] = running_marker
            r = await func(self, *args, **kwargs)
            cache[key] = r
            return r

        while cache[key] is running_marker:
            await asyncio.sleep(0.01)

        return cache[key]

    @wraps(func)
    async def ignore_cache(self, *args, **kwargs):
        with no_cache:
            return wrapper(self, *args, **kwargs)

    setattr(wrapper, "no_cache", ignore_cache)

    return wrapper
