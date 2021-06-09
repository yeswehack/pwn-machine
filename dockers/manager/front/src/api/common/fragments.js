import gql from "graphql-tag";

export const BASIC_MUTATION_FRAGMENT = gql`
  fragment BasicMutationFragment on BasicMutationResponse {
    error
    success
  }
`;
