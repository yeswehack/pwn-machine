import gql from "graphql-tag";
import { LOG_FRAGMENT } from "./fragments";

export const LIST_LOGS = gql`
  query listTraefikLogs(
    $filter: TreaefikLogFilterInput
    $cursor: CursorInput!
  ) {
    traefikLogs(filter: $filter, cursor: $cursor) {
      total
      result {
        ...TraefikLogFragment
      }
    }
  }
  ${LOG_FRAGMENT}
`;
