<template>
  <div class="full-width column q-col-gutter-md">
    <div class="col col-auto">
      <div class="row q-gutter-sm items-center">
        <div class="col">
          <q-select
            clearable
            filled
            :options="entrypointOptions"
            v-model="entrypoint"
            label="Entrypoint"
          />
        </div>
        <div class="col">
          <q-select
            clearable
            filled
            :options="routerOptions"
            v-model="router"
            label="Router"
          />
        </div>
        <div class="col">
          <q-select
            clearable
            filled
            :options="serviceOptions"
            v-model="service"
            label="Service"
          />
        </div>
      </div>
    </div>
    <div class="col full-width">
      <log-list
        bordered
        flat
        :rows-per-page="20"
        hide-title
        :entrypoint="entrypoint"
        :service="service"
        :router="router"
      />
    </div>
  </div>
</template>

<script>
import LogList from "src/components/Traefik/LogList.vue";
import api from "src/api";
export default {
  components: { LogList },
  apollo: {
    traefikEntrypoints: {
      query: api.traefik.entrypoints.LIST_ENTRYPOINTS
    },
    traefikRouters: {
      query: api.traefik.routers.LIST_ROUTERS
    },
    traefikServices: {
      query: api.traefik.services.LIST_SERVICES
    }
  },
  data() {
    return {
      entrypoint: null,
      router: null,
      service: null
    };
  },
  computed: {
    entrypointOptions() {
      return (this.traefikEntrypoints ?? []).map(x => x.name);
    },
    routerOptions() {
      return (this.traefikRouters ?? []).map(x => x.name);
    },
    serviceOptions() {
      return (this.traefikServices ?? []).map(x => x.name);
    }
  }
};
</script>

<style></style>
