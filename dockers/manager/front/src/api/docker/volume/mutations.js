import gql from "graphql-tag";
import { VOLUME_FRAGMENT } from "./fragments.js";

export const CREATE_VOLUME = gql`
  mutation createVolume($input: DockerVolumeInput!) {
    createDockerVolume(input: $input) {
      ...VolumeFragment
    }
  }
  ${VOLUME_FRAGMENT}
`;
export const DELETE_VOLUME = gql`
  mutation deleteVolume($name: String!) {
    deleteDockerVolume(name: $name)
  }
`;

export const PRUNE_VOLUMES = gql`
  mutation pruneVolumes {
    pruneDockerVolumes {
      deleted
      spaceReclaimed
    }
  }
`;
