import gql from "graphql-tag";
import { CONTAINER_FRAGMENT } from "./fragments";

export const LIST_CONTAINERS = gql`
  query listContainers($onlyRunning: Boolean = false) {
    dockerContainers(onlyRunning: $onlyRunning) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;

export const GET_CONTAINER_BY_NAME = gql`
  query GetContainerByName($name: String!) {
    dockerContainerByName(name: $name) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;
export const GET_CONTAINER_BY_ID = gql`
  query GetContainerById($id: ID!) {
    dockerContainerById(id: $id) {
      ...ContainerFragment
    }
  }
  ${CONTAINER_FRAGMENT}
`;
