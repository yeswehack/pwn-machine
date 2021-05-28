import gql from "graphql-tag";

export const PULL_IMAGE_SUBSCRIBE = gql`
  subscription pullImageProgress($id: ID!) {
    pullImageProgress(id: $id) {
      status
      id
      progressDetail {
        current
        total
      }
      progress
    }
  }
`;
