import graphene



class KeyValue(graphene.ObjectType):
    key = graphene.String()
    value = graphene.String()

    def resolve_key(kv, info):
        return kv[0]

    def resolve_value(kv, info):
        return kv[1]
