import gql from "graphql-tag";

export const LOG_FRAGMENT = gql`
  fragment LogFragment on TraefikLog {
    host
    origin
    status
    method
    path
    port
    protocol
    scheme
    routerName
    entrypointName
    serviceName
    time
  }
`;
