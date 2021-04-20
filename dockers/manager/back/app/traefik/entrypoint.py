import re
from .api import get_from_api
from ..utils.registration import createType, registerQuery

TraefikEntrypoint = createType("TraefikEntrypoint")

entrypoint_re = re.compile(
    r"(?P<ip>\d+\.\d+\.\d+\.\d+)?:(?P<port>\d+)(?:/(?P<protocol>[a-z]+))?"
)


@registerQuery("traefikEntrypoints")
def resolve_TraefikEntrypoints(*_):
    entrypoints = []
    for entrypoint in get_from_api(f"/entrypoints"):
        address = entrypoint_re.match(entrypoint["address"]).groupdict()
        entrypoints.append(
            {
                "ip": address["ip"] or "0.0.0.0",
                "port": address["port"] or 0,
                "protocol": address["protocol"] or "tcp",
                "name": entrypoint["name"],
            }
        )

    return entrypoints