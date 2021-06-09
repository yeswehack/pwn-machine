from utils import (
    info_input_name,
    info_name,
    info_name,
    type_name,
    input_name,
    fragment_name,
    const_name,
)
from textwrap import indent


def generate_basic(fields):
    graphql = ""
    for attr, value in fields.items():
        if isinstance(value, dict):
            graphql += f"{attr} {{\n"
            graphql += indent(generate_basic(value), "  ")
            graphql += f"}}\n"
        elif value == "KV":
            graphql += f"{attr} {{\n"
            graphql += f"  key\n"
            graphql += f"  value\n"
            graphql += f"}}\n"
        else:
            graphql += f"{attr}\n"
    return graphql


def generate_sub_fragment(name, fields):
    graphql = f"fragment {fragment_name(name)} on {type_name(name)} {{\n"
    graphql += f"  {name} {{\n"
    graphql += indent(generate_basic(fields), "    ")
    graphql += "  }\n"
    graphql += "}\n"

    js = f"export const {const_name(name).upper()} = gql`\n"
    js += indent(graphql, "  ")
    js += "`\n"
    return js


def generate_fragment(name, fields):
    graphql = ""
    graphql += f"... on {type_name(name)} {{\n"
    graphql += f"  ...{fragment_name(name)}\n"
    graphql += f"}}\n"
    return indent(graphql, "  ")


def generate_fragments_from_types(types):
    header = "fragment MiddlewareFragment on TraefikMiddleware {\n"
    header += f"  nodeId\n"
    header += f"  name\n"
    header += f"  type\n"
    header += f"  error\n"
    header += f"  enabled\n"
    header += f"  usedBy {{\n"
    header += f"    nodeId \n"
    header += f"    name \n"
    header += f"  }}\n"

    prefix = ""
    graphql = ""
    footer = "}\n"
    for middleware_name, fields in types.items():
        footer += f"${{{const_name(middleware_name)}}}\n"
        prefix += generate_sub_fragment(middleware_name, fields)
        graphql += generate_fragment(middleware_name, fields)

    js = 'import gql from "graphql-tag"\n\n'
    js += f"export const {const_name('middleware')} = gql`\n"
    js += indent( header + graphql + footer, "  ")
    js += "`\n"
    return prefix + js
