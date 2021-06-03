import gql from "graphql-tag";
import { SHELL_FRAGMENT } from "./fragments.js";

export const SPAWN_SHELL = gql`
  mutation spawnDockerContainerShell($input: SpawnContainerShellInput!) {
    spawnDockerContainerShell(input: $input) {
      success
      error
      result {
        ...ShellFragment
      }
    }
  }
  ${SHELL_FRAGMENT}
`;
export const DELETE_SHELL = gql`
  mutation deleteDockerContainerShell($id: ID!) {
    deleteDockerContainerShell(id: $id) {
      success
      error
    }
  }
`;
