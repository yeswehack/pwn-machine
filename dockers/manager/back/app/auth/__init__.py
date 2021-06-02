import os
from warnings import warn

from app.utils import registerMutation, registerQuery

from .database import Database

AUTH_DISABLED_ENVVAR = "PM_DISABLE_AUTH"
if AUTH_DISABLED := bool(os.environ.get(AUTH_DISABLED_ENVVAR)):
    warn(f"Never set {AUTH_DISABLED_ENVVAR} in production")

db = Database()
auth_operations = {}


def auth_query(name, skip_auth=True):
    auth_operations[name] = skip_auth
    return registerQuery(name)


def auth_mutation(name, skip_auth=True):
    auth_operations[name] = skip_auth
    return registerMutation(name)


from .auth import auth_middleware
