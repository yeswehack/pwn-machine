import gql from "graphql-tag";
import TraefikServiceFragment from "./ServiceFragment.graphql";

const create_http_loadbalancer = gql`
  mutation createTraefikHTTPServiceLoadBalancer($input: TraefikHTTPServiceLoadBalancerInput!) {
    createTraefikHTTPServiceLoadBalancer(input: $input) {
      ...TraefikServiceFragment
    }
  }
  ${TraefikServiceFragment}
`;

export default {
  create: {
    http: {
      loadBalancer: create_http_loadbalancer
    }
  }
};
