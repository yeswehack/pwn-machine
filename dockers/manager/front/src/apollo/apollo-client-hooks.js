import { ApolloLink, from } from "apollo-link";
import { split } from "apollo-link";
import { HttpLink } from "apollo-link-http";
import { WebSocketLink } from "apollo-link-ws";
import { getMainDefinition } from "apollo-utilities";

function createWSLink() {
  const connectionParams = {};
  const jwt = localStorage.getItem("token");
  if (jwt) {
    connectionParams.authorization = `Bearer ${jwt}`;
  }
  const wsLinkConfig = {
    uri: `${location.protocol == "https:" ? "wss" : "ws"}://${
      location.host
    }/api`,
    options: {
      reconnect: true,
      connectionParams
    }
  };

  return new WebSocketLink(wsLinkConfig);
}

function createHTTPLink() {
  return new HttpLink({
    uri: "/api"
  });
}

function createAuthLink() {
  return new ApolloLink((operation, forward) => {
    operation.setContext(({ headers = {} }) => {
      const token = localStorage.getItem("JWT");

      if (token) {
        headers = { ...headers, authorization: `Bearer ${token}` };
      }

      return { headers };
    });

    return forward(operation);
  });
}

function createTerminatingLink() {
  return split(
    ({ query }) => {
      const definition = getMainDefinition(query);
      return (
        definition.kind === "OperationDefinition" &&
        definition.operation === "subscription"
      );
    },
    createWSLink(),
    createHTTPLink()
  );
}

export async function apolloClientBeforeCreate({ apolloClientConfigObj }) {
  apolloClientConfigObj.link = from([
    createAuthLink(),
    createTerminatingLink()
  ]);
}

export async function apolloClientAfterCreate(/* { apolloClient, app, router, store, ssrContext, urlPath, redirect } */) {
  // if needed you can modify here the created apollo client
}
