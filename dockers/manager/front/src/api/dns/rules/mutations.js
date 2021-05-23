import gql from "graphql-tag";
import { RULE_FRAGMENT } from "./fragments";

export const CREATE_RULE = gql`
  mutation createDnsRule($input: CreateDnsRuleInput!) {
    createDnsRule(input: $input) {
      ...RuleFragment
    }
  }
  ${RULE_FRAGMENT}
`;
export const DELETE_RULE = gql`
  mutation deleteDnsRule($nodeId: ID!) {
    deleteDnsRule(nodeId: $nodeId)
  }
`;

export const UPDATE_RULE = gql`
  mutation updateDnsRule($nodeId: ID!, $patch: UpdateDnsRuleInput!) {
    updateDnsRule(nodeId: $nodeId, patch: $patch) {
      ...RuleFragment
    }
  }
  ${RULE_FRAGMENT}
`;

export const ENABLE_RULE = gql`
  mutation enableDnsRule($nodeId: ID!, $enabled: Boolean!) {
    enableDnsRule(nodeId: $nodeId, enabled: $enabled) {
      ...RuleFragment
    }
  }
  ${RULE_FRAGMENT}
`;
