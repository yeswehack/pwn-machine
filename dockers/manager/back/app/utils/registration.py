from ariadne import ObjectType, InterfaceType
from functools import wraps
from app.exception import PMException
import asyncio

registered_types = []


def createType(name):
    t = ObjectType(name)
    registered_types.append(t)
    return t


def createInterface(name):
    t = InterfaceType(name)
    registered_types.append(t)
    return t


registered_queries = {}


def registerQuery(name):
    def decorator(f):
        registered_queries[name] = f
        return f

    return decorator


registered_mutations = {}


def registerMutation(name):
    def decorator(f):

        @wraps(f)
        async def async_wrapper(*args, **kwargs):
            print("WRAPS ASYNC")
            try:
                result = await f(*args, **kwargs)
                return {"success": True, "result": result}
            except PMException as e:
                return {"success": False, "error": str(e)}

        @wraps(f)
        def wrapper(*args, **kwargs):
            print("WRAPS ")
            try:
                result = f(*args, **kwargs)
                return {"success": True, "result": result}
            except PMException as e:
                return {"success": False, "error": str(e)}

        w = async_wrapper if asyncio.iscoroutinefunction(f) else wrapper
        registered_mutations[name] = w
        return w

    return decorator


registered_subscriptions = {}


def registerSubscription(name):
    def decorator(f):
        registered_subscriptions[name] = f
        return f

    return decorator
