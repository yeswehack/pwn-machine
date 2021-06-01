import gql from "graphql-tag";
import { BASIC_MUTATION_FRAGMENT } from "src/api/common/fragments";

export const CREATE_CONTAINER = gql`
  mutation createContainer($input: DockerContainerInput!) {
    createDockerContainer(input: $input) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const START_CONTAINER = gql`
  mutation startContainer($id: ID!) {
    startDockerContainer(id: $id) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const RESTART_CONTAINER = gql`
  mutation restartContainer($id: ID!) {
    restartDockerContainer(id: $id) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const PAUSE_CONTAINER = gql`
  mutation pauseContainer($id: ID!) {
    pauseDockerContainer(id: $id) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const UNPAUSE_CONTAINER = gql`
  mutation unpauseContainer($id: ID!) {
    unpauseDockerContainer(id: $id) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const STOP_CONTAINER = gql`
  mutation stopContainer($id: ID!) {
    stopDockerContainer(id: $id) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const KILL_CONTAINER = gql`
  mutation killContainer($id: ID!) {
    killDockerContainer(id: $id) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const DELETE_CONTAINER = gql`
  mutation deleteDockerContainer(
    $id: ID!
    $force: Boolean
    $pruneVolumes: Boolean
  ) {
    deleteDockerContainer(id: $id, force: $force, pruneVolumes: $pruneVolumes) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const PRUNE_CONTAINERS = gql`
  mutation pruneContainers {
    pruneDockerContainers {
      deleted
      spaceReclaimed
    }
  }
`;
