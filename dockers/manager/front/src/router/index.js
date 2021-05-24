import Vue from "vue";
import VueRouter from "vue-router";

import routes from "./routes";

Vue.use(VueRouter);

Vue.mixin({
  methods: {
    async refresh() {
      const queries = Object.values(this.$apollo.queries)
      queries.forEach(q => q.refetch());
      this.$children.forEach(c => c.refresh())
    }
  }
});

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

function AuthMiddleware(store) {
  return function(to, from, next) {
    if (to.matched.some(r => r.meta.noauth)) {
      return next();
    }
    next();
    /* if (store.getters.validToken) {
      next()
    } else {
      next({ name: "login" })
    } */
  };
}

export default function({ store }) {
  const Router = new VueRouter({
    scrollBehavior: (to, from) => {
      if (to.path != from.path) {
        return { x: 0, y: 0 };
      }
      return false;
    },
    routes,

    // Leave these as they are and change in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    mode: process.env.VUE_ROUTER_MODE,
    base: process.env.VUE_ROUTER_BASE
  });

  Router.beforeEach(AuthMiddleware(store));
  return Router;
}
