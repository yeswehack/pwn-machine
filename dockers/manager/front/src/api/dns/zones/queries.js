import gql from "graphql-tag";
import { ZONE_FRAGMENT } from "./fragments";

export const LIST_ZONES = gql`
  query getDNSZones {
    dnsZones {
      ...ZoneFragment
    }
  }
  ${ZONE_FRAGMENT}
`;
