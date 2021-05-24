import gql from "graphql-tag";
import { CONTAINER_FRAGMENT } from "./fragments";

export const START_CONTAINER = gql`
  mutation startContainer($id: ID!) {
    dockerStartContainer(id: $id) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;

export const RESTART_CONTAINER = gql`
  mutation restartContainer($id: ID!) {
    dockerRestartContainer(id: $id) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;

export const PAUSE_CONTAINER = gql`
  mutation pauseContainer($id: ID!) {
    dockerPauseContainer(id: $id) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;

export const UNPAUSE_CONTAINER = gql`
  mutation unpauseContainer($id: ID!) {
    dockerUnpauseContainer(id: $id) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;

export const STOP_CONTAINER = gql`
  mutation stopContainer($id: ID!) {
    dockerStopContainer(id: $id) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;

export const KILL_CONTAINER = gql`
  mutation killContainer($id: ID!) {
    dockerKillContainer(id: $id) {
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
