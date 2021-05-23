import gql from "graphql-tag";

export const IMAGE_FRAGMENT = gql`
  fragment ImageFragment on DockerImage {
    id
    name
    tags {
      repository
      tag
    }
    labels {
      key
      value
    }
    parent
    created
    size
    entrypoint
    command
    environment {
      key
      value
    }
    usedBy(onlyRunning: false) {
      id
      name
    }
  }
`;
