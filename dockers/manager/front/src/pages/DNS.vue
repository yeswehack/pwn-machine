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
        @click="fetchData"
        class="q-mx-md refresh-btn"
        :class="{ spin: loading }"
        icon="refresh"
      />
    </template>
    <template #tabs>
      <q-tab-panel name="zones">
        <ZonesTable
          v-on:refetch="refetch"
          :loading="loading"
          :zones="zones"
          :records="records"
        />
      </q-tab-panel>
      <q-tab-panel name="records">
        <RecordsTable
          v-on:refetch="refetch"
          :loading="loading"
          :zones="zones"
          :records="records"
        />
      </q-tab-panel>
    </template>
  </TabPage>
  </div>
</template>

<script>
import TabPage from "../components/TabPage.vue";
import ZonesTable from "./DNS/ZonesTable.vue";
import RecordsTable from "./DNS/RecordsTable.vue";
import { mapGetters } from "vuex";
export default {
  components: { TabPage, ZonesTable, RecordsTable },
  props: {
    tab: {
      type: String,
      default: "overview"
    }
  },
  created() {
    this.fetchData();
  },
  data() {

    return {
      loading: true,
      entrypoints: [],
    };
  },
  computed: {
    ...mapGetters("dns", ["zones", "records"]),
  },
  methods: {
    async fetchData() {
      await this.$store.dispatch("dns/fetchAll");
    },
    refetch() {
      window.setTimeout(() => this.fetchData(), 1000);
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
