import gql from "graphql-tag";
export const HTTP_ROUTER_FRAGMENT = gql`
  fragment HttpRouterFragment on TraefikHTTPRouter {
    middlewares {
      name
      type
    }
    priority
    rule
  }
`;

export const ROUTER_FRAGMENT = gql`
  fragment RouterFragment on TraefikRouter {
    name
    nodeId
    entryPoints {
      nodeId
      name
    }
    error
    service {
      nodeId
      name
    }
    ... on TraefikHTTPRouter {
      ...HttpRouterFragment
    }
    enabled
    protocol
    provider
  }
  ${HTTP_ROUTER_FRAGMENT}
`;
