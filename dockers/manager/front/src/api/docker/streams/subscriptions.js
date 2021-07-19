import gql from "graphql-tag";
import { STREAM_FRAGMENT } from "./fragments";

export const STREAM_PULL = gql`
  subscription dockerStreamPull($id: ID!) {
    dockerStreamPull(id: $id) {
      done
      status
      id
      progressDetail {
        current
        total
      }
      progress
    }
  }
`;
export const STREAM_BUILD = gql`
  subscription dockerStreamBuild($id: ID!) {
    dockerStreamBuild(id: $id) {
      done
      stream
    }
  }
`;

export const STREAM_START = gql`
  subscription dockerStreamStart {
    dockerStreamStart {
      ...StreamFragment
    }
  }
  ${STREAM_FRAGMENT}
`;
