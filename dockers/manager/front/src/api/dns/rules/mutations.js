import gql from "graphql-tag";
import { BASIC_MUTATION_FRAGMENT } from "src/api/common/fragments";

export const CREATE_RULE = gql`
  mutation createDnsRule($input: CreateDnsRuleInput!) {
    createDnsRule(input: $input) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;
export const DELETE_RULE = gql`
  mutation deleteDnsRule($nodeId: ID!) {
    deleteDnsRule(nodeId: $nodeId) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const UPDATE_RULE = gql`
  mutation updateDnsRule($nodeId: ID!, $patch: UpdateDnsRuleInput!) {
    updateDnsRule(nodeId: $nodeId, patch: $patch) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const ENABLE_RULE = gql`
  mutation enableDnsRule($nodeId: ID!, $enabled: Boolean!) {
    enableDnsRule(nodeId: $nodeId, enabled: $enabled)  {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;
