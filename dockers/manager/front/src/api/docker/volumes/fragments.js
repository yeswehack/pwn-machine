import gql from "graphql-tag";

export const VOLUME_FRAGMENT = gql`
fragment VolumeFragment on DockerVolume {
  name
  mountpoint
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