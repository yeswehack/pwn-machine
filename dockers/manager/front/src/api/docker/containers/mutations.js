import gql from "graphql-tag";
import { CONTAINER_FRAGMENT } from "./fragments";

export const START_CONTAINER = gql`
  mutation startContainer($id: ID!) {
    startDockerContainer(id: $id) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;

export const RESTART_CONTAINER = gql`
  mutation restartContainer($id: ID!) {
    restartDockerContainer(id: $id) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;

export const PAUSE_CONTAINER = gql`
  mutation pauseContainer($id: ID!) {
    pauseDockerContainer(id: $id) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;

export const UNPAUSE_CONTAINER = gql`
  mutation unpauseContainer($id: ID!) {
    unpauseDockerContainer(id: $id) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;

export const STOP_CONTAINER = gql`
  mutation stopContainer($id: ID!) {
    stopDockerContainer(id: $id) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;

export const KILL_CONTAINER = gql`
  mutation killContainer($id: ID!) {
    killDockerContainer(id: $id) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;

export const PRUNE_CONTAINERS = gql`
  mutation pruneContainers {
    pruneDockerContainers {
      deleted
      spaceReclaimed
    }
  }
`;
