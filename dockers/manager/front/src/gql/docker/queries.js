
import gql from "graphql-tag";
import { containerFragment, networkFragment } from "./fragments.js"


export const getDockerContainers = gql`
query getDockerContainers {
  docker {
    id
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
    id
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
    id
    network(name: $name) {
      ...networkFragment
      connectedContainers {
        name
        ipv4
        ipv6
      }
    }
  }
}
${networkFragment}
`
