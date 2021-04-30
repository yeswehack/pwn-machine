
def type_name(name):
    return f"TraefikMiddleware{name[0].capitalize() + name[1:]}"


def input_name(name):
    return f"{type_name(name)}Input"


def info_name(name):
    return f"{type_name(name)}Info"


def info_input_name(name):
    return f"{info_name(name)}Input"