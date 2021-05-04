<template>
  <div>
    <TabPage :tab="tab" path-template="/dns/{}">
      <template #top>
        <q-tab name="overview" label="Overview" icon="eva-globe-outline" />
        <q-tab name="zones" label="Zones" icon="eva-home-outline" />
        <q-tab name="records" label="Rules" icon="eva-book" />
        <q-tab name="logs" label="Logs" icon="eva-list" />
      </template>
      <template #tabs>
        <q-tab-panel name="overview" class="overview">
          <overview />
        </q-tab-panel>
        <q-tab-panel name="zones">
          <zones-table />
        </q-tab-panel>
        <q-tab-panel name="records">
          <rules-table />
        </q-tab-panel>
        <q-tab-panel name="logs">
          <dns-logs />
        </q-tab-panel>
      </template>
    </TabPage>
  </div>
</template>

<script>
import TabPage from "../components/TabPage.vue";
import ZonesTable from "./DNS/ZonesTable.vue";
import RulesTable from "./DNS/RulesTable.vue";
import DnsLogs from "./DNS/DNSLogs.vue";
import Overview from "./DNS/Overview.vue";
export default {
  components: { TabPage, ZonesTable, RulesTable, DnsLogs, Overview },
  props: {
    tab: {
      type: String,
      default: "overview"
    }
  }
};
</script>

<style lang="scss" scoped>
.overview {
  display: flex;
  flex-direction: column;
}
</style>