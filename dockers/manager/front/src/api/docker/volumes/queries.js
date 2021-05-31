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