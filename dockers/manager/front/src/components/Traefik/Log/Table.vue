<template>
  <div class="traefik-log-table">
    <div class="row q-gutter-sm items-center">
      <div class="col">
        <q-select
          v-model="entrypoint"
          multiple
          clearable
          filled
          :options="entrypointOptions"
          label="Entrypoint"
        />
      </div>
      <div class="col">
        <q-select
          v-model="router"
          multiple
          clearable
          filled
          :options="routerOptions"
          label="Router"
        />
      </div>
      <div class="col">
        <q-select
          v-model="service"
          multiple
          clearable
          filled
          :options="serviceOptions"
          label="Service"
        />
      </div>
    </div>
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
</template>

<script>
import LogList from "src/components/Traefik/Log/LogList.vue";
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
  data: () => ({ entrypoint: [], router: [], service: [] }),
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

<style lang="scss" scope>
.traefik-log-table {
  width: 100%;
  display: grid;
  grid-template-rows: auto 1fr;
  row-gap: 14px;
}
</style>
