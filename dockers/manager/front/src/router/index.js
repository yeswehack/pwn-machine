import Vue from "vue";
import VueRouter from "vue-router";

import routes from "./routes";

Vue.use(VueRouter);

Vue.mixin({
  methods: {
    async refresh() {
      const queries = Object.values(this.$apollo.queries);
      queries.forEach(q => q.refetch());
      this.$children.forEach(c => c.refresh());
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

export default new VueRouter({
  routes,

  // Leave these as they are and change in quasar.conf.js instead!
  // quasar.conf.js -> build -> vueRouterMode
  // quasar.conf.js -> build -> publicPath
  mode: process.env.VUE_ROUTER_MODE,
  base: process.env.VUE_ROUTER_BASE
});
