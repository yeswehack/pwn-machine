import gql from "graphql-tag";

export const HEALTH_CHECK_FRAGMENT = gql`
  fragment HealthCheckFragment on TraefikServiceLoadBalancerHealthCheck {
    followRedirects
    headers {
      key
      value
    }
    hostname
    interval
    path
    port
    scheme
    timeout
  }
`;

export const STICKY_FRAGMENT = gql`
  fragment StickyFragment on TraefikHTTPSticky {
    cookie {
      httpOnly
      name
      sameSite
      secure
    }
  }
`;

export const HTTP_LOADBALANCER_FRAGMENT = gql`
  fragment HttpLoadbalancerFragment on TraefikHTTPServiceLoadBalancer {
    loadBalancer {
      healthCheck {
        ...HealthCheckFragment
      }
      passHostHeader
      responseForwarding {
        flushInterval
      }
      servers {
        url
      }
      serversTransport
      sticky {
        ...StickyFragment
      }
    }
  }
  ${HEALTH_CHECK_FRAGMENT}
  ${STICKY_FRAGMENT}
`;

export const HTTP_MIRRORING_FRAGMENT = gql`
  fragment HttpMirroringFragment on TraefikHTTPServiceMirroring {
    mirroring {
      maxBodySize
      mirrors {
        name
        percent
      }
    }
  }
`;

export const HTTP_WEIGHTED_FRAGMENT = gql`
  fragment HttpWeightedFragment on TraefikHTTPServiceWeighted {
    weighted {
      services {
        name
        weight
      }
      sticky {
        ...StickyFragment
      }
    }
  }
  ${STICKY_FRAGMENT}
`;

export const TCP_LOADBALANCER_FRAGMENT = gql`
  fragment TcpLoadbalancerFragment on TraefikTCPServiceLoadBalancer {
    loadBalancer {
      proxyProtocol {
        version
      }
      servers {
        address
      }
      terminationDelay
    }
  }
`;

export const UDP_LOADBALANCER_FRAGMENT = gql`
  fragment UdpLoadbalancerFragment on TraefikUDPServiceLoadBalancer {
    loadBalancer {
      servers {
        address
      }
    }
  }
`;

export const WEIGHTED_FRAGMENT = gql`
  fragment WeightedFragment on TraefikServiceWeighted {
    weighted {
      services {
        name
        weight
      }
    }
  }
`;

export const SERVICE_FRAGMENT = gql`
  fragment ServiceFragment on TraefikService {
    name
    nodeId
    protocol
    type
    enabled
    usedBy {
      name
    }
    ... on TraefikHTTPServiceLoadBalancer {
      ...HttpLoadbalancerFragment
    }
    ... on TraefikHTTPServiceMirroring {
      ...HttpMirroringFragment
    }
    ... on TraefikHTTPServiceWeighted {
      ...HttpWeightedFragment
    }
    ... on TraefikTCPServiceLoadBalancer {
      ...TcpLoadbalancerFragment
    }
    ... on TraefikUDPServiceLoadBalancer {
      ...UdpLoadbalancerFragment
    }
    ... on TraefikServiceWeighted {
      ...WeightedFragment
    }
  }
  ${HTTP_LOADBALANCER_FRAGMENT}
  ${HTTP_MIRRORING_FRAGMENT}
  ${HTTP_WEIGHTED_FRAGMENT}
  ${TCP_LOADBALANCER_FRAGMENT}
  ${UDP_LOADBALANCER_FRAGMENT}
  ${WEIGHTED_FRAGMENT}
`;
