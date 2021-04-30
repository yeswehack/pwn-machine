import gql from "graphql-tag"
import traefikMiddlewareFragment from "./MiddlewareFragment.graphql"

const create = {}
const update = {}

create['addPrefix'] = gql`
mutation createTraefikMiddlewareAddPrefix($input: TraefikMiddlewareAddPrefixInput!) {
  createTraefikMiddlewareAddPrefix(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['addPrefix'] = gql`
mutation updateTraefikMiddlewareAddPrefix($nodeId: ID!, $patch: TraefikMiddlewareAddPrefixInfoInput!) {
  updateTraefikMiddlewareAddPrefix(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['basicAuth'] = gql`
mutation createTraefikMiddlewareBasicAuth($input: TraefikMiddlewareBasicAuthInput!) {
  createTraefikMiddlewareBasicAuth(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['basicAuth'] = gql`
mutation updateTraefikMiddlewareBasicAuth($nodeId: ID!, $patch: TraefikMiddlewareBasicAuthInfoInput!) {
  updateTraefikMiddlewareBasicAuth(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['buffering'] = gql`
mutation createTraefikMiddlewareBuffering($input: TraefikMiddlewareBufferingInput!) {
  createTraefikMiddlewareBuffering(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['buffering'] = gql`
mutation updateTraefikMiddlewareBuffering($nodeId: ID!, $patch: TraefikMiddlewareBufferingInfoInput!) {
  updateTraefikMiddlewareBuffering(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['chain'] = gql`
mutation createTraefikMiddlewareChain($input: TraefikMiddlewareChainInput!) {
  createTraefikMiddlewareChain(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['chain'] = gql`
mutation updateTraefikMiddlewareChain($nodeId: ID!, $patch: TraefikMiddlewareChainInfoInput!) {
  updateTraefikMiddlewareChain(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['circuitBreaker'] = gql`
mutation createTraefikMiddlewareCircuitBreaker($input: TraefikMiddlewareCircuitBreakerInput!) {
  createTraefikMiddlewareCircuitBreaker(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['circuitBreaker'] = gql`
mutation updateTraefikMiddlewareCircuitBreaker($nodeId: ID!, $patch: TraefikMiddlewareCircuitBreakerInfoInput!) {
  updateTraefikMiddlewareCircuitBreaker(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['compress'] = gql`
mutation createTraefikMiddlewareCompress($input: TraefikMiddlewareCompressInput!) {
  createTraefikMiddlewareCompress(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['compress'] = gql`
mutation updateTraefikMiddlewareCompress($nodeId: ID!, $patch: TraefikMiddlewareCompressInfoInput!) {
  updateTraefikMiddlewareCompress(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['contentType'] = gql`
mutation createTraefikMiddlewareContentType($input: TraefikMiddlewareContentTypeInput!) {
  createTraefikMiddlewareContentType(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['contentType'] = gql`
mutation updateTraefikMiddlewareContentType($nodeId: ID!, $patch: TraefikMiddlewareContentTypeInfoInput!) {
  updateTraefikMiddlewareContentType(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['digestAuth'] = gql`
mutation createTraefikMiddlewareDigestAuth($input: TraefikMiddlewareDigestAuthInput!) {
  createTraefikMiddlewareDigestAuth(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['digestAuth'] = gql`
mutation updateTraefikMiddlewareDigestAuth($nodeId: ID!, $patch: TraefikMiddlewareDigestAuthInfoInput!) {
  updateTraefikMiddlewareDigestAuth(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['errors'] = gql`
mutation createTraefikMiddlewareErrors($input: TraefikMiddlewareErrorsInput!) {
  createTraefikMiddlewareErrors(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['errors'] = gql`
mutation updateTraefikMiddlewareErrors($nodeId: ID!, $patch: TraefikMiddlewareErrorsInfoInput!) {
  updateTraefikMiddlewareErrors(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['forwardAuth'] = gql`
mutation createTraefikMiddlewareForwardAuth($input: TraefikMiddlewareForwardAuthInput!) {
  createTraefikMiddlewareForwardAuth(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['forwardAuth'] = gql`
mutation updateTraefikMiddlewareForwardAuth($nodeId: ID!, $patch: TraefikMiddlewareForwardAuthInfoInput!) {
  updateTraefikMiddlewareForwardAuth(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['headers'] = gql`
mutation createTraefikMiddlewareHeaders($input: TraefikMiddlewareHeadersInput!) {
  createTraefikMiddlewareHeaders(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['headers'] = gql`
mutation updateTraefikMiddlewareHeaders($nodeId: ID!, $patch: TraefikMiddlewareHeadersInfoInput!) {
  updateTraefikMiddlewareHeaders(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['ipWhiteList'] = gql`
mutation createTraefikMiddlewareIpWhiteList($input: TraefikMiddlewareIpWhiteListInput!) {
  createTraefikMiddlewareIpWhiteList(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['ipWhiteList'] = gql`
mutation updateTraefikMiddlewareIpWhiteList($nodeId: ID!, $patch: TraefikMiddlewareIpWhiteListInfoInput!) {
  updateTraefikMiddlewareIpWhiteList(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['inFlightReq'] = gql`
mutation createTraefikMiddlewareInFlightReq($input: TraefikMiddlewareInFlightReqInput!) {
  createTraefikMiddlewareInFlightReq(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['inFlightReq'] = gql`
mutation updateTraefikMiddlewareInFlightReq($nodeId: ID!, $patch: TraefikMiddlewareInFlightReqInfoInput!) {
  updateTraefikMiddlewareInFlightReq(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['passTLSClientCert'] = gql`
mutation createTraefikMiddlewarePassTLSClientCert($input: TraefikMiddlewarePassTLSClientCertInput!) {
  createTraefikMiddlewarePassTLSClientCert(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['passTLSClientCert'] = gql`
mutation updateTraefikMiddlewarePassTLSClientCert($nodeId: ID!, $patch: TraefikMiddlewarePassTLSClientCertInfoInput!) {
  updateTraefikMiddlewarePassTLSClientCert(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['rateLimit'] = gql`
mutation createTraefikMiddlewareRateLimit($input: TraefikMiddlewareRateLimitInput!) {
  createTraefikMiddlewareRateLimit(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['rateLimit'] = gql`
mutation updateTraefikMiddlewareRateLimit($nodeId: ID!, $patch: TraefikMiddlewareRateLimitInfoInput!) {
  updateTraefikMiddlewareRateLimit(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['redirectRegex'] = gql`
mutation createTraefikMiddlewareRedirectRegex($input: TraefikMiddlewareRedirectRegexInput!) {
  createTraefikMiddlewareRedirectRegex(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['redirectRegex'] = gql`
mutation updateTraefikMiddlewareRedirectRegex($nodeId: ID!, $patch: TraefikMiddlewareRedirectRegexInfoInput!) {
  updateTraefikMiddlewareRedirectRegex(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['redirectScheme'] = gql`
mutation createTraefikMiddlewareRedirectScheme($input: TraefikMiddlewareRedirectSchemeInput!) {
  createTraefikMiddlewareRedirectScheme(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['redirectScheme'] = gql`
mutation updateTraefikMiddlewareRedirectScheme($nodeId: ID!, $patch: TraefikMiddlewareRedirectSchemeInfoInput!) {
  updateTraefikMiddlewareRedirectScheme(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['replacePath'] = gql`
mutation createTraefikMiddlewareReplacePath($input: TraefikMiddlewareReplacePathInput!) {
  createTraefikMiddlewareReplacePath(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['replacePath'] = gql`
mutation updateTraefikMiddlewareReplacePath($nodeId: ID!, $patch: TraefikMiddlewareReplacePathInfoInput!) {
  updateTraefikMiddlewareReplacePath(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['replacePathRegex'] = gql`
mutation createTraefikMiddlewareReplacePathRegex($input: TraefikMiddlewareReplacePathRegexInput!) {
  createTraefikMiddlewareReplacePathRegex(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['replacePathRegex'] = gql`
mutation updateTraefikMiddlewareReplacePathRegex($nodeId: ID!, $patch: TraefikMiddlewareReplacePathRegexInfoInput!) {
  updateTraefikMiddlewareReplacePathRegex(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['retry'] = gql`
mutation createTraefikMiddlewareRetry($input: TraefikMiddlewareRetryInput!) {
  createTraefikMiddlewareRetry(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['retry'] = gql`
mutation updateTraefikMiddlewareRetry($nodeId: ID!, $patch: TraefikMiddlewareRetryInfoInput!) {
  updateTraefikMiddlewareRetry(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['stripPrefix'] = gql`
mutation createTraefikMiddlewareStripPrefix($input: TraefikMiddlewareStripPrefixInput!) {
  createTraefikMiddlewareStripPrefix(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['stripPrefix'] = gql`
mutation updateTraefikMiddlewareStripPrefix($nodeId: ID!, $patch: TraefikMiddlewareStripPrefixInfoInput!) {
  updateTraefikMiddlewareStripPrefix(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

create['stripPrefixRegex'] = gql`
mutation createTraefikMiddlewareStripPrefixRegex($input: TraefikMiddlewareStripPrefixRegexInput!) {
  createTraefikMiddlewareStripPrefixRegex(input: $input){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`
update['stripPrefixRegex'] = gql`
mutation updateTraefikMiddlewareStripPrefixRegex($nodeId: ID!, $patch: TraefikMiddlewareStripPrefixRegexInfoInput!) {
  updateTraefikMiddlewareStripPrefixRegex(nodeId: $nodeId, patch: $patch){
    ... TraefikMiddlewareFragment
  }
}
${traefikMiddlewareFragment}
`

export default {create, update};
