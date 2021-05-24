<template>
  <tab-page>
    <q-route-tab
      :to="{ name: 'traefikOverview' }"
      label="Overview"
      icon="eva-eye-outline"
    />
    <q-route-tab
      :to="{ name: 'traefikEntrypoints' }"
      label="Entrypoints"
      icon="eva-log-in-outline"
    />
    <q-route-tab
      :to="{ name: 'traefikRouters' }"
      label="Routers"
      icon="eva-globe-outline"
    />
    <q-route-tab
      :to="{ name: 'traefikMiddlewares' }"
      label="Middlewares"
      icon="eva-layers"
    />
    <q-route-tab
      :to="{ name: 'traefikServices' }"
      label="Services"
      icon="eva-flash"
    />
    <q-route-tab :to="{ name: 'traefikLogs' }" label="Logs" icon="eva-list" />
  </tab-page>
</template>

<script>
import TabPage from "../components/TabPage.vue";
export default {
  components: { TabPage }
};
</script>
