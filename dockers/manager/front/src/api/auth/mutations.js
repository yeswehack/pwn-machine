import gql from "graphql-tag";

export const CREATE_TOKEN = gql`
  mutation createToken($password: String!, $totp: Int!, $expire: Int) {
    createAuthToken(password: $password, totp: $totp, expire: $expire) {
      token
      expire
    }
  }
`;

export const REFRESH_TOKEN = gql`
  mutation refreshToken($token: String!, $expire: Int) {
    refreshAuthToken(token: $token, expire: $expire) {
      token
      expire
    }
  }
`;

export const UPDATE_PASSWORD = gql`
  mutation updatePassword($password: String!) {
    updateAuthPassword(password: $password)
  }
`;

export const UPDATE_TOTP = gql`
  mutation updateTotp($uri: String!, $totp: Int!) {
    updateAuthTotp(uri: $uri, totp: $totp)
  }
`;
