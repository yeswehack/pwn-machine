from ariadne import ObjectType, InterfaceType


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
        registered_mutations[name] = f
        return f

    return decorator
