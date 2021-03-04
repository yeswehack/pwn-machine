import Vue from 'vue'
import Vuex from 'vuex'

import docker from './docker'
import traefik from './traefik'
import dns from './dns'

import api from "src/api.js"

Vue.use(Vuex)

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
      loading(state) { return state.loading != 0 },
      tokenExpired(state) { return state.tokenExpire && state.tokenExpire < Date.now() / 1000 },
      token(state) { return state.token },
      validToken(_, getters) { return Boolean(getters.token && !getters.tokenExpired) }
    },
    mutations: {
      startLoading(state) { state.loading += 1 },
      stopLoading(state) { state.loading -= 1 },
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
      async authenticate({ commit }, { password, otp, expire }) {
        const data = await api.auth.authenticate(password, otp, expire)
        if (!data) {
          return false
        }
        console.log(data)
        commit("setToken", data)
      }
    },

    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: process.env.DEV
  })
  api.bindStore(Store)
  return Store
}
