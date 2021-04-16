import gql from 'graphql-tag';

export const login = gql`
  mutation login($password: String!, $otp: Int!, $expire: Int) {
    login(password: $password, otp: $otp, expire: $expire) {
      token
    }
  }
`
