
import gql from "graphql-tag";

export const logFragment = gql`
fragment logFragment on DnsLog {
  origin
  domain
  type
  time
}
`

export const ruleFragment = gql`
fragment ruleFragment on Rule {
  id
  zone
  name
  type
  ttl
  records {
    content
    enabled
  }
}`

export const soaFragment = gql`
fragment soaFragment on Soa {
          nameserver
          postmaster
          refresh
          retry
          expire
          ttl
}
`
export const dnsZoneInfoFragment = gql`
fragment dnsZoneInfoFragment on ZoneInfo {
  id
  soa {
    ...soaFragment
  }
}
${soaFragment}
`

export const zoneFragment = gql`
fragment zoneFragment on Zone {
      id
      name
      serial
      soa {
        ...soaFragment
      }
}
${soaFragment}
`