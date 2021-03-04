<template>
  <TabPage :tab="tab" pathTemplate="/docker/{}">
    <template #top>
      <q-tab name="overview" label="Overview" />
      <q-tab name="images" label="Images" />
      <q-tab name="containers" label="Containers" />
      <q-tab name="networks" label="Networks" />
      <q-tab name="volumes" label="Volumes" />
      <q-space />
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
      <q-tab-panel name="overview" class="overview">
        <Overview
          v-on:refetch="refetch"
          :containers="containers"
          :networks="networks"
          :volumes="volumes"
          :images="images"
        />
      </q-tab-panel>
      <q-tab-panel name="images">
        <ImagesTable
          v-on:refetch="refetch"
          :containers="containers"
          :networks="networks"
          :volumes="volumes"
          :images="images"
        />
      </q-tab-panel>
      <q-tab-panel name="containers">
        <ContainersTable
          v-on:refetch="refetch"
          :containers="containers"
          :networks="networks"
          :volumes="volumes"
          :images="images"
        />
      </q-tab-panel>
      <q-tab-panel name="networks">
        <NetworksTable
          v-on:refetch="refetch"
          :containers="containers"
          :networks="networks"
          :volumes="volumes"
          :images="images"
      /></q-tab-panel>
      <q-tab-panel name="volumes">
        <VolumesTable
          v-on:refetch="refetch"
          :containers="containers"
          :networks="networks"
          :volumes="volumes"
          :images="images"
        />
      </q-tab-panel>
    </template>
  </TabPage>
</template>

<script>
import TabPage from "../components/TabPage.vue";
import ContainersTable from "./Docker/ContainersTable.vue";
import NetworksTable from "./Docker/NetworksTable.vue";
import ImagesTable from "./Docker/ImagesTable.vue";
import VolumesTable from "./Docker/VolumesTable.vue";
import Overview from "./Docker/Overview.vue";
import { mapGetters } from "vuex";
export default {
  // name: 'PageName',
  components: {
    TabPage,
    ContainersTable,
    NetworksTable,
    Overview,
    ImagesTable,
    VolumesTable
  },
  props: {
    tab: {
      type: String,
      default: "overview"
    }
  },
  created() {
    this.fetchData();
  },
  computed: {
    ...mapGetters("docker", ["images", "containers", "networks", "volumes"]),
    ...mapGetters(["loading"])
  },
  methods: {
    async fetchData() {
      await this.$store.dispatch("docker/fetchAll");
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
