import gql from "graphql-tag";
import { SERVICE_FRAGMENT } from "./fragments";

export const DELETE_SERVICE = gql`
  mutation deleteService($nodeId: ID!) {
    deleteTraefikService(nodeId: $nodeId)
  }
`;

const create_http_loadbalancer = gql`
  mutation createTraefikHTTPServiceLoadBalancer(
    $input: TraefikHTTPServiceLoadBalancerInput!
  ) {
    createTraefikHTTPServiceLoadBalancer(input: $input) {
      ...ServiceFragment
    }
  }
  ${SERVICE_FRAGMENT}
`;

const create_http_weighted = gql`
  mutation createTraefikHTTPServiceWeighted(
    $input: TraefikHTTPServiceWeightedInput!
  ) {
    createTraefikHTTPServiceWeighted(input: $input) {
      ...ServiceFragment
    }
  }
  ${SERVICE_FRAGMENT}
`;

const create_http_mirroring = gql`
  mutation createTraefikHTTPServiceMirroring(
    $input: TraefikHTTPServiceMirroringInput!
  ) {
    createTraefikHTTPServiceMirroring(input: $input) {
      ...ServiceFragment
    }
  }
  ${SERVICE_FRAGMENT}
`;

const create_tcp_loadbalancer = gql`
  mutation createTraefikTCPServiceLoadBalancer(
    $input: TraefikTCPServiceLoadBalancerInput!
  ) {
    createTraefikTCPServiceLoadBalancer(input: $input) {
      ...ServiceFragment
    }
  }
  ${SERVICE_FRAGMENT}
`;

const create_tcp_weighted = gql`
  mutation createTraefikTCPServiceWeighted(
    $input: TraefikTCPServiceWeightedInput!
  ) {
    createTraefikTCPServiceWeighted(input: $input) {
      ...ServiceFragment
    }
  }
  ${SERVICE_FRAGMENT}
`;

const create_udp_loadbalancer = gql`
  mutation createTraefikUDPServiceLoadBalancer(
    $input: TraefikUDPServiceLoadBalancerInput!
  ) {
    createTraefikUDPServiceLoadBalancer(input: $input) {
      ...ServiceFragment
    }
  }
  ${SERVICE_FRAGMENT}
`;

const create_udp_weighted = gql`
  mutation createTraefikUDPServiceWeighted(
    $input: TraefikUDPServiceWeightedInput!
  ) {
    createTraefikUDPServiceWeighted(input: $input) {
      ...ServiceFragment
    }
  }
  ${SERVICE_FRAGMENT}
`;

export const CREATE_SERVICE = {
  http: {
    loadBalancer: create_http_loadbalancer,
    weighted: create_http_weighted,
    mirroring: create_http_mirroring
  },
  tcp: {
    loadBalancer: create_tcp_loadbalancer,
    weighted: create_tcp_weighted
  },
  udp: {
    loadBalancer: create_udp_loadbalancer,
    weighted: create_udp_weighted
  }
};
