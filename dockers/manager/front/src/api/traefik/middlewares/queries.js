import gql from "graphql-tag";
import { MIDDLEWARE_FRAGMENT } from "./fragments";

export const LIST_MIDDLEWARES = gql`
  query GetMiddlewares {
    traefikMiddlewares {
      ...MiddlewareFragment
    }
  }
  ${MIDDLEWARE_FRAGMENT}
`;
