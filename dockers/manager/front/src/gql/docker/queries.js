
import gql from "graphql-tag";
import { containerFragment, networkFragment } from "./fragments.js"


export const getDockerContainers = gql`
query getDockerContainers {
  docker {
    containers {
      ...containerFragment
    }
  }
}
${containerFragment}
`

export const getDockerNetworks = gql`
query getDockerNetworks {
  docker {
    networks {
      ...networkFragment
    }
  }
}
${networkFragment}
`

export const getDockerNetwork = gql`
query getNetwork($name: String!) {
  docker {
    network(name: $name) {
      id
      name
      driver
      gateway
      subnet
      connectedContainers {
        name
        ipv4
        ipv6
      }
      labels {
        key
        value
      }
    }
  }
}
`