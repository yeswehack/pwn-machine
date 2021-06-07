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

export const DELETE_IMAGE = gql`
  mutation deleteDockerImage($id: ID!, $force: Boolean, $pruneParents: Boolean){
    deleteDockerImage(id: $id, force: $force, pruneParents: $pruneParents ){
      success
      error
    }
  }
`
