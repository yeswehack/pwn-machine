from ..utils import registerQuery, createType, createInterface, base64_encode
from . import with_traefik_http
MAPPING = {
    "addprefix": "TraefikMiddlewareAddPrefix",
    "basicauth": "TraefikMiddlewareBasicAuth",
    "buffering": "TraefikMiddlewareBuffering",
    "chain": "TraefikMiddlewareChain",
    "circuitbreaker": "TraefikMiddlewareCircuitBreaker",
    "compress": "TraefikMiddlewareCompress",
    "contenttype": "TraefikMiddlewareContentType",
    "digestauth": "TraefikMiddlewareDigestAuth",
    "errors": "TraefikMiddlewareErrors",
    "tls": "TraefikMiddlewareTls",
    "forwardauth": "TraefikMiddlewareForwardAuth",
    "headers": "TraefikMiddlewareHeaders",
    "ipstrategy": "TraefikMiddlewareIpStrategy",
    "ipwhitelist": "TraefikMiddlewareIpWhiteList",
    "sourcecriterion": "TraefikMiddlewareSourceCriterion",
    "inflightreq": "TraefikMiddlewareInFlightReq",
    "issuer": "TraefikMiddlewareIssuer",
    "subject": "TraefikMiddlewareSubject",
    "info": "TraefikMiddlewareInfo",
    "passtlsclientcert": "TraefikMiddlewarePassTLSClientCert",
    "ratelimit": "TraefikMiddlewareRateLimit",
    "redirectregex": "TraefikMiddlewareRedirectRegex",
    "redirectscheme": "TraefikMiddlewareRedirectScheme",
    "replacepath": "TraefikMiddlewareReplacePath",
    "replacepathregex": "TraefikMiddlewareReplacePathRegex",
    "retry": "TraefikMiddlewareRetry",
    "stripprefix": "TraefikMiddlewareStripPrefix",
    "stripprefixregex": "TraefikMiddlewareStripPrefixRegex",
}

TraefikMiddleware = createInterface("TraefikMiddleware")

def create_basic_resolver(key):
    def basic_resolver(middleware, *_):
        return middleware[key]
    return basic_resolver

for object_type in MAPPING.values():
    ObjectType = createType(object_type)
    key = object_type[len("TraefikMiddleware"): ]
    key = key[0].lower() + key[1:]
    ObjectType.field(key)(create_basic_resolver(key))

    @ObjectType.field("usedBy")
    @with_traefik_http
    async def resolve_usedBy(middleware, *_, traefik_http):
        if "usedBy" not in middleware:
            return []
        routers = []
        for router_name in middleware["usedBy"]:
            router = await traefik_http.get_router("http", router_name)
            routers.append(router)
        return routers
    
    @ObjectType.field("enabled")
    def resolve_enabled(middleware, info):
        return middleware["status"] == "enabled"


@TraefikMiddleware.field("nodeId")
async def resolve_nodeid(middleware, *_):
    return base64_encode(["middleware", middleware["name"]], json=True)


@TraefikMiddleware.type_resolver
def resolve_middleware_type(obj, *_):
    return MAPPING[obj["type"]]

@registerQuery("traefikMiddlewares")
@with_traefik_http
async def resolve_middlewares(*_, traefik_http):
    return await traefik_http.get_middlewares()

