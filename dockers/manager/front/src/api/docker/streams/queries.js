import gql from "graphql-tag";
import { STREAM_FRAGMENT } from "./fragments";

export const LIST_STREAMS = gql`
  query dockerStreams {
    dockerStreams {
      ...StreamFragment
    }
  }
  ${STREAM_FRAGMENT}
`;
