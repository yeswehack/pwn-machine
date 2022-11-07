from utils import input_name, type_name, info_input_name
from textwrap import indent

def generate_mutations_from_types(types):
    create = ""
    update = ""
    for name in types:
        create += f"{name}: gql`\n"
        create += f"  mutation create{type_name(name)}($input: {input_name(name)}!) {{\n"
        create += f"    create{type_name(name)}(input: $input){{\n"
        create += "      ... BasicMutationFragment\n"
        create += "    }\n"
        create += "  }\n"
        create += "  ${BASIC_MUTATION_FRAGMENT}\n"
        create += "`,\n"

        update += f"{name}: gql`\n"
        update += f"  mutation update{type_name(name)}($nodeId: ID!, $patch: {info_input_name(name)}!) {{\n"
        update += f"    update{type_name(name)}(nodeId: $nodeId, patch: $patch){{\n"
        update += "      ... BasicMutationFragment\n"
        update += "    }\n"
        update += "  }\n"
        update += "  ${BASIC_MUTATION_FRAGMENT}\n"
        update += f"`,\n"


    js = 'import gql from "graphql-tag"\n'

    js += 'import { BASIC_MUTATION_FRAGMENT } from "src/api/common/fragments";'
    js += "export const DELETE_MIDDLEWARE = gql`\n"
    js += "  mutation deleteMiddleware($nodeId: ID!) {\n"
    js += "    deleteTraefikMiddleware(nodeId: $nodeId) {\n"
    js += "      ... BasicMutationFragment\n"
    js += "    }\n"
    js += "  }\n"
    js += "${BASIC_MUTATION_FRAGMENT}\n"
    js += "`;\n\n"
    js += "export const CREATE_MIDDLEWARE = {\n"
    js += indent(create, "  ")
    js += "}\n"
    js += "export const UPDATE_MIDDLEWARE = {\n"
    js += indent(update, "  ")
    js += "}\n"
    return js
