import gql from "graphql-tag";
import { BASIC_MUTATION_FRAGMENT } from "src/api/common/fragments";
export const DELETE_MIDDLEWARE = gql`
  mutation deleteMiddleware($nodeId: ID!) {
    deleteTraefikMiddleware(nodeId: $nodeId) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const CREATE_MIDDLEWARE = {
  addPrefix: gql`
    mutation createTraefikMiddlewareAddPrefix(
      $input: TraefikMiddlewareAddPrefixInput!
    ) {
      createTraefikMiddlewareAddPrefix(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  basicAuth: gql`
    mutation createTraefikMiddlewareBasicAuth(
      $input: TraefikMiddlewareBasicAuthInput!
    ) {
      createTraefikMiddlewareBasicAuth(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  buffering: gql`
    mutation createTraefikMiddlewareBuffering(
      $input: TraefikMiddlewareBufferingInput!
    ) {
      createTraefikMiddlewareBuffering(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  chain: gql`
    mutation createTraefikMiddlewareChain(
      $input: TraefikMiddlewareChainInput!
    ) {
      createTraefikMiddlewareChain(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  circuitBreaker: gql`
    mutation createTraefikMiddlewareCircuitBreaker(
      $input: TraefikMiddlewareCircuitBreakerInput!
    ) {
      createTraefikMiddlewareCircuitBreaker(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  compress: gql`
    mutation createTraefikMiddlewareCompress(
      $input: TraefikMiddlewareCompressInput!
    ) {
      createTraefikMiddlewareCompress(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  contentType: gql`
    mutation createTraefikMiddlewareContentType(
      $input: TraefikMiddlewareContentTypeInput!
    ) {
      createTraefikMiddlewareContentType(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  digestAuth: gql`
    mutation createTraefikMiddlewareDigestAuth(
      $input: TraefikMiddlewareDigestAuthInput!
    ) {
      createTraefikMiddlewareDigestAuth(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  errors: gql`
    mutation createTraefikMiddlewareErrors(
      $input: TraefikMiddlewareErrorsInput!
    ) {
      createTraefikMiddlewareErrors(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  forwardAuth: gql`
    mutation createTraefikMiddlewareForwardAuth(
      $input: TraefikMiddlewareForwardAuthInput!
    ) {
      createTraefikMiddlewareForwardAuth(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  headers: gql`
    mutation createTraefikMiddlewareHeaders(
      $input: TraefikMiddlewareHeadersInput!
    ) {
      createTraefikMiddlewareHeaders(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  ipWhiteList: gql`
    mutation createTraefikMiddlewareIpWhiteList(
      $input: TraefikMiddlewareIpWhiteListInput!
    ) {
      createTraefikMiddlewareIpWhiteList(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  inFlightReq: gql`
    mutation createTraefikMiddlewareInFlightReq(
      $input: TraefikMiddlewareInFlightReqInput!
    ) {
      createTraefikMiddlewareInFlightReq(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  passTLSClientCert: gql`
    mutation createTraefikMiddlewarePassTLSClientCert(
      $input: TraefikMiddlewarePassTLSClientCertInput!
    ) {
      createTraefikMiddlewarePassTLSClientCert(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  rateLimit: gql`
    mutation createTraefikMiddlewareRateLimit(
      $input: TraefikMiddlewareRateLimitInput!
    ) {
      createTraefikMiddlewareRateLimit(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  redirectRegex: gql`
    mutation createTraefikMiddlewareRedirectRegex(
      $input: TraefikMiddlewareRedirectRegexInput!
    ) {
      createTraefikMiddlewareRedirectRegex(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  redirectScheme: gql`
    mutation createTraefikMiddlewareRedirectScheme(
      $input: TraefikMiddlewareRedirectSchemeInput!
    ) {
      createTraefikMiddlewareRedirectScheme(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  replacePath: gql`
    mutation createTraefikMiddlewareReplacePath(
      $input: TraefikMiddlewareReplacePathInput!
    ) {
      createTraefikMiddlewareReplacePath(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  replacePathRegex: gql`
    mutation createTraefikMiddlewareReplacePathRegex(
      $input: TraefikMiddlewareReplacePathRegexInput!
    ) {
      createTraefikMiddlewareReplacePathRegex(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  retry: gql`
    mutation createTraefikMiddlewareRetry(
      $input: TraefikMiddlewareRetryInput!
    ) {
      createTraefikMiddlewareRetry(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  stripPrefix: gql`
    mutation createTraefikMiddlewareStripPrefix(
      $input: TraefikMiddlewareStripPrefixInput!
    ) {
      createTraefikMiddlewareStripPrefix(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  stripPrefixRegex: gql`
    mutation createTraefikMiddlewareStripPrefixRegex(
      $input: TraefikMiddlewareStripPrefixRegexInput!
    ) {
      createTraefikMiddlewareStripPrefixRegex(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `
};
export const UPDATE_MIDDLEWARE = {
  addPrefix: gql`
    mutation updateTraefikMiddlewareAddPrefix(
      $nodeId: ID!
      $patch: TraefikMiddlewareAddPrefixInfoInput!
    ) {
      updateTraefikMiddlewareAddPrefix(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  basicAuth: gql`
    mutation updateTraefikMiddlewareBasicAuth(
      $nodeId: ID!
      $patch: TraefikMiddlewareBasicAuthInfoInput!
    ) {
      updateTraefikMiddlewareBasicAuth(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  buffering: gql`
    mutation updateTraefikMiddlewareBuffering(
      $nodeId: ID!
      $patch: TraefikMiddlewareBufferingInfoInput!
    ) {
      updateTraefikMiddlewareBuffering(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  chain: gql`
    mutation updateTraefikMiddlewareChain(
      $nodeId: ID!
      $patch: TraefikMiddlewareChainInfoInput!
    ) {
      updateTraefikMiddlewareChain(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  circuitBreaker: gql`
    mutation updateTraefikMiddlewareCircuitBreaker(
      $nodeId: ID!
      $patch: TraefikMiddlewareCircuitBreakerInfoInput!
    ) {
      updateTraefikMiddlewareCircuitBreaker(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  compress: gql`
    mutation updateTraefikMiddlewareCompress(
      $nodeId: ID!
      $patch: TraefikMiddlewareCompressInfoInput!
    ) {
      updateTraefikMiddlewareCompress(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  contentType: gql`
    mutation updateTraefikMiddlewareContentType(
      $nodeId: ID!
      $patch: TraefikMiddlewareContentTypeInfoInput!
    ) {
      updateTraefikMiddlewareContentType(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  digestAuth: gql`
    mutation updateTraefikMiddlewareDigestAuth(
      $nodeId: ID!
      $patch: TraefikMiddlewareDigestAuthInfoInput!
    ) {
      updateTraefikMiddlewareDigestAuth(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  errors: gql`
    mutation updateTraefikMiddlewareErrors(
      $nodeId: ID!
      $patch: TraefikMiddlewareErrorsInfoInput!
    ) {
      updateTraefikMiddlewareErrors(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  forwardAuth: gql`
    mutation updateTraefikMiddlewareForwardAuth(
      $nodeId: ID!
      $patch: TraefikMiddlewareForwardAuthInfoInput!
    ) {
      updateTraefikMiddlewareForwardAuth(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  headers: gql`
    mutation updateTraefikMiddlewareHeaders(
      $nodeId: ID!
      $patch: TraefikMiddlewareHeadersInfoInput!
    ) {
      updateTraefikMiddlewareHeaders(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  ipWhiteList: gql`
    mutation updateTraefikMiddlewareIpWhiteList(
      $nodeId: ID!
      $patch: TraefikMiddlewareIpWhiteListInfoInput!
    ) {
      updateTraefikMiddlewareIpWhiteList(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  inFlightReq: gql`
    mutation updateTraefikMiddlewareInFlightReq(
      $nodeId: ID!
      $patch: TraefikMiddlewareInFlightReqInfoInput!
    ) {
      updateTraefikMiddlewareInFlightReq(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  passTLSClientCert: gql`
    mutation updateTraefikMiddlewarePassTLSClientCert(
      $nodeId: ID!
      $patch: TraefikMiddlewarePassTLSClientCertInfoInput!
    ) {
      updateTraefikMiddlewarePassTLSClientCert(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  rateLimit: gql`
    mutation updateTraefikMiddlewareRateLimit(
      $nodeId: ID!
      $patch: TraefikMiddlewareRateLimitInfoInput!
    ) {
      updateTraefikMiddlewareRateLimit(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  redirectRegex: gql`
    mutation updateTraefikMiddlewareRedirectRegex(
      $nodeId: ID!
      $patch: TraefikMiddlewareRedirectRegexInfoInput!
    ) {
      updateTraefikMiddlewareRedirectRegex(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  redirectScheme: gql`
    mutation updateTraefikMiddlewareRedirectScheme(
      $nodeId: ID!
      $patch: TraefikMiddlewareRedirectSchemeInfoInput!
    ) {
      updateTraefikMiddlewareRedirectScheme(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  replacePath: gql`
    mutation updateTraefikMiddlewareReplacePath(
      $nodeId: ID!
      $patch: TraefikMiddlewareReplacePathInfoInput!
    ) {
      updateTraefikMiddlewareReplacePath(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  replacePathRegex: gql`
    mutation updateTraefikMiddlewareReplacePathRegex(
      $nodeId: ID!
      $patch: TraefikMiddlewareReplacePathRegexInfoInput!
    ) {
      updateTraefikMiddlewareReplacePathRegex(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  retry: gql`
    mutation updateTraefikMiddlewareRetry(
      $nodeId: ID!
      $patch: TraefikMiddlewareRetryInfoInput!
    ) {
      updateTraefikMiddlewareRetry(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  stripPrefix: gql`
    mutation updateTraefikMiddlewareStripPrefix(
      $nodeId: ID!
      $patch: TraefikMiddlewareStripPrefixInfoInput!
    ) {
      updateTraefikMiddlewareStripPrefix(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  stripPrefixRegex: gql`
    mutation updateTraefikMiddlewareStripPrefixRegex(
      $nodeId: ID!
      $patch: TraefikMiddlewareStripPrefixRegexInfoInput!
    ) {
      updateTraefikMiddlewareStripPrefixRegex(nodeId: $nodeId, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `
};
