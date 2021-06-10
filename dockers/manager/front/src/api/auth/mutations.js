import gql from "graphql-tag";

export const REFRESH_TOKEN = gql`
  mutation refreshToken($token: String!) {
    refreshToken(token: $token) {
      success
      error
      result {
        token
        isFirstRun
      }
    }
  }
`;

export const INITIALIZE_AUTH = gql`
  mutation initializeAuth($password: String!, $otp: String!) {
    initializeAuth(password: $password, otp: $otp) {
      success
      error
      result
    }
  }
`;

export const LOGIN = gql`
  mutation login($input: LoginInput!) {
    login(input: $input) {
      success
      error
      result
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

export const RESET_JWT_SECRET = gql`
  mutation resetJwtSecret {
    resetJWTSecret {
      success
      error
    }
  }
`;
