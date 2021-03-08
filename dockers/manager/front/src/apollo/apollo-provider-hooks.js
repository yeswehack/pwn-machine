


import Vue from "vue"

let loading = 0;
Vue.mixin({
  computed: {
      isGlobalLoading(){
        return loading
      }
  }
})

export async function apolloProviderBeforeCreate({ apolloProviderConfigObj, store }) {
  apolloProviderConfigObj["watchLoading"] = (isLoading, countModifier) => {
    loading += countModifier
    window.s = store
    store.dispatch("modLoading", countModifier)
    console.log('Global loading', loading, countModifier)
  }
}

export async function apolloProviderAfterCreate(/* { apolloProvider, app, router, store, ssrContext, urlPath, redirect } */) {
  // if needed you can modify here the created apollo provider
}
