import gql from "graphql-tag";

export const GET_OTP_SECRET = gql`
  query otpSecret{
    otpSecret
  }
`;
