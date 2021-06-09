import gql from "graphql-tag";

export const CONNECTION_FRAGMENT = gql`
  fragment NetworkConnectionFragment on DockerNetworkConnection {
    ipAddress
    aliases
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
    driver
    internal
    ipams {
      ...IpamFragment
    }
    usedBy {
      ...NetworkConnectionFragment
    }
  }
  ${IPAM_FRAGMENT}
  ${CONNECTION_FRAGMENT}
`;
