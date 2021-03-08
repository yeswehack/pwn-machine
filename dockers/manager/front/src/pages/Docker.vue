<template>
  <TabPage :tab="tab" pathTemplate="/docker/{}">
    <template #top>
      <q-tab name="overview" label="Overview" icon="eva-globe-2" />
      <q-tab name="images" label="Images" icon="eva-bookmark"/>
      <q-tab name="containers" label="Containers" icon="eva-grid-outline" />
      <q-tab name="networks" label="Networks" icon="eva-globe"/>
      <q-tab name="volumes" label="Volumes" icon="eva-hard-drive"/>
    </template>
    <template #tabs>
      <q-tab-panel name="overview" class="overview">
        <Overview/>
      </q-tab-panel>
      <q-tab-panel name="images">
        <ImagesTable/>
      </q-tab-panel>
      <q-tab-panel name="containers">
        <ContainersTable/>
      </q-tab-panel>
      <q-tab-panel name="networks">
        <NetworksTable/></q-tab-panel>
      <q-tab-panel name="volumes">
        <VolumesTable/>
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
};
</script>

<style lang="scss" scoped>
.overview {
  display: flex;
  flex-direction: column;
}
</style>
