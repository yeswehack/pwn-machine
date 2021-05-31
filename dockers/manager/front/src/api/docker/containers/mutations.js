import gql from "graphql-tag";
import { CONTAINER_FRAGMENT } from "./fragments";

export const CREATE_CONTAINER = gql`
  mutation createContainer($input: DockerContainerInput!) {
    createDockerContainer(input: $input) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;

export const START_CONTAINER = gql`
  mutation startContainer($id: ID!) {
    startDockerContainer(id: $id)
  }
`;

export const RESTART_CONTAINER = gql`
  mutation restartContainer($id: ID!) {
    restartDockerContainer(id: $id)
  }
`;

export const PAUSE_CONTAINER = gql`
  mutation pauseContainer($id: ID!) {
    pauseDockerContainer(id: $id)
  }
`;

export const UNPAUSE_CONTAINER = gql`
  mutation unpauseContainer($id: ID!) {
    unpauseDockerContainer(id: $id)
  }
`;

export const STOP_CONTAINER = gql`
  mutation stopContainer($id: ID!) {
    stopDockerContainer(id: $id)
  }
`;

export const KILL_CONTAINER = gql`
  mutation killContainer($id: ID!) {
    killDockerContainer(id: $id)
  }
`;

export const DELETE_CONTAINER = gql`
  mutation deleteDockerContainer(
    $id: ID!
    $force: Boolean
    $pruneVolumes: Boolean
  ) {
    deleteDockerContainer(id: $id, force: $force, pruneVolumes: $pruneVolumes)
  }
`;

export const PRUNE_CONTAINERS = gql`
  mutation pruneContainers {
    pruneDockerContainers {
      deleted
      spaceReclaimed
    }
  }
`;
