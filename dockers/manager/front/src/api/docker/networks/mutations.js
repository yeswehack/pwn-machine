import gql from "graphql-tag";
import { BASIC_MUTATION_FRAGMENT } from "src/api/common/fragments.js";

export const PRUNE_NETWORKS = gql`
  mutation pruneNetworks {
    pruneDockerNetworks {
      success
      error
      result {
        deleted
        spaceReclaimed
      }
    }
  }
`;

export const CREATE_NETWORK = gql`
  mutation createNetwork($input: DockerNetworkInput!) {
    createDockerNetwork(input: $input) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;
export const DELETE_NETWORK = gql`
  mutation deleteNetwork($id: ID!) {
    deleteDockerNetwork(id: $id) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const CONNECT_TO_NETWORK = gql`
  mutation connectContainerToNetwork($input: DockerNetworkConnectionInput) {
    connectDockerContainer(input: $input) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const DISCONNECT_FROM_NETWORK = gql`
  mutation disconnectContainerFromNetwork(
    $input: DockerNetworkConnectionInput
  ) {
    disconnectDockerContainer(input: $input) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;
