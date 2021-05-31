import gql from "graphql-tag";

export const GET_SETUP_NEEDED = gql`
  query getSetupNeeded {
    authSetupNeeded
  }
`;

export const GET_TOTP_URI = gql`
  query getTotpUri {
    authTotpUri
  }
`;
