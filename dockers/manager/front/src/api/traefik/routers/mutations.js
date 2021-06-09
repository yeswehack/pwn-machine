import gql from "graphql-tag";
import { BASIC_MUTATION_FRAGMENT } from "src/api/common/fragments";
export const DELETE_ROUTER = gql`
  mutation deleteRouter($id: ID!) {
    deleteTraefikRouter(id: $id) {
      ...BasicMutationFragment
    }
  }
  ${BASIC_MUTATION_FRAGMENT}
`;

export const CREATE_ROUTER = {
  http: gql`
    mutation createHTTPRouter($input: TraefikHTTPRouterInput!) {
      createTraefikHTTPRouter(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  tcp: gql`
    mutation createTCPRouter($input: TraefikTCPRouterInput!) {
      createTraefikTCPRouter(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  udp: gql`
    mutation createUDPRouter($input: TraefikUDPRouterInput!) {
      createTraefikUDPRouter(input: $input) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `
};

export const UPDATE_ROUTER = {
  http: gql`
    mutation updateHTTPRouter($id: ID!, $patch: TraefikHTTPRouterPatch!) {
      updateTraefikHTTPRouter(id: $id, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  tcp: gql`
    mutation updateTCPRouter($id: ID!, $patch: TraefikTCPRouterPatch!) {
      updateTraefikTCPRouter(id: $id, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `,
  udp: gql`
    mutation updateUDPRouter($id: ID!, $patch: TraefikUDPRouterPatch!) {
      updateTraefikUDPRouter(id: $id, patch: $patch) {
        ...BasicMutationFragment
      }
    }
    ${BASIC_MUTATION_FRAGMENT}
  `
};
