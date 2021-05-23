import gql from "graphql-tag";
import { SERVICE_FRAGMENT } from "./fragments.js";
export const LIST_SERVICES = gql`
  query listService {
    traefikServices {
      ...ServiceFragment
    }
  }
  ${SERVICE_FRAGMENT}
`;
