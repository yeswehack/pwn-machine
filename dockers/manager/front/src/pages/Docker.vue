<template>
  <tab-page>
      <q-route-tab :to="{name: 'dockerOverview'}" label="Overview" icon="eva-globe-2" />
      <q-route-tab :to="{name: 'dockerImages'}" label="Images" icon="eva-bookmark"/>
      <q-route-tab :to="{name: 'dockerContainers'}" label="Containers" icon="eva-grid-outline" />
      <q-route-tab :to="{name: 'dockerNetworks'}" label="Networks" icon="eva-globe"/>
      <q-route-tab :to="{name: 'dockerVolumes'}" label="Volumes" icon="eva-hard-drive"/>
  </tab-page>
</template>

<script>
import TabPage from "../components/TabPage.vue";
export default {
  components: {
    TabPage,
  },
};
</script>