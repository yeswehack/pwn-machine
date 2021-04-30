from utils import info_input_name, info_name, info_name, type_name, input_name
import textwrap

def generate_sub_fragment(fields):
    graphql = ""
    for attr, value in fields.items():
        if isinstance(value, dict):
            graphql += f"{attr} {{\n"
            graphql += generate_sub_fragment(value)
            graphql += f"}}\n"
        elif value == "KV":
            graphql += f"{attr} {{\n"
            graphql += f"  key\n"
            graphql += f"  value\n"
            graphql += f"}}\n"
        else:
            graphql += f"{attr}\n"
    return textwrap.indent(graphql, "  ")


def generate_fragment(name, fields):
    graphql = ""
    graphql += f"... on {type_name(name)} {{\n"
    graphql += f"  nodeId\n"
    graphql += f"  name\n"
    graphql += f"  type\n"
    graphql += f"  enabled\n"
    graphql += f"  usedBy {{\n"
    graphql += f"    name \n"
    graphql += f"  }}\n"
    graphql += f"  {name} {{\n"
    graphql += textwrap.indent(generate_sub_fragment(fields), "  ")
    graphql += f"  }}\n"
    graphql += f"}}\n"
    return textwrap.indent(graphql, "  ")


def generate_fragments_from_types(types):
    prefix = "fragment TraefikMiddlewareFragment on TraefikMiddleware {\n"
    prefix += "  name\n"
    prefix += "  nodeId\n"

    graphql = ""
    for middleware_name, fields in types.items():
        graphql += generate_fragment(middleware_name, fields)

    suffix = "}"
    return prefix + graphql + suffix
