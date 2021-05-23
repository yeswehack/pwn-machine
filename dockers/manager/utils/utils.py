import re
def type_name(name):
    return f"TraefikMiddleware{name[0].capitalize() + name[1:]}"


def input_name(name):
    return f"{type_name(name)}Input"


def info_name(name):
    return f"{type_name(name)}Info"

def fragment_name(name):
    return f"{name[0].capitalize() + name[1:]}Fragment"

def const_name(name):
    return re.sub(r"[A-Z]+", lambda s: "_" + s.group(0), name).upper() + "_FRAGMENT"

def info_input_name(name):
    return f"{info_name(name)}Input"