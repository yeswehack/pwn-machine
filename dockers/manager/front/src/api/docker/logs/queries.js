import gql from "graphql-tag";
import { LOG_FRAGMENT } from "./fragments.js";

export const LIST_LOGS = gql`
  query listLogs($filter: DockerLogFilter, $cursor: CursorInput!) {
    dockerLogs(filter: $filter, cursor: $cursor) {
      total
      result {
        ...LogFragment
      }
    }
  }

  ${LOG_FRAGMENT}
`;
