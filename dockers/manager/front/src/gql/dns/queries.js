import gql from "graphql-tag";
import {ruleFragment, zoneFragment, logFragment} from "./fragments.js"

export const getRules = gql`
query getRules {
  dns {
    id
    rules {
      ...ruleFragment
    }
  }
}
${ruleFragment}
`

export const getZoneNames = gql`
query getZoneNames {
  dns {
    id
    zones {
      id
      name
    }
  }
}`

export const getDnsZones = gql`
query getDnsZones {
  dns {
    id
    zones {
      ...zoneFragment
    }
  }
}
${zoneFragment}
`

export const getDnsLogs = gql`
query getDnsLogs($domain: String, $type: String){
  dns {
    id
    logs(ruleName: $domain, ruleType: $type){
      ...logFragment
    }
  }
}
${logFragment}
` 