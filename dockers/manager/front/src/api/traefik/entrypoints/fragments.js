import gql from "graphql-tag";

export const ENTRYPOINT_FRAGMENT = gql`
  fragment EntrypointFragment on TraefikEntrypoint {
    name
    ip
    port
    protocol
    usedBy {
      name
      protocol
    }
  }
`;
