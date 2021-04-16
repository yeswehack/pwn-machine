import Vue from 'vue'
import Vuex from 'vuex'

import docker from './docker'
import traefik from './traefik'
import dns from './dns'

import VuexORM from '@vuex-orm/core'
import VuexORMGraphQL from '@vuex-orm/plugin-graphql';

import Docker from "./models/docker/Docker.js"
import Image from "./models/docker/Image.js"

import { DefaultAdapter, ConnectionMode } from '@vuex-orm/plugin-graphql';


import api from "src/api.js"

Vue.use(Vuex)




class CustomAdapter extends DefaultAdapter {
  // Your code here

  // Example
  getConnectionMode() {
    return ConnectionMode.PLAIN
  }
}

const database = new VuexORM.Database()
database.register(Image)
database.register(Docker)
VuexORM.use(VuexORMGraphQL, {
  database,
  url: "/api",
  debug: true,
  adapter: new CustomAdapter(),
});



/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

export default function (/* { ssrContext } */) {
  const token = localStorage.getItem("token")
  const tokenExpire = parseInt(localStorage.getItem("tokenExpire"))


  const Store = new Vuex.Store({
    modules: {
      docker,
      traefik,
      dns
    },
    state: {
      loading: 0,
      token,
      tokenExpire,
    },
    getters: {
      loading(state) { return state.loading != 0  },
      tokenExpired(state) { return state.tokenExpire && state.tokenExpire < Date.now() / 1000 },
      token(state) { return state.token },
      validToken(_, getters) { return Boolean(getters.token && !getters.tokenExpired) }
    },
    mutations: {
      startLoading(state) { state.loading += 1 },
      stopLoading(state) { state.loading -= 1 },
      modLoading(state, mod) { state.loading += mod },
      setToken(state, { token, expire }) {
        localStorage.setItem("token", token)
        localStorage.setItem("tokenExpire", expire)
        state.token = token
        state.tokenExpire = expire
      },
      invalidateToken(state) {
        localStorage.removeItem("token")
        localStorage.removeItem("tokenExpire")
        state.token = null
        state.tokenExpire = null
      },
    },
    actions: {

      startLoading({ commit }) { commit("startLoading") },
      stopLoading({ commit }) { commit("stopLoading") },
      modLoading({commit}, mod) { commit("modLoading", mod) },
    },

    plugins: [VuexORM.install(database)],
    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: process.env.DEV
  })
  api.bindStore(Store)

  // DELETE ME
  window.Image = Image
  window.Docker = Docker
  return Store
}
