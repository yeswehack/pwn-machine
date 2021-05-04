<template>
  <div>
    <TabPage :tab="tab" path-template="/dns/{}">
      <template #top>
        <q-tab name="zones" label="Zones" icon="eva-home-outline" />
        <q-tab name="records" label="Rules" icon="eva-book" />
        <q-tab name="logs" label="Logs" icon="eva-list" />
      </template>
      <template #tabs>
        <q-tab-panel name="zones">
          <ZonesTable />
        </q-tab-panel>
        <q-tab-panel name="records">
          <RulesTable />
        </q-tab-panel>
        <q-tab-panel name="logs">
          <DNSLogs />
        </q-tab-panel>
      </template>
    </TabPage>
  </div>
</template>

<script>
import TabPage from "../components/TabPage.vue";
import ZonesTable from "./DNS/ZonesTable.vue";
import RulesTable from "./DNS/RulesTable.vue";
import DNSLogs from "./DNS/DNSLogs.vue";
export default {
  components: { TabPage, ZonesTable, RulesTable, DNSLogs },
  props: {
    tab: {
      type: String,
      default: "overview"
    }
  }
};
</script>
