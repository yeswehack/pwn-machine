from utils import info_input_name, info_name, info_name, type_name, input_name
import textwrap




def create_info_type(name, fields, visited=set()):
    if name in visited:
        return ""
    else:
        visited.add(name)
    prefix = ""
    graphql = f"type {info_name(name)} {{\n"
    for field_name, field_type in fields.items():
        if field_type == "KV":
            graphql += f"  {field_name}: [KeyValue!]!\n"
        elif isinstance(field_type, dict):
            prefix += create_info_type(field_name, field_type)
            graphql += f"  {field_name}: {info_name(field_name)}\n"
        else:
            graphql += f"  {field_name}: {field_type}\n"
    graphql += f"}}\n\n"
    return prefix + graphql


def create_info_input_type(name, fields, visited=set()):
    if name in visited:
        return ""
    else:
        visited.add(name)
    prefix = ""
    graphql = f"input {info_input_name(name)} {{\n"
    for field_name, field_type in fields.items():
        if field_type == "KV":
            graphql += f"  {field_name}: [KeyValueInput!]!\n"
        elif isinstance(field_type, dict):
            prefix += create_info_input_type(field_name, field_type)
            graphql += f"  {field_name}: {info_input_name(field_name)}\n"
        else:
            graphql += f"  {field_name}: {field_type}\n"
    graphql += f"}}\n\n"
    return prefix + graphql


def create_type(name, fields):
    graphql = create_info_type(name, fields)
    graphql += create_info_input_type(name, fields)
    graphql += f"type {type_name(name)} implements TraefikMiddleware {{\n"
    graphql += f"  nodeId: ID!\n"
    graphql += f"  name: String!\n"
    graphql += f"  provider: String!\n"
    graphql += f"  type: String!\n"
    graphql += f"  enabled: Boolean\n"
    graphql += f"  usedBy: [TraefikRouter!]!\n"
    graphql += f"  {name}: {info_name(name)}!\n"
    graphql += f"}}\n\n"

    graphql += f"input {input_name(name)} {{\n"
    graphql += f"  name: String!\n"
    graphql += f"  {name}: {info_input_name(name)}!\n"
    graphql += f"}}\n\n"


    graphql += "extend type Mutation {\n"
    graphql += f"  create{type_name(name)}(input: {input_name(name)}!): {type_name(name)}!\n"
    graphql += f"  update{type_name(name)}(nodeId: ID!, patch: {info_input_name(name)}!): {type_name(name)}!\n"
    graphql += "}\n\n\n"

    return graphql


def generate_base_schema():
    graphql = f""" 
        interface TraefikMiddleware {{
            nodeId: ID!
            name: String!
            provider: String!
            type: String!
            enabled: Boolean
            usedBy: [TraefikRouter!]!
        }}
        """
    return textwrap.dedent(graphql)


def generate_schema_from_types(types):
    graphql = generate_base_schema()
    for middleware_name, fields in types.items():
        #if middleware_name != "headers":
        #    continue
        graphql += create_type(middleware_name, fields)

    return graphql
