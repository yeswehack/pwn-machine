import gql from "graphql-tag";
import { BASIC_MUTATION_FRAGMENT } from "src/api/common/fragments.js";
import { VOLUME_FRAGMENT } from "./fragments.js";

export const CREATE_VOLUME = gql`
  mutation createVolume($input: DockerVolumeInput!) {
    createDockerVolume(input: $input) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;
export const DELETE_VOLUME = gql`
  mutation deleteVolume($name: String!) {
    deleteDockerVolume(name: $name) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const PRUNE_VOLUMES = gql`
  mutation pruneVolumes {
    pruneDockerVolumes {
      success
      error
      result {
        deleted
        spaceReclaimed
      }
    }
  }
`;


export const DELETE_FILE = gql`
mutation deleteDockerVolumeFile($input: DeleteDockerVolumeFileInput!){
  deleteDockerVolumeFile(input:$input){
    success
    error
  }
}
`