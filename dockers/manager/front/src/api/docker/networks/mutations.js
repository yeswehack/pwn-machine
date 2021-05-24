import gql from "graphql-tag";
import { NETWORK_FRAGMENT } from "./fragments.js";

export const PRUNE_NETWORKS = gql`
mutation pruneNetworks{
  pruneDockerNetworks{
    deleted
    spaceReclaimed
  }
}
`

export const CREATE_NETWORK = gql`
  mutation createNetwork($input: DockerNetworkInput!) {
    createDockerNetwork(input: $input) {
      ...NetworkFragment
    }
  }
  ${NETWORK_FRAGMENT}
`;
export const DELETE_NETWORK = gql`
  mutation deleteNetwork($id: ID!) {
    deleteDockerNetwork(id: $id)
  }
`;

export const CONNECT_TO_NETWORK = gql`
  mutation connectContainerToNetwork($input: DockerNetworkConnectionInput) {
    connectDockerContainer(input: $input)
  }
`;

export const DISCONNECT_FROM_NETWORK = gql`
  mutation disconnectContainerFromNetwork(
    $input: DockerNetworkConnectionInput
  ) {
    disconnectDockerContainer(input: $input)
  }
`;
