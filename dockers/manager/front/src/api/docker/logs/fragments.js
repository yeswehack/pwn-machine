import gql from "graphql-tag";

export const LOG_FRAGMENT = gql`
  fragment DockerLogFragment on DockerLog {
    nodeId
    date
    containerName
    containerId
    message
  }
`;
