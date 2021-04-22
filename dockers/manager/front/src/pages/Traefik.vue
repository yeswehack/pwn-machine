<template>
  <TabPage :tab="tab" path-template="/traefik/{}">
    <template #top>
      <q-tab name="overview" label="Overview" icon="eva-eye-outline" />
      <q-tab name="entrypoints" label="Entrypoints" icon="eva-log-in-outline" />
      <q-tab name="routers" label="Routers" icon="eva-globe-outline" />
      <q-tab name="middlewares" label="Middlewares" icon="eva-layers" />
      <q-tab name="services" label="Services" icon="eva-flash" />
    </template>
    <template #tabs>
      <q-tab-panel name="overview" class="overview">
        <Overview />
      </q-tab-panel>
      <q-tab-panel name="entrypoints">
        <entrypoint-table />
      </q-tab-panel>
      <q-tab-panel name="routers">
        <routers-table />
      </q-tab-panel>
      <q-tab-panel name="middlewares">
        <middleware-table />
      </q-tab-panel>
      <q-tab-panel name="services">
        <service-table />
      </q-tab-panel>
    </template>
  </TabPage>
</template>

<script>
import { mapGetters } from "vuex";
import TabPage from "../components/TabPage.vue";
import RoutersTable from "./Traefik/RoutersTable.vue";
import ServiceTable from "./Traefik/ServiceTable.vue";
import MiddlewareTable from "./Traefik/MiddlewareTable.vue";
import Overview from "./Traefik/Overview.vue";
import db from "src/gql";
import EntrypointTable from "./Traefik/EntrypointTable.vue";
export default {
  // name: 'PageName',
  components: {
    TabPage,
    RoutersTable,
    ServiceTable,
    EntrypointTable,
    MiddlewareTable,
    Overview
  },
  props: {
    tab: {
      type: String,
      default: "overview"
    }
  },
  created() {
    //this.fetchData();
  },
  data() {
    return {
      createRouterVisible: false
    };
  },
  computed: {
    ...mapGetters("traefik", ["entrypoints", "services", "middlewares"]),
    ...mapGetters(["loading"])
  },
  methods: {
    async fetchData() {
      await this.$store.dispatch("traefik/fetchAll");
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
