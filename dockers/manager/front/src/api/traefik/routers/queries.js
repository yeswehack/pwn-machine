import gql from "graphql-tag";
import { ROUTER_FRAGMENT } from "./fragments.js";

export const LIST_ROUTERS = gql`
  query GetRouters {
    traefikRouters {
      ...RouterFragment
    }
  }
  ${ROUTER_FRAGMENT}
`;
