import gql from "graphql-tag";

export const PRUNE_IMAGES = gql`
  mutation pruneImages($onlyDangling: Boolean) {
    pruneDockerImages(onlyDangling: $onlyDangling) {
      success
      error
      result {
        deleted
        spaceReclaimed
      }
    }
  }
`;
export const PULL_IMAGE = gql`
  mutation pullDockerImage($name: String!) {
    pullDockerImage(name: $name) {
      success
      error
      result {
        id
        name
      }
    }
  }
`;
