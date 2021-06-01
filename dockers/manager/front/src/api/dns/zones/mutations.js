import gql from "graphql-tag";
import { BASIC_MUTATION_FRAGMENT } from "src/api/common/fragments";

export const CREATE_ZONE = gql`
  mutation createDnsZone($input: CreateDnsZoneInput!) {
    createDnsZone(input: $input) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;


export const DELETE_ZONE = gql`
  mutation deleteDnsZone($nodeId: ID!) {
    deleteDnsZone(nodeId: $nodeId) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const UPDATE_ZONE = gql`
  mutation updateDnsZone($nodeId: ID!, $patch: UpdateDnsZoneInput!) {
    updateDnsZone(nodeId: $nodeId, patch: $patch) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;
