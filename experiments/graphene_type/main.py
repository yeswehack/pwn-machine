import graphene
from icecream import ic
from typing import NewType, GenericAlias, Optional
from graphql import GraphQLError


class DnsLog(graphene.ObjectType):
    origin = graphene.String()
    type = graphene.String()
    domain = graphene.String()
    time = graphene.String()

    def resolve_time(log, info):
        date = datetime.fromtimestamp(float(log["time"]))
        return date.isoformat()


ID = NewType("ID", str)


def check_optional(t):
    if isinstance(type, GenericAlias) and type.__origin__ == Optional:
        if len(type.__args__) != 1:
            raise GraphQLError("Optional must have a single arguments")
        return t, {**args, "required": False}
    return 

def parse_type(type):
    scalars = {
        int: graphene.Int,
        float: graphene.Float,
        bool: graphene.Boolean,
        str: graphene.String,
        ID: graphene.ID,
    }

    if type in scalars:
        return scalars[type], []

    if type == list:
        print(type)


    if isinstance(type, GenericAlias):
        if type.__origin__ == list:
            if len(type.__args__) != 1:
                raise GraphQLError("List must have a single arguments")
            return graphene.List, (type_to_graphene(type.__args__[0]),)

    raise GraphQLError(f"Invalid type {type}")


def type_to_graphene(t):
    parsed = parse_type(t)
    ic(parsed)
    return parsed

class ObjectMeta(type):
    def __new__(cls, name, bases, class_dict):

        if "__annotations__" in class_dict:
            for name, type in class_dict["__annotations__"].items():
                g = type_to_graphene(type)
        return super().__new__(cls, name, bases, class_dict)


class Object(metaclass=ObjectMeta):
    def __init__(self):
        pass


class DnsLog2(Object):
    id: ID
    origin: list[str]


print(DnsLog2)
