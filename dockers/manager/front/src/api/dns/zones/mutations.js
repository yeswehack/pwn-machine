import gql from "graphql-tag";
import { ZONE_FRAGMENT } from "./fragments";

export const CREATE_ZONE = gql`
  mutation createDnsZone($input: CreateDnsZoneInput!) {
    createDnsZone(input: $input) {
      ...ZoneFragment
    }
  }
  ${ZONE_FRAGMENT}
`;

export const DELETE_ZONE = gql`
  mutation deleteDnsZone($nodeId: ID!) {
    deleteDnsZone(nodeId: $nodeId)
  }
`;

export const UPDATE_ZONE = gql`
  mutation updateDnsZone($nodeId: ID!, $patch: UpdateDnsZoneInput!) {
    updateDnsZone(nodeId: $nodeId, patch: $patch) {
      ...ZoneFragment
    }
  }
`;
