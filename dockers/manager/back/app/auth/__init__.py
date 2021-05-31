USERNAME = "admin"
ISSUER = "PwnMachine"


from app.utils import registerQuery, registerMutation

auth_operations = {}


def auth_query(name, skip_auth=True):
    auth_operations[name] = skip_auth
    return registerQuery(name)


def auth_mutation(name, skip_auth=True):
    auth_operations[name] = skip_auth
    return registerMutation(name)


from .auth import auth_middleware
