import gql from "graphql-tag";

export const SHELL_FRAGMENT = gql`
fragment ShellFragment on DockerContainerShell {
  nodeId
  containerName
  running
}
`