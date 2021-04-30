from utils import input_name, type_name, info_input_name


def generate_mutations_from_types(types):
    js = 'import gql from "graphql-tag"\n'
    js += 'import traefikMiddlewareFragment from "./MiddlewareFragment.graphql"\n\n'
    js += "const create = {}\n"
    js += "const update = {}\n\n"
    for name in types:
        js += f"create['{name}'] = gql`\n"
        js += f"mutation create{type_name(name)}($input: {input_name(name)}!) {{\n"
        js += f"  create{type_name(name)}(input: $input){{\n"
        js += "    ... TraefikMiddlewareFragment\n"
        js += "  }\n"
        js += "}\n"
        js += "${traefikMiddlewareFragment}\n`\n"

        js += f"update['{name}'] = gql`\n"
        js += f"mutation update{type_name(name)}($nodeId: ID!, $patch: {info_input_name(name)}!) {{\n"
        js += f"  update{type_name(name)}(nodeId: $nodeId, patch: $patch){{\n"
        js += "    ... TraefikMiddlewareFragment\n"
        js += "  }\n"
        js += "}\n"
        js += "${traefikMiddlewareFragment}\n`\n\n"
    js += "export default {create, update};"
    return js
