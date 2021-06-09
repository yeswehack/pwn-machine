import gql from "graphql-tag";

export const SOA_FRAGMENT = gql`
  fragment SoaFragment on DnsStartOfAuthority {
    nameserver
    postmaster
    refresh
    retry
    expire
    ttl
  }
`;

export const ZONE_FRAGMENT = gql`
  fragment ZoneFragment on DnsZone {
    name
    serial
    nodeId
    soa {
      ...SoaFragment
    }
  }
  ${SOA_FRAGMENT}
`;
