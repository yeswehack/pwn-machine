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

export const GET_NETWORK_BY_ID = gql`
  query getNetwork($id: ID!) {
    getDockerNetworkById(id: $id) {
      ...NetworkFragment
    }
  }
  ${NETWORK_FRAGMENT}
`;
