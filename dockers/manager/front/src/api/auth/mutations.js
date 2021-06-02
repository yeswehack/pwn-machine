import gql from "graphql-tag";

export const VALIDATE_TOKEN = gql`
  mutation validateToken($token: String!) {
    validateAuthToken(token: $token) {
      token {
        token
        expire
      }
      isFirstRun
    }
  }
`;

export const INITIALIZE_AUTH = gql`
  mutation initializeAuth($password: String!, $otp: String!) {
    initializeAuth(password: $password, otp: $otp) {
      error
      success
      result {
        token
      }
    }
  }
`;

export const LOGIN = gql`
  mutation login($password: String!, $otp: String!, $expire: Int) {
    login(password: $password, otp: $otp, expire: $expire) {
      success
      error
      result {
        token
        expire
      }
    }
  }
`;

export const UPDATE_PASSWORD = gql`
  mutation updatePassword($old: String!, $new: String!) {
    updatePassword(old: $old, new: $new) {
      success
      error
    }
  }
`;

export const UPDATE_TOTP = gql`
  mutation updateTotp($uri: String!, $totp: Int!) {
    updateAuthTotp(uri: $uri, totp: $totp)
  }
`;
