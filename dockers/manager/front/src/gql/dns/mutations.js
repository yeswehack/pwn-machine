import gql from "graphql-tag";
import { ruleFragment, zoneFragment } from "./fragments.js"

export const createDnsRule = gql`
mutation createDnsRule(
  $zone: String!
  $name: String!
  $type: String!
  $ttl: Int!
  $records: [RecordInput!]
) {
  createDnsRule(
    rule: {
      zone: $zone
      name: $name
      type: $type
      ttl: $ttl
      records: $records
    }
  ) {
    rule {
      ...ruleFragment
    }
  }
}
${ruleFragment}
`


export const updateRecordsForDnsRule = gql`
mutation updateRecordsForDnsRule(
  $zone: String!
  $name: String!
  $type: String!
  $records: [RecordInput!]
) {
  updateRecordsForDnsRule(
    zone: $zone
    name: $name
    type: $type
    records: $records
  ) {
    rule {
      ...ruleFragment
    }
  }
}
${ruleFragment}
`

export const enableDnsRule = gql`
  mutation enableDnsRule($zone: String!, $name: String!, $type: String!) {
    enableDnsRule(zone: $zone, name: $name, type: $type) {
      rule {
        ...ruleFragment
      }
    }
  }
  ${ruleFragment}
`;

export const disableDnsRule = gql`
  mutation disableDnsRule($zone: String!, $name: String!, $type: String!) {
    disableDnsRule(zone: $zone, name: $name, type: $type) {
      rule {
        ...ruleFragment
      }
    }
  }
  ${ruleFragment}
`;

export const deleteDnsRule = gql`
  mutation deleteDnsRule($zone: String!, $name: String!, $type: String!) {
    deleteDnsRule(zone: $zone, name: $name, type: $type) {
      ok
    }
  }
`;

export const updateTLLForDnsRule = gql`
mutation updateTLLForDnsRule($zone: String!, $name: String!, $type: String!, $ttl: Int!){
  updateTTLForDnsRule(name: $name, type: $type, zone: $zone, ttl: $ttl) {
    rule {
      ...ruleFragment
    }
  }
}
${ruleFragment}
`



// {nameserver: "ns.bi.tk", postmaster:"r@oot.bi.tk", expire:0,refresh:0,retry:0,ttl:0}

export const createDnsZone = gql`
mutation createDnsZone($name: String!, $soa: SoaInput!) {
  createDnsZone(name:$name, soa: $soa) {
    zone {
      ...zoneFragment
    }
  }
}
${zoneFragment}
`

export const modifySoaForDnsZone = gql`
mutation modifySoaForDnsZone($zone: String!, $soa: SoaInput!) {
  modifySoaForDnsZone(zone:$zone, soa: $soa) {
    zone {
      ...zoneFragment
    }
  }
}
${zoneFragment}
`


export const deleteDnsZone = gql`
mutation deleteDnsZone($zone: String!) {
  deleteDnsZone(zone: $zone) {
    ok
  }
}

`