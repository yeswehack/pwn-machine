from base64 import b64decode, b64encode
import json as JSON
from .registration import (
    registerMutation,
    registerSubscription,
    registerQuery,
    createType,
    createInterface,
)

class PMException(Exception):
    pass


def base64_encode(s, json=False):
    if json:
        s = JSON.dumps(s)
    return b64encode(s.encode()).decode()


def base64_decode(s, json=False):
    r = b64decode(s.encode()).decode()
    if not json:
        return r
    try:
        return JSON.loads(r)
    except:
        return None


def create_kv_resolver(key):
    def resolve_kv(target, *_):
        kv = target.get(key, {})
        return [{"key": k, "value": v} for k, v in kv.items()]

    return resolve_kv


def create_node_id(target_type, *args):
    if len(args) == 0:
        raise ValueError("Invalid nodeId.")
    if not all(isinstance(a, (str, int)) for a in args):
        raise ValueError("Invalid nodeId.")
    return base64_encode([target_type, *args], json=True)


def validate_node_id(nodeId, target_type):
    try:
        result = base64_decode(nodeId, json=True)
        if not isinstance(result, list):
            raise ValueError()
        if not all(isinstance(r, (str, int)) for r in result):
            raise ValueError()
        if len(result) < 2:
            raise ValueError()

        typename, *args = result
        if typename != target_type:
            raise ValueError()
        return args
    except Exception as e:
        raise ValueError(f"Invalid nodeId.")
