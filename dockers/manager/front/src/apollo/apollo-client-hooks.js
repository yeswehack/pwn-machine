export async function apolloClientBeforeCreate (/* { apolloClientConfigObj, app, router, store, ssrContext, urlPath, redirect } */) {
  // if needed you can modify here the config object used for apollo client
  // instantiation
}

export async function apolloClientAfterCreate (/* { apolloClient, app, router, store, ssrContext, urlPath, redirect } */) {
  // if needed you can modify here the created apollo client
}
