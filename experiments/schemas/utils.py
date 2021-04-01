import graphene

queries = {}
mutations = {}
subscriptions = {}


def get_name(cls):
    name = graphene.utils.str_converters.to_camel_case(cls.__name__)
    return name[0].lower() + name[1:]


def register_mutation(name=None):
    def wrapper(c):
        mutation_name = get_name(c) if name is None else name
        if mutation_name in mutations:
            raise Exception(f"Mutation {mutation_name} was registered twice")
        mutations[mutation_name] = c.Field()
        return c

    return wrapper


def register_subscription(name=None):
    def wrapper(c):
        subscription_name = get_name(c) if name is None else name
        if subscription_name in subscriptions:
            raise Exception(f"Subscription {subscription_name} was registered twice")
        subscriptions[subscription_name] = graphene.Field(c)
        return c

    return wrapper


def create_resolver(c):
    def resolver(*args, **kwargs):
        return c()

    return resolver


def register_query(name=None):
    def wrapper(c):
        if name in queries:
            raise Exception(f"Query {name} was registered twice")
        queries[name] = graphene.Field(c, required=True)
        queries[f"resolve_{name}"] = create_resolver(c)
        return c

    return wrapper


def get_queries():
    return type("Query", (graphene.ObjectType,), queries)


def get_mutations():
    return type("Mutation", (graphene.ObjectType,), mutations)


def get_subscriptions():
    return type("Subscription", (graphene.ObjectType,), subscriptions)