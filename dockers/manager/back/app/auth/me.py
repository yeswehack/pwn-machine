
@query.field("me")
def resolve_me(*_):
    return {
        "is_first_login": False,
    }