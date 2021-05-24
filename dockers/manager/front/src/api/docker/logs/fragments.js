import gql from "graphql-tag";

export const LOG_FRAGMENT = gql`
  fragment LogFragment on DockerLog {
    nodeId
    date
    containerName
    containerId
    message
  }
`;
