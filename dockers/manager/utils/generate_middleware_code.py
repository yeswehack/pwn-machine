import requests
from collections import Counter, defaultdict
from textwrap import dedent
import io
import sys
import textwrap
import json
from contextlib import redirect_stdout
from generate_middleware_schema import generate_schema_from_types
from generate_middleware_fragments import generate_fragments_from_types
from generate_middleware_mutations import generate_mutations_from_types

REF_URL = "https://raw.githubusercontent.com/traefik/traefik/v2.4/docs/content/reference/dynamic-configuration/kv-ref.md"


def graphql_name(name):
    return f"TraefikMiddleware{name[0].capitalize() + name[1:]}"


def get_refs():
    md = requests.get(REF_URL).text.strip()
    refs = []
    for line in md.split("\n"):
        columns = line.split("|")
        key = columns[1][2:-2]
        value = columns[2][2:-2]
        refs.append([key, value])
    return refs


def get_type(value, is_array, is_kv):
    type_mapping = {"true": "Boolean", "foobar": "String", "42": "Int"}
    if is_kv:
        return "KV"
    if is_array:
        return f"[{type_mapping[value]}]"
    return type_mapping[value]


def get_middlewares():
    needle = "traefik/http/middlewares/"
    refs = get_refs()
    middlewares = []
    for key, value in refs:
        if not key.startswith(needle):
            continue
        if key.endswith("1"):
            # ignore second array ref
            continue
        if value == "bar":
            # ignore plugin stuff
            continue

        _, _, key = key[len(needle) :].partition("/")
        middlewares.append([key, value])
    return middlewares


def check_if_array(l):
    if l.endswith("/0"):
        return True, l[:-2]
    return False, l


def check_if_kv(l):
    if l.endswith("/name0"):
        return True, l[:-6]
    return False, l


def parse_line(types, l, v, is_array, is_kv):
    if ("/") not in l:
        types[l] = get_type(v, is_array, is_kv)
    else:
        name, _, options = l.partition("/")
        if name not in types:
            types[name] = {}
        parse_line(types[name], options, v, is_array, is_kv)


def parse_middleware(types, l, v):
    name, _, options = l.partition("/")
    is_kv, options = check_if_kv(options)
    is_array, options = check_if_array(options)
    if name not in types:
        types[name] = {}

    parse_line(types[name], options, v, is_array, is_kv)


def generate_json(types):
    return json.dumps(types)

if __name__ == "__main__":
    choices = ["json", "mutation", "schema", "fragment"]
    if len(sys.argv) != 2:
        exit(f"Usage: {sys.argv[0]} <{'|'.join(choices)}>")
    choice = sys.argv[1].lower()

    types = {}

    for key, value in get_middlewares():
        parse_middleware(types, key, value)

    if "json".startswith(choice):
        print(generate_json(types))
    if "schema".startswith(choice):
        print(generate_schema_from_types(types))
    if "fragment".startswith(choice):
        print(generate_fragments_from_types(types))
    if "mutation".startswith(choice):
        print(generate_mutations_from_types(types))
# print(json.dumps(types))
# print()
