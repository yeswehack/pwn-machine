import gql from "graphql-tag";
import { SHELL_FRAGMENT } from "./fragments.js";

export const LIST_SHELLS = gql`
  query dockerContainerShells {
    dockerContainerShells {
      ...ShellFragment
    }
  }
  ${SHELL_FRAGMENT}
`;

export const GET_SHELL_BY_ID = gql`
  query dockerContainerShellById($id: ID!) {
    dockerContainerShellById(id: $id) {
      ...ShellFragment
    }
  }
  ${SHELL_FRAGMENT}
`;
