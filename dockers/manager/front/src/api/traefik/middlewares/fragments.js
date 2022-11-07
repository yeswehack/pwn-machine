export const ADD_PREFIX_FRAGMENT = gql`
  fragment AddPrefixFragment on TraefikMiddlewareAddPrefix {
    addPrefix {
      prefix
    }
  }
`;
export const BASIC_AUTH_FRAGMENT = gql`
  fragment BasicAuthFragment on TraefikMiddlewareBasicAuth {
    basicAuth {
      headerField
      realm
      removeHeader
      users
      usersFile
    }
  }
`;
export const BUFFERING_FRAGMENT = gql`
  fragment BufferingFragment on TraefikMiddlewareBuffering {
    buffering {
      maxRequestBodyBytes
      maxResponseBodyBytes
      memRequestBodyBytes
      memResponseBodyBytes
      retryExpression
    }
  }
`;
export const CHAIN_FRAGMENT = gql`
  fragment ChainFragment on TraefikMiddlewareChain {
    chain {
      middlewares
    }
  }
`;
export const CIRCUIT_BREAKER_FRAGMENT = gql`
  fragment CircuitBreakerFragment on TraefikMiddlewareCircuitBreaker {
    circuitBreaker {
      expression
    }
  }
`;
export const COMPRESS_FRAGMENT = gql`
  fragment CompressFragment on TraefikMiddlewareCompress {
    compress {
      excludedContentTypes
    }
  }
`;
export const CONTENT_TYPE_FRAGMENT = gql`
  fragment ContentTypeFragment on TraefikMiddlewareContentType {
    contentType {
      autoDetect
    }
  }
`;
export const DIGEST_AUTH_FRAGMENT = gql`
  fragment DigestAuthFragment on TraefikMiddlewareDigestAuth {
    digestAuth {
      headerField
      realm
      removeHeader
      users
      usersFile
    }
  }
`;
export const ERRORS_FRAGMENT = gql`
  fragment ErrorsFragment on TraefikMiddlewareErrors {
    errors {
      query
      service
      status
    }
  }
`;
export const FORWARD_AUTH_FRAGMENT = gql`
  fragment ForwardAuthFragment on TraefikMiddlewareForwardAuth {
    forwardAuth {
      address
      authRequestHeaders
      authResponseHeaders
      authResponseHeadersRegex
      tls {
        ca
        caOptional
        cert
        insecureSkipVerify
        key
      }
      trustForwardHeader
    }
  }
`;
export const HEADERS_FRAGMENT = gql`
  fragment HeadersFragment on TraefikMiddlewareHeaders {
    headers {
      accessControlAllowCredentials
      accessControlAllowHeaders
      accessControlAllowMethods
      accessControlAllowOrigin
      accessControlAllowOriginList
      accessControlAllowOriginListRegex
      accessControlExposeHeaders
      accessControlMaxAge
      addVaryHeader
      allowedHosts
      browserXssFilter
      contentSecurityPolicy
      contentTypeNosniff
      customBrowserXSSValue
      customFrameOptionsValue
      customRequestHeaders {
        key
        value
      }
      customResponseHeaders {
        key
        value
      }
      featurePolicy
      forceSTSHeader
      frameDeny
      hostsProxyHeaders
      isDevelopment
      publicKey
      referrerPolicy
      sslForceHost
      sslHost
      sslProxyHeaders {
        key
        value
      }
      sslRedirect
      sslTemporaryRedirect
      stsIncludeSubdomains
      stsPreload
      stsSeconds
    }
  }
`;
export const IP_WHITE_LIST_FRAGMENT = gql`
  fragment IpWhiteListFragment on TraefikMiddlewareIpWhiteList {
    ipWhiteList {
      ipStrategy {
        depth
        excludedIPs
      }
      sourceRange
    }
  }
`;
export const IN_FLIGHT_REQ_FRAGMENT = gql`
  fragment InFlightReqFragment on TraefikMiddlewareInFlightReq {
    inFlightReq {
      amount
      sourceCriterion {
        ipStrategy {
          depth
          excludedIPs
        }
        requestHeaderName
        requestHost
      }
    }
  }
`;
export const PASS_TLSCLIENT_CERT_FRAGMENT = gql`
  fragment PassTLSClientCertFragment on TraefikMiddlewarePassTLSClientCert {
    passTLSClientCert {
      info {
        issuer {
          commonName
          country
          domainComponent
          locality
          organization
          province
          serialNumber
        }
        notAfter
        notBefore
        sans
        serialNumber
        subject {
          commonName
          country
          domainComponent
          locality
          organization
          province
          serialNumber
        }
      }
      pem
    }
  }
`;
export const RATE_LIMIT_FRAGMENT = gql`
  fragment RateLimitFragment on TraefikMiddlewareRateLimit {
    rateLimit {
      average
      burst
      period
      sourceCriterion {
        ipStrategy {
          depth
          excludedIPs
        }
        requestHeaderName
        requestHost
      }
    }
  }
`;
export const REDIRECT_REGEX_FRAGMENT = gql`
  fragment RedirectRegexFragment on TraefikMiddlewareRedirectRegex {
    redirectRegex {
      permanent
      regex
      replacement
    }
  }
`;
export const REDIRECT_SCHEME_FRAGMENT = gql`
  fragment RedirectSchemeFragment on TraefikMiddlewareRedirectScheme {
    redirectScheme {
      permanent
      port
      scheme
    }
  }
`;
export const REPLACE_PATH_FRAGMENT = gql`
  fragment ReplacePathFragment on TraefikMiddlewareReplacePath {
    replacePath {
      path
    }
  }
`;
export const REPLACE_PATH_REGEX_FRAGMENT = gql`
  fragment ReplacePathRegexFragment on TraefikMiddlewareReplacePathRegex {
    replacePathRegex {
      regex
      replacement
    }
  }
`;
export const RETRY_FRAGMENT = gql`
  fragment RetryFragment on TraefikMiddlewareRetry {
    retry {
      attempts
      initialInterval
    }
  }
`;
export const STRIP_PREFIX_FRAGMENT = gql`
  fragment StripPrefixFragment on TraefikMiddlewareStripPrefix {
    stripPrefix {
      forceSlash
      prefixes
    }
  }
`;
export const STRIP_PREFIX_REGEX_FRAGMENT = gql`
  fragment StripPrefixRegexFragment on TraefikMiddlewareStripPrefixRegex {
    stripPrefixRegex {
      regex
    }
  }
`;
import gql from "graphql-tag";

export const MIDDLEWARE_FRAGMENT = gql`
  fragment MiddlewareFragment on TraefikMiddleware {
    nodeId
    name
    error
    type
    enabled
    usedBy {
      nodeId
      name
    }
    ... on TraefikMiddlewareAddPrefix {
      ...AddPrefixFragment
    }
    ... on TraefikMiddlewareBasicAuth {
      ...BasicAuthFragment
    }
    ... on TraefikMiddlewareBuffering {
      ...BufferingFragment
    }
    ... on TraefikMiddlewareChain {
      ...ChainFragment
    }
    ... on TraefikMiddlewareCircuitBreaker {
      ...CircuitBreakerFragment
    }
    ... on TraefikMiddlewareCompress {
      ...CompressFragment
    }
    ... on TraefikMiddlewareContentType {
      ...ContentTypeFragment
    }
    ... on TraefikMiddlewareDigestAuth {
      ...DigestAuthFragment
    }
    ... on TraefikMiddlewareErrors {
      ...ErrorsFragment
    }
    ... on TraefikMiddlewareForwardAuth {
      ...ForwardAuthFragment
    }
    ... on TraefikMiddlewareHeaders {
      ...HeadersFragment
    }
    ... on TraefikMiddlewareIpWhiteList {
      ...IpWhiteListFragment
    }
    ... on TraefikMiddlewareInFlightReq {
      ...InFlightReqFragment
    }
    ... on TraefikMiddlewarePassTLSClientCert {
      ...PassTLSClientCertFragment
    }
    ... on TraefikMiddlewareRateLimit {
      ...RateLimitFragment
    }
    ... on TraefikMiddlewareRedirectRegex {
      ...RedirectRegexFragment
    }
    ... on TraefikMiddlewareRedirectScheme {
      ...RedirectSchemeFragment
    }
    ... on TraefikMiddlewareReplacePath {
      ...ReplacePathFragment
    }
    ... on TraefikMiddlewareReplacePathRegex {
      ...ReplacePathRegexFragment
    }
    ... on TraefikMiddlewareRetry {
      ...RetryFragment
    }
    ... on TraefikMiddlewareStripPrefix {
      ...StripPrefixFragment
    }
    ... on TraefikMiddlewareStripPrefixRegex {
      ...StripPrefixRegexFragment
    }
  }
  ${ADD_PREFIX_FRAGMENT}
  ${BASIC_AUTH_FRAGMENT}
  ${BUFFERING_FRAGMENT}
  ${CHAIN_FRAGMENT}
  ${CIRCUIT_BREAKER_FRAGMENT}
  ${COMPRESS_FRAGMENT}
  ${CONTENT_TYPE_FRAGMENT}
  ${DIGEST_AUTH_FRAGMENT}
  ${ERRORS_FRAGMENT}
  ${FORWARD_AUTH_FRAGMENT}
  ${HEADERS_FRAGMENT}
  ${IP_WHITE_LIST_FRAGMENT}
  ${IN_FLIGHT_REQ_FRAGMENT}
  ${PASS_TLSCLIENT_CERT_FRAGMENT}
  ${RATE_LIMIT_FRAGMENT}
  ${REDIRECT_REGEX_FRAGMENT}
  ${REDIRECT_SCHEME_FRAGMENT}
  ${REPLACE_PATH_FRAGMENT}
  ${REPLACE_PATH_REGEX_FRAGMENT}
  ${RETRY_FRAGMENT}
  ${STRIP_PREFIX_FRAGMENT}
  ${STRIP_PREFIX_REGEX_FRAGMENT}
`;
