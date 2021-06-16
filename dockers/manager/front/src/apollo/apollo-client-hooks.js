import { ApolloLink, split, from } from "apollo-link";
import { HttpLink } from "apollo-link-http";
import { WebSocketLink } from "apollo-link-ws";
import { getMainDefinition } from "apollo-utilities";
import { onError } from "apollo-link-error";
import { Notify } from "quasar";
import router from "src/router";
import Config from "src/config";


function withAuthToken(params = {}) {
  const token = localStorage.getItem("token");
  if (token) {
    params[Config.AuthenticationHeader] = `Bearer ${token}`;
  }
  return params;
}

const AuthLink = new ApolloLink((operation, forward) => {
  operation.setContext(({ headers = {} }) => ({
    headers: withAuthToken(headers)
  }));
  return forward(operation);
});

const ErrorLink = onError(({ graphQLErrors = [] }) => {
  graphQLErrors.forEach(({ message }) => {
    if (message === "Unauthorized") {
      router.push("/login");
    }
    Notify.create({
      message,
      color: "negative",
      position: "top"
    });
  });
});

const WSLink = new WebSocketLink({
  uri: `${location.protocol.replace("http", "ws")}//${location.host}/api`,
  options: {
    reconnect: true,
    connectionParams: withAuthToken
  }
});

const HTTPLink = new HttpLink({ uri: "/api" });

const TerminatingLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === "OperationDefinition" &&
      definition.operation === "subscription"
    );
  },
  WSLink,
  HTTPLink
);

export function apolloClientBeforeCreate({ apolloClientConfigObj }) {
  apolloClientConfigObj.link = from([AuthLink, ErrorLink, TerminatingLink]);
}

export async function apolloClientAfterCreate(/* { apolloClient, app, router, store, ssrContext, urlPath, redirect } */) {
  // if needed you can modify here the created apollo client
}
