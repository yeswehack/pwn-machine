import gql from "graphql-tag";
import {NETWORK_FRAGMENT} from "./fragments.js";

export const LIST_NETWORKS = gql`
  query listNetworks {
    dockerNetworks {
      ...NetworkFragment
    }
  }
  ${NETWORK_FRAGMENT}
`;
