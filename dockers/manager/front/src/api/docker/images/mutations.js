import gql from "graphql-tag";

export const PRUNE_IMAGES = gql`
  mutation pruneImages($onlyDangling: Boolean) {
    pruneDockerImages(onlyDangling: $onlyDangling) {
      deleted
      spaceReclaimed
    }
  }
`;
