import gql from "graphql-tag";
import { RULE_FRAGMENT } from "./fragments.js";

export const LIST_RULES = gql`
  query getDNSRules {
    dnsRules {
      ...RuleFragment
    }
  }
  ${RULE_FRAGMENT}
`;
