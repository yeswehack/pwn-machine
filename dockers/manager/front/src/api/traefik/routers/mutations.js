import gql from "graphql-tag";
import { ROUTER_FRAGMENT } from "./fragments";

export const DELETE_ROUTER = gql`
  mutation deleteRouter($id: ID!) {
    deleteTraefikRouter(id: $id)
  }
`;

export const CREATE_ROUTER = {
  http: gql`
    mutation createHTTPRouter($input: TraefikHTTPRouterInput!) {
      createTraefikHTTPRouter(input: $input) {
        ...RouterFragment
      }
    }
    ${ROUTER_FRAGMENT}
  `,
  tcp: gql`
    mutation createTCPRouter($input: TraefikTCPRouterInput!) {
      createTraefikTCPRouter(input: $input) {
        ...RouterFragment
      }
    }
    ${ROUTER_FRAGMENT}
  `,
  udp: gql`
    mutation createUDPRouter($input: TraefikUDPRouterInput!) {
      createTraefikUDPRouter(input: $input) {
        ...RouterFragment
      }
    }
    ${ROUTER_FRAGMENT}
  `
};

export const UPDATE_ROUTER = {
  http: gql`
    mutation updateHTTPRouter($id: ID!, $patch: TraefikHTTPRouterPatch!) {
      updateTraefikHTTPRouter(id: $id, patch: $patch) {
        ...RouterFragment
      }
    }
    ${ROUTER_FRAGMENT}
  `,
  tcp: gql`
    mutation updateTCPRouter($id: ID!, $patch: TraefikTCPRouterPatch!) {
      updateTraefikTCPRouter(id: $id, patch: $patch) {
        ...RouterFragment
      }
    }
    ${ROUTER_FRAGMENT}
  `,
  udp: gql`
    mutation updateUDPRouter($id: ID!, $patch: TraefikUDPRouterPatch!) {
      updateTraefikUDPRouter(id: $id, patch: $patch) {
        ...RouterFragment
      }
    }
    ${ROUTER_FRAGMENT}
  `
};
