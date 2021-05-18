<template>
  <tab-page>
      <q-route-tab
        :to="{ name: 'dnsOverview' }"
        label="Overview"
        icon="eva-globe-outline"
      />
      <q-route-tab
        :to="{ name: 'dnsZones' }"
        label="Zones"
        icon="eva-home-outline"
      />
      <q-route-tab :to="{ name: 'dnsRules' }" label="Rules" icon="eva-book" />
      <q-route-tab :to="{ name: 'dnsLogs' }" label="Logs" icon="eva-list" />
  </tab-page>
</template>

<script>
import TabPage from "../components/TabPage.vue";
export default {
  components: { TabPage }
};
</script>
