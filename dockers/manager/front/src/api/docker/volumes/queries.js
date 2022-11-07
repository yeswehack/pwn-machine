import gql from "graphql-tag";
import { VOLUME_FRAGMENT } from "./fragments.js";

export const LIST_VOLUMES = gql`
  query listVolumes {
    dockerVolumes {
      ...VolumeFragment
    }
  }
  ${VOLUME_FRAGMENT}
`;

export const EXPLORE_VOLUME = gql`
  query exploreVolume($input: DockerExploreVolumeInput!) {
    dockerExploreVolume(input: $input) {
      fullpath
      name
      ... on DockerVolumeFile {
        size
        mime
      }
      ... on DockerVolumeLink {
        target
      }
    }
  }
`;
