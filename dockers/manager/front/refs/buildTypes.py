#!/usr/bin/env python
import json
from collections import defaultdict

with open("KV.json") as f:
    kv = json.load(f)


typemap = {"foobar": "STR", "true": "BOOL", "42": "NUMBER"}

types = defaultdict(dict)
subtypes = defaultdict(dict)


def parseType(name, options, value, depth=0):
    t = types if depth == 0 else subtypes
    if len(options) == 1:
        t[name][options[0]] = value
    else:
        nextname, *options = options

        t[name][nextname] = "REF"
        parseType(nextname, options, value, depth + 1)


for k, v in kv:
    if not k.startswith("traefik/http/middlewares/"):
        continue
    name, *options = k.split("/")[4:]

    v = typemap[v]
    if options[-1] in ["1", "name1"]:
        continue
    if options[-1] == "0":
        v = "ARRAY"
        options = options[:-1]
    if options[-1] == "name0":
        v = "PAIR"
        options = options[:-1]

    parseType(name, options, v)
    continue

    current = types[typename]
    for i, option in enumerate(options):
        isLast = i == (len(options) - 1)
        if not isLast:
            if option not in current:
                current[option] = {}
            current = current[option]
        else:
            current[option] = v

print(json.dumps({"middlewares": types, "types": subtypes}, indent=2))
