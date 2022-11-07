import gql from "graphql-tag";

export const RULE_FRAGMENT = gql`
  fragment RuleFragment on DnsRule {
    nodeId
    zone
    name
    type
    ttl
    isLua
    records {
      content
      enabled
    }
  }
`;
