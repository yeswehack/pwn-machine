import gql from "graphql-tag";

export const CONNECTION_FRAGMENT = gql`
  fragment ConnectionFragment on DockerNetworkConnection {
    ipv4Address
    ipv6Address
    container {
      name
      id
    }
  }
`;
export const IPAM_FRAGMENT = gql`
  fragment IpamFragment on DockerNetworkIpam {
    subnet
    ipRange
    gateway
  }
`;

export const NETWORK_FRAGMENT = gql`
  fragment NetworkFragment on DockerNetwork {
    id
    name
    labels {
      key
      value
    }
    builtin
    created
    ipv6
    driver
    internal
    ipams {
      ...IpamFragment
    }
    usedBy {
      ...ConnectionFragment
    }
  }
  ${IPAM_FRAGMENT}
  ${CONNECTION_FRAGMENT}
`;
