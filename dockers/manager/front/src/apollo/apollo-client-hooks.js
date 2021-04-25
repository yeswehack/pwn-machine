import { ApolloLink, from } from "apollo-link";

const authLink = new ApolloLink((operation, forward) => {
  operation.setContext(({ headers = {} }) => ({
    headers: {
      ...headers,
      Authorization: "Bearer " + localStorage.getItem("token")
    }
  }));
  return forward(operation);
});

export async function apolloClientBeforeCreate({ apolloClientConfigObj }) {
  apolloClientConfigObj.link = from([authLink, apolloClientConfigObj.link]);
}

export async function apolloClientAfterCreate (/* { apolloClient, app, router, store, ssrContext, urlPath, redirect } */) {
  // if needed you can modify here the created apollo client
}
