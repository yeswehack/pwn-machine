
import gql from "graphql-tag";


export const containerFragment = gql`
fragment containerFragment on Container{
  id
  name
  image {
    repository
    id
  }
  mounts {
    name
    source
    destination
    rw
  }
  connectedNetworks {
    name
  }
  exposedPorts {
    containerPort
    hostPort
    protocol
  }
  status
}
`


export const networkFragment = gql`
fragment networkFragment on Network {
  id
  name
  driver
  internal
  gateway
  subnet
  labels {
    key
    value
  }
  usedBy {
    id
    name
  }
}
`