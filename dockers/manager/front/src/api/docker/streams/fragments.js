import gql from "graphql-tag";

export const STREAM_FRAGMENT = gql`
fragment StreamFragment on DockerStream {
  id
  type
  name
}
`