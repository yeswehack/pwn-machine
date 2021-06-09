import gql from "graphql-tag";
import { ENTRYPOINT_FRAGMENT } from "./fragments";

export const LIST_ENTRYPOINTS = gql`
  query listEntrypoints {
    traefikEntrypoints {
      ...EntrypointFragment
    }
  }
  ${ENTRYPOINT_FRAGMENT}
`;
