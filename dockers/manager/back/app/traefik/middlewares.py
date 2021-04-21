from ..utils.registration import registerQuery, createType, createInterface
from .api import get_from_api

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
    async def resolve_usedBy(middleware, *_):
        if "usedBy" not in middleware:
            return []
        routers = []
        for router_name in middleware["usedBy"]:
            router = await get_from_api(f"/http/routers/{router_name}")
            routers.append(router)
        return routers
    
    @ObjectType.field("enabled")
    def resolve_enabled(middleware, *_):
        return middleware["status"] == "enabled"

@TraefikMiddleware.type_resolver
def resolve_middleware_type(obj, *_):
    return MAPPING[obj["type"]]

@registerQuery("traefikMiddlewares")
async def resolve_middlewares(*_):
    return await get_from_api("/http/middlewares")

