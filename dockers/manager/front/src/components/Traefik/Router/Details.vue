<template>
  <BaseDetails :errors="router.error">
    <template #body>
      <div class="col col-grow">
        <CreateRouter
          style="max-width: 100%"
          class="bg-dark"
          edit
          v-on:created="routerModified"
          :info="router"
          :services="services"
          :routers="routers"
          :entrypoints="entrypoints"
          v-on:type-change="typeChange"
        />
      </div>
      <div class="col col-grow" v-if="showMiddlewares">
        {{ form.middlewares }}
        <MiddlewareList :middlewares.sync="form.middlewares" />
      </div>

      <q-dialog v-model="createMiddlewareVisible">
        <CreateMiddleware
          :middlewares="middlewares"
          v-on:created="middlewareCreated"
        />
      </q-dialog>
    </template>
  </BaseDetails>
</template>

<script>
import CreateRouter from "src/components/Traefik/Router/Create.vue";
import CreateMiddleware from "src/components/Traefik/Middleware/Create.vue";
import MiddlewareList from "src/components/Traefik/Router/MiddlewareList.vue";
import BaseDetails from "src/components/Traefik/BaseDetails.vue";
export default {
  components: {
    CreateRouter,
    CreateMiddleware,
    MiddlewareList,
    BaseDetails
  },
  props: {
    router: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      form: {
        middlewares: router.middlewares ? [...router.middlewares] : [null]
      },
      createMiddlewareVisible: false,
      useChain: false,
      showMiddlewares: router.type == "http"
    };
  },
  methods: {
    reset() {
      this.form.middlewares = this.router.middlewares
        ? [...this.router.middlewares]
        : [null];
    },
    async save() {
      await this.$api.traefik.updateRouterMiddlewares(
        this.router.name.split("@")[0],
        this.form.middlewares
      );
    },
    createMiddleware() {
      this.$emit;
    },
    deleteFromChain(idx) {
      this.form.middlewares.splice(idx, 1);
    },
    addChainEntry() {
      this.form.middlewares.push(null);
    },
    middlewareCreated() {
      this.$emit("refetch");
      this.createMiddlewareVisible = false;
    },
    routerModified() {
      this.$emit("modified");
    },
    typeChange(t) {
      this.showMiddlewares = t == "http";
    }
  }
};
</script>
