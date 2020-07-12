from collections.abc import Iterable
from pprint import pprint
from contextlib import contextmanager
import yaml
import re
import os
import bcrypt
import ipaddress
from dataclasses import dataclass
from .utils import hl
from collections import namedtuple

_re_container_name = r"[a-zA-Z0-9][a-zA-Z0-9_.-]*"
re_container_name = re.compile(f"^({_re_container_name})$")
re_container_name_port = re.compile(
    f"^(?P<container>{_re_container_name}):(?P<port>[0-9]+)$"
)
re_auth = re.compile(r"^(?P<login>[^:]+):(?P<hash>.+)$")
VERSION = 1.1


def yaml_load(filename):
    try:
        with open(filename) as f:
            return yaml.safe_load(f)
    except yaml.parser.ParserError as e:
        exit(e)


@contextmanager
def keep_error_trail(name):
    try:
        yield
    except ParserError as e:
        e.trail = [name, e.trail]
        raise e


def as_list(obj):
    if isinstance(obj, list):
        return obj
    if obj is None:
        return list()
    return (obj,)


def get_ip(ip):
    assert_type(ip, str)
    try:
        if "/" in ip:
            return ipaddress.ip_network(ip, strict=False)
        else:
            return ipaddress.ip_address(ip)
    except ValueError as e:
        raise ParserError(str(e))


def get_domains(domain_list):
    for domain in domain_list:
        yield domain


class ParserError(Exception):
    def __init__(self, msg, trail=None):
        super().__init__(msg)
        self.msg = msg
        self.trail = [trail, None] if trail else None

    def __str__(self):
        if self.trail:
            return f"{hl('red', '[ERROR]')} {self.msg} in {self.get_trail()}"
        else:
            return f"{hl('red', '[ERROR]')} {self.msg}"

    def get_trail(self):
        def inner(trail):
            current, next_item = trail
            if next_item:
                return f"{hl('blue', current)}.{inner(next_item)}"
            return hl("blue", current)

        return inner(self.trail)


def assert_type(obj, valid_type):
    if not isinstance(valid_type, tuple):
        valid_type = (valid_type,)
    if not isinstance(obj, valid_type):
        valid = "' or '".join(hl("yellow", t.__name__) for t in valid_type)
        raise ParserError(
            f"Invalid type '{hl('yellow', type(obj).__name__)}', expected '{valid}'"
        )
    return obj


def get_regex(regex, str):
    try:
        match = next(regex.finditer(str))
        return match.groupdict()
    except StopIteration:
        raise ParserError(
            f"Invalid value '{hl('yellow', str)}' expected '{hl('yellow', regex.pattern)}'"
        )


def get_typed_value(config, key, expected_type, required=True):
    if key not in config:
        if required:
            raise ParserError(f"Missing required key '{hl('blue', key)}'")
        return None

    value = config.get(key)

    with keep_error_trail(key):
        assert_type(value, expected_type)
    return value


def parse_basic_auth(domain):
    basic_auth = as_list(
        get_typed_value(domain, "basic-auth", (list, str), required=False)
    )

    for entry in basic_auth:
        match = get_regex(re_auth, entry)
        if match["login"].startswith("~"):
            hash = bcrypt.hashpw(match["hash"].encode(), bcrypt.gensalt())
            yield f"{match['login'][1:]}:{hash.decode()}"
        else:
            yield f"{match['login']}:{match['hash']}"


def parse_ip_list(domain, type_name):
    allow_list = as_list(
        get_typed_value(domain, type_name, (list, str), required=False) or list()
    )

    with keep_error_trail(type):
        return [get_ip(ip) for ip in allow_list]


def parse_domain(domain_name, domain):
    with keep_error_trail(domain_name):
        result = {}
        if domain is None:
            domain = {}

        with keep_error_trail("basic-auth"):
            result["basic-auth"] = list(parse_basic_auth(domain))

        with keep_error_trail("ip-allow-list"):
            result["ip-allow-list"] = parse_ip_list(domain, "ip-allow-list")

        with keep_error_trail("ip-deny-list"):
            result["ip-deny-list"] = parse_ip_list(domain, "ip-deny-list")

        return result


def find_exposed(compose):
    found = False
    for service_name, service in compose.get("services", {}).items():
        labels = service.get("labels")
        if labels is None:
            continue
        if isinstance(labels, list):
            labels = {l.partition("=")[0]: l.partition("=")[2] for l in labels}
        for name, value in labels.items():
            if name == "pm.http.port":
                if found:
                    raise ParserError(
                        f"Multiple {hl('yellow', 'pm.http.port')} labels found"
                    )
                found = {"container": service_name, "port": value}

    if not found:
        raise ParserError(
            f"Unable to find a container with label {hl('yellow', 'pm.http.port')}",
            "labels",
        )

    return found


def parse_web(http, compose_file):
    result = {}

    compose = yaml_load(compose_file)

    shorter_name = "/".join(compose_file.split("/")[-3:])
    with keep_error_trail(f"[...{shorter_name}]"):
        container_port = find_exposed(compose)

    result.update(container_port)

    domain_list = get_typed_value(http, "domains", (dict, list))
    if isinstance(domain_list, list):
        domain_list = {name: {} for name in domain_list}
    result["domains"] = {
        domain_name: parse_domain(domain_name, domain)
        for domain_name, domain in domain_list.items()
    }

    return result


def get_info_from_compose(compose_file):
    config = yaml_load(compose_file)

    services = list(config.get("services", {}).keys())
    volumes = []
    for volume in config.get("volumes", {}).values():
        if volume and "name" in volume:
            volumes.append(volume["name"])
    return services, volumes


def parse_service(config_dir, name, service):
    if service is None:
        service = {}
    with keep_error_trail(name):
        result = {}

        if "compose-file" in service:
            compose_path = get_typed_value(service, "compose-file", str)
        else:
            compose_path = f"./services/{name}/docker-compose.yml"

        result["compose-file"] = os.path.realpath(
            os.path.join(config_dir, compose_path)
        )
        containers, volumes = get_info_from_compose(result["compose-file"])
        result["containers"] = containers
        result["volumes"] = volumes
        with keep_error_trail("http"):
            http = get_typed_value(service, "http", dict, required=False)
            result["http"] = parse_web(http, result["compose-file"]) if http else None

        with keep_error_trail("https"):
            https = get_typed_value(service, "https", dict, required=False)
            result["https"] = (
                parse_web(https, result["compose-file"]) if https else None
            )
        return result


def parse_domains(domains):
    result = {}
    for domain, ip in domains.items():
        assert_type(domain, str)
        with keep_error_trail(domain):
            assert_type(ip, str)
        result[domain] = ip
    return result


def parse(config_dir, config):
    result = {}
    version = get_typed_value(config, "version", float)
    if version > VERSION:
        raise ParserError(
            f"Configuration file is from newer version {version} > {VERSION}"
        )

    domains = get_typed_value(config, "domains", dict)
    with keep_error_trail("domains"):
        if not domains:
            raise ParserError(f"You need at least one domain")
        result["domains"] = parse_domains(domains)
    result["docker-machine"] = get_typed_value(config, "docker-machine", str)
    services = get_typed_value(config, "services", dict)

    with keep_error_trail("services"):
        result["services"] = {
            name: parse_service(config_dir, name, service)
            for name, service in services.items()
        }
    result["environment"] = (
        get_typed_value(config, "environment", dict, required=False) or {}
    )
    return result


def parse_config(config_dir, filename):
    yaml_config = yaml_load(filename)
    try:
        config = parse(config_dir, yaml_config)
        return config
    except ParserError as e:
        exit(str(e))
