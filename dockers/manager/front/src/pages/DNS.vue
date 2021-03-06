<template>
  <div>
    <TabPage :tab="tab" pathTemplate="/dns/{}">
      <template #top>
        <q-tab name="zones" label="Zones" />
        <q-tab name="records" label="Records" />
        <q-btn
          dense
          round
          color="primary"
          size="sm"
          class="q-mx-md refresh-btn"
          :class="{ spin: loading }"
          icon="refresh"
        />
      </template>
      <template #tabs>
        <q-tab-panel name="zones">
          <ZonesTable />
        </q-tab-panel>
        <q-tab-panel name="records">
          <RecordsTable />
        </q-tab-panel>
      </template>
    </TabPage>
  </div>
</template>

<script>
import TabPage from "../components/TabPage.vue";
import ZonesTable from "./DNS/ZonesTable.vue";
import RecordsTable from "./DNS/RecordsTable.vue";
export default {
  components: { TabPage, ZonesTable, RecordsTable },
  props: {
    tab: {
      type: String,
      default: "overview"
    }
  },
  computed: {
    loading() {
      return this.$apollo.loading;
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
