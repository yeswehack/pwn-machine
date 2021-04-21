import requests
from collections import Counter, defaultdict
from icecream import ic
from textwrap import dedent


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
        return f"[{graphql_name('HeaderPair')}]"
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
        parse_line(types[name], options, v, is_kv, is_array)


def parse_middleware(types, l, v):
    name, _, options = l.partition("/")
    is_kv, options = check_if_kv(options)
    is_array, options = check_if_array(options)
    if name not in types:
        types[name] = {}

    parse_line(types[name], options, v, is_array, is_kv)


def dict_to_graphql(types, visited=set()):
    for name, attrs in types.items():
        if name in visited:
            continue
        visited.add(name)
        type_name = graphql_name(name)
        info_name = graphql_name(name) + "Info"


        graphql = f"type {info_name} {{\n"

        for attr, value in attrs.items():
            if isinstance(value, dict):
                dict_to_graphql({attr: value})
                graphql += f"  {attr}: {graphql_name(attr)}\n"
            else:
                graphql += f"  {attr}: {value}\n"
        graphql += "}\n\n"

        graphql += f"type {type_name} implements TraefikMiddleware {{\n"
        graphql += "  name: String!\n"
        graphql += "  provider: String!\n"
        graphql += "  type: String!\n"
        graphql += "  enabled: Boolean\n"
        graphql += "  usedBy: [TraefikRouter!]!\n"
        graphql += f"  {name}: {info_name}!\n"
        graphql += "}\n\n\n"
        print(graphql)


types = {}
for key, value in get_middlewares():
    parse_middleware(types, key, value)

print(
    f""" 

interface TraefikMiddleware {{
    name: String!
    provider: String!
    type: String!
    enabled: Boolean
    usedBy: [TraefikRouter!]!
}}

type {graphql_name("HeaderPair")} {{
    name: String
    value: String
}}

"""
)

dict_to_graphql(types)
#        print(key)
#        print(middleware_name, conf)


# refs = get_refs()
# conf = get_middlewares(refs)
# ic(conf)
