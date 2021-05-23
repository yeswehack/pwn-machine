import gql from "graphql-tag";
import {VOLUME_FRAGMENT} from "./fragments.js";

export const LIST_VOLUMES = gql`
  query listVolumes {
    dockerVolumes {
      ...VolumeFragment
    }
  }
  ${VOLUME_FRAGMENT}
`;

export const GET_VOLUME_BY_NAME = gql`
  query getVolume($name: String!) {
    getDockerVolumeByName(name: $name) {
      ...VolumeFragment
    }
  }
  ${VOLUME_FRAGMENT}
`;
