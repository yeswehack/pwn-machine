from app.utils import registerQuery, registerMutation

auth_operations = []


def auth_query(name):
    auth_operations.append(name)
    return registerQuery(name)


def auth_mutation(name):
    auth_operations.append(name)
    return registerMutation(name)


from .auth import auth_middleware
