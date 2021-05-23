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

export const CREATE_SERVICE = {
  http: {
    loadBalancer: create_http_loadbalancer
  }
};
